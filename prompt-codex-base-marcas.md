# Prompt para o Codex — montar base de prospecção de indústrias com marca registrada

> Cole tudo abaixo da linha no Codex (ou em qualquer agente com acesso livre à internet).
> Ele foi escrito para ser autocontido: não depende de nenhum contexto anterior.

---

## Contexto

Trabalho numa operadora de canais de marketplace. Vendemos operação de canal (Mercado Livre, Amazon, Shopee, TikTok Shop) para **donos de marca** — indústrias e importadores exclusivos. Não vendemos para varejo nem para distribuidor que só revende marca de terceiro, porque esses não têm Brand Registry, não controlam preço e não têm buy box a proteger.

Preciso montar, do zero, uma base nacional que me permita gerar listas de prospecção de **fabricantes que são donos de marca registrada**, em qualquer segmento — pet, cosmético, alimento, utilidade doméstica, ferramenta, brinquedo, moda, o que for.

Hoje o processo é o inverso e é ruim: pegamos uma lista pronta (expositores de feira, associados de entidade) e tentamos descobrir quem ali é fabricante. Medi isso numa base de 441 empresas e o resultado foi:

- **9,3%** eram indústria de fato
- **60%** das empresas cujo nome sugeria "indústria" NÃO eram indústria pelo CNAE
- **100%** das empresas com "Import"/"Importação" na razão social não tinham CNAE de importação
- **~30%** das que tinham "Distribuidora" no nome eram varejo na Receita

Conclusão: **nome de empresa não informa atividade.** A lista precisa nascer do registro oficial, não de um diretório.

## O que eu quero que você construa

Um pipeline reprodutível que produza uma tabela com uma linha por empresa, onde toda linha satisfaça simultaneamente:

1. **É indústria** — CNAE principal registrado na Receita Federal nas divisões 10 a 33
2. **Tem marca registrada** — é titular de pelo menos um registro de marca no INPI
3. **Tem porte mínimo** — não é MEI; situação cadastral ativa

Depois quero poder filtrar essa tabela por CNAE, por UF, por classe de Nice da marca e por porte, para gerar a lista de cada campanha.

## Fonte 1 — Base CNPJ da Receita Federal (dados abertos)

`https://dadosabertos.rfb.gov.br/CNPJ/`

Publicação mensal, em arquivos ZIP com CSV separados por `;` e encoding **latin-1** (não UTF-8 — isso quebra se você assumir errado). Os conjuntos relevantes:

| Arquivo | Contém |
|---|---|
| `Empresas*.zip` | CNPJ básico (8 dígitos), razão social, natureza jurídica, capital social, porte |
| `Estabelecimentos*.zip` | CNPJ completo (básico + ordem + DV), CNAE fiscal principal, CNAEs secundários, situação cadastral, UF, município, data de início |
| `Cnaes.zip`, `Municipios.zip`, `Naturezas.zip` | tabelas de domínio para decodificar os códigos |

Pontos de atenção que você vai encontrar:

- Os arquivos são grandes (dezenas de GB descompactados no total). **Não carregue tudo em memória.** Use DuckDB ou SQLite, ou leia em chunks com pandas. DuckDB lendo CSV direto é o caminho mais simples e rápido.
- O CNPJ vem **em três colunas separadas** (básico, ordem, DV). Junte-as para formar o CNPJ de 14 dígitos.
- `situacao_cadastral`: **02 = ativa**. Filtre por isso.
- `identificador_matriz_filial`: 1 = matriz, 2 = filial. Para prospecção, normalmente você quer a matriz — mas CNAE pode variar por estabelecimento, então decida explicitamente e documente a escolha.
- `porte_empresa` está em `Empresas`, não em `Estabelecimentos`: 01 = micro, 03 = pequeno, 05 = demais. MEI é identificado no Simples, em arquivo separado.
- Baixe apenas o mês mais recente. Confira no diretório qual é.

**Entregável desta fonte:** uma tabela `empresas_industria` com CNPJ, razão social, nome fantasia, CNAE principal (código e descrição), CNAEs secundários, porte, capital social, UF, município, data de abertura — filtrada para CNAE principal nas divisões 10–33 e situação ativa.

## Fonte 2 — Marcas registradas no INPI

O INPI **não tem API pública**. Existem dois caminhos, e eu quero os dois:

### Caminho A — Revista da Propriedade Industrial (RPI) em XML

`https://revistas.inpi.gov.br/rpi/`

A RPI sai semanalmente e traz todos os despachos de marca, em XML. **Eu já inspecionei uma revista (RM2907, de 22/09/2026) e o schema está no apêndice no fim deste documento — não precisa descobrir do zero.**

**O achado que define a arquitetura do projeto: o XML NÃO traz o CNPJ do titular.** O elemento `<titular>` tem exatamente três atributos — `nome-razao-social`, `pais` e `uf`. Nada de CPF ou CNPJ. Varri o arquivo inteiro: os únicos CNPJs que aparecem estão dentro de texto corrido de exigência ("comprovar vínculo de grupo econômico com a empresa X (CNPJ ...)"), e se referem a terceiros, não ao titular.

Consequência: **a junção com a Receita tem que ser por razão social normalizada + UF.** Isso é impreciso e você precisa tratar como tal:

- Normalize agressivamente: maiúsculas, sem acento, sem pontuação, e remova sufixos societários (LTDA, ME, EPP, EIRELI, S.A., CIA).
- **Use a UF como desempate.** Ela vem preenchida em 100% dos titulares brasileiros — medi, são 34.143 de 34.143.
- Medi a taxa de colisão dentro da própria revista: 59 chaves normalizadas apontam para titulares diferentes, num universo de ~24 mil chaves. **0,25%.** É baixa, mas a colisão entre registros do INPI e da Receita (bases diferentes, grafias diferentes) vai ser maior — meça e me reporte.
- Nomes curtos são o perigo. Encontrei 940 chaves com menos de 12 caracteres (BIONEXO, AGA FOOD, UZE TOP). Trate qualquer chave curta como match de baixa confiança, e marque isso numa coluna em vez de descartar.

**Nunca entregue um match de nome como se fosse certeza.** Quero uma coluna `confianca_match` com o critério que a sustenta.

Sobre volume e cobertura, com números medidos numa revista:

| Medida | Valor |
|---|---|
| Tamanho do XML | 53 MB (9 MB zipado) |
| Processos numa revista | 37.393 |
| Titulares brasileiros | 34.373 de 37.419 (92%) |
| Titulares PJ distintos (heurística de sufixo) | ~11.760 |
| Titulares PF distintos | ~12.366 |
| Processos com classe de Nice | 29.236 (78%) |

**Atenção a um limite que muda o planejamento:** a RPI publica *movimentação*, não o acervo. Uma empresa só aparece na semana em que teve despacho. Para montar a base de marcas vivas você precisa **acumular anos de revistas**, não algumas semanas. Antes de baixar o histórico inteiro, me diga quantas revistas você pretende puxar e qual cobertura estima atingir.

Valide o pipeline com 12 semanas antes de rodar o histórico longo.

### Caminho B — Busca de marcas do INPI, via navegador

`https://busca.inpi.gov.br/pePI/`

É formulário com sessão, feito para humano. **Este é o caminho para obter o CNPJ**, que falta na RPI: a página de detalhe do processo mostra o titular com CPF/CNPJ. Confirme isso na primeira consulta e me diga se procede — se não procede, o CNPJ não existe em nenhuma fonte pública do INPI e a junção fica sendo por nome, ponto final.

O papel dele no projeto é **resolver, não descobrir**: rodar sobre a lista curta que saiu do cruzamento, para converter match por nome em match por CNPJ.

Use Playwright com Chromium. Respeite o serviço: delay entre requisições, sem paralelismo agressivo, e **pare se aparecer captcha ou bloqueio — não tente contornar proteção de serviço público.** Se houver limite, respeite e me avise.

### Caminho B — Busca de marcas do INPI, via navegador

`https://busca.inpi.gov.br/pePI/`

É formulário com sessão, feito para humano. Serve para **qualificar uma lista que já existe** ("este CNPJ tem marca?"), não para descobrir do zero.

Use Playwright com Chromium. A busca permite consultar por titular. Respeite o serviço: coloque delay entre requisições, não paralelize agressivamente, e pare se aparecer captcha ou bloqueio — não tente contornar proteção. Se o site impuser limite, respeite e me diga.

**Entregável desta fonte:** tabela `marcas_inpi` com número do processo, marca, titular (nome e CNPJ quando disponível), classe de Nice, situação e data.

## O cruzamento

```
empresas_industria  ⨝  marcas_inpi   ON  CNPJ do titular = CNPJ da empresa
```

Resultado: `industrias_com_marca` — uma linha por empresa, com as colunas da Receita mais:

- `qtd_marcas` — quantas marcas registradas a empresa tem
- `marcas` — lista dos nomes
- `classes_nice` — lista das classes
- `marca_mais_antiga` / `marca_mais_recente` — datas
- `tem_marca_viva` — se ao menos um registro está em vigor (não arquivado, não extinto)

## Regras de qualidade que não se negociam

Estas vêm de erro que já cometi e me custou caro:

1. **Dado ausente vale mais que dado errado.** Numa lista de prospecção, um dado errado faz o vendedor abrir a call falando bobagem e queima o lead. Campo que você não conseguiu confirmar fica **vazio**, nunca preenchido por dedução.
2. **Nunca infira atividade ou marca a partir do nome da empresa.** Os números no topo deste prompt mostram que o nome erra entre 30% e 100% dependendo do rótulo. Se a fonte oficial não disse, não é dado.
3. **Confira CNPJ dígito a dígito** em qualquer junção. Homônimo de razão social é a regra, não a exceção — "Distripet", "Delta Imports", "Cia do Pet" aparecem várias vezes com CNPJs diferentes.
4. **Valide o dígito verificador do CNPJ** com o algoritmo oficial antes de usar. Na base de 441 que analisei, **26 CNPJs (6%) falhavam no DV** — ou seja, o número não existe. Marque, não descarte silenciosamente.
5. **Registre a proveniência de cada coluna.** Quero saber, por campo, de qual arquivo e de qual data ele veio.

## Entregáveis

1. **Código versionado** no repositório, com README explicando como rodar do zero e quanto tempo/disco leva.
2. **Banco local** (DuckDB ou SQLite) com as tabelas `empresas_industria`, `marcas_inpi` e `industrias_com_marca`.
3. **Um script de consulta** que recebe filtros (lista de CNAEs, UFs, classes de Nice, porte mínimo) e cospe um CSV pronto para o time comercial.
4. **Relatório de cobertura**, com números reais e não arredondados:
   - quantas empresas de indústria ativas existem no país
   - quantas têm ao menos uma marca no INPI
   - qual o percentual de junção que você conseguiu, e por que o resto não casou
   - quantos CNPJs foram descartados por DV inválido
5. **Auditoria de amostra:** sorteie 20 linhas do resultado final, confira manualmente na busca do INPI e na consulta de CNPJ, e me reporte a **taxa de erro medida**. Um número medido vale mais que a afirmação de que ficou tudo certo.

## Como quero que você trabalhe

- **Comece pequeno e me mostre antes de escalar.** Primeiro: baixe uma RPI, abra o XML, me diga o que tem dentro. Segundo: baixe um arquivo de Estabelecimentos, me mostre 10 linhas. Só depois construa o pipeline inteiro.
- **Me avise se alguma fonte estiver fora do ar ou tiver mudado de formato.** Não invente um workaround silencioso.
- **Se bater em limite de rate, de captcha ou de termos de uso, pare e me diga.** Não contorne proteção de serviço público.
- Se alguma premissa minha estiver errada — por exemplo, se a RPI não trouxer CNPJ, ou se a base da Receita tiver mudado de estrutura — **me diga em vez de adaptar por conta própria.** Prefiro replanejar a receber um resultado que parece certo e não é.

## Prioridade se faltar tempo

Se você só conseguir fazer uma parte, faça nesta ordem:

1. Base da Receita filtrada por indústria (isso sozinho já é muito melhor que qualquer lista de feira)
2. Parser da RPI + acúmulo de revistas
3. Cruzamento por nome + UF, com coluna de confiança
4. Resolução de CNPJ via busca do INPI para a lista curta
5. Script de consulta e relatório de cobertura

---

# Apêndice — Schema real do XML da RPI

Verificado na revista **RM2907, de 22/09/2026**. Encoding UTF-8. Estrutura:

```xml
<revista numero="2907" data="22/09/2026">
  <processo numero="906428203" data-deposito="..." data-concessao="..." data-vigencia="...">
    <despachos>
      <despacho codigo="IPAS161" nome="Extinção de registro pela expiração do prazo de vigência"/>
    </despachos>
    <titulares>
      <titular nome-razao-social="Mercilo João Rigon" pais="BR" uf="SC"/>
    </titulares>
    <procurador>MARIA ELISA SANTUCCI BREVES</procurador>
    <marca apresentacao="..." natureza="...">
      <nome>...</nome>
    </marca>
    <lista-classe-nice>
      <classe-nice codigo="35">
        <especificacao>...</especificacao>
      </classe-nice>
    </lista-classe-nice>
    <classes-vienna>
      <classe-vienna .../>
    </classes-vienna>
  </processo>
</revista>
```

**Atributos confirmados, por elemento** (contagem numa revista):

| Elemento | Atributos | Ocorrências |
|---|---|---|
| `processo` | `numero`, `data-deposito`, `data-concessao`, `data-vigencia` | 37.393 |
| `titular` | `nome-razao-social`, `pais`, `uf` — **e só isso** | 37.419 |
| `despacho` | `codigo`, `nome` | 37.588 |
| `marca` | `apresentacao`, `natureza` | 20.982 |
| `classe-nice` | `codigo` | 30.574 |
| `requerente` | `nome-razao-social`, `pais`, `uf` | 5.814 |
| `cedente` / `cessionario` | `nome-razao-social` (+ `pais`, `uf` no cedente) | ~540 |
| `protocolo` | `numero`, `data`, `codigoServico` | 6.149 |

Elementos de texto (não atributo): `nome` (da marca), `especificacao`, `texto-complementar`, `procurador`, `apostila`.

**Códigos de despacho mais frequentes** — use-os para saber o estado do registro:

| Código | Qtd | Significado |
|---|---|---|
| `IPAS009` | 9.848 | Publicação de pedido para oposição |
| `IPAS158` | 9.004 | **Concessão de registro** |
| `IPAS029` | 6.150 | Deferimento do pedido |
| `IPAS270` | 3.721 | Deferimento da petição |
| `IPAS024` | 2.127 | Indeferimento do pedido |
| `IPAS136` | 1.560 | Exigência de mérito |
| `IPAS161` | 1.071 | **Extinção por expiração de vigência** |
| `IPAS360` | 754 | Notificação de recurso |

Para "tem marca viva", o sinal forte é `IPAS158` (concessão) sem `IPAS161` (extinção) posterior no mesmo processo. Levante a tabela completa de códigos IPAS no Manual de Marcas do INPI antes de fechar a regra.

`cedente`/`cessionario` marcam **transferência de titularidade** — é um sinal comercial interessante por si só: marca que mudou de dono recentemente costuma indicar movimento societário.
