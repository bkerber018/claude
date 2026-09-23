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

A RPI sai semanalmente e traz todos os despachos de marca. Os arquivos ficam disponíveis para download, em XML.

**Não confie na minha descrição do schema — inspecione o XML real antes de escrever o parser.** O que eu preciso extrair de cada processo de marca é:

- número do processo
- nome da marca (elemento nominativo)
- **titular: nome e, se houver, o CNPJ/CPF** ← este é o campo crítico, porque é a chave de junção com a Receita
- classe(s) de Nice
- código e descrição do despacho (para saber se é depósito, concessão, arquivamento, extinção)
- data

**A primeira coisa a fazer é baixar UMA revista, abrir o XML e me dizer o que ele realmente contém**, em especial se o CNPJ do titular está presente ou se só vem o nome. Isso muda todo o resto do projeto:

- **Se o CNPJ vier no XML:** a junção com a Receita é exata e o projeto é direto.
- **Se só vier o nome do titular:** precisamos casar por razão social normalizada contra a base da Receita, o que é impreciso e exige regra de desempate. Nesse caso, me avise antes de prosseguir — vamos decidir juntos o critério.

Para montar a base histórica, acumule várias revistas. Comece com as últimas 12 semanas para validar o pipeline; só depois rode o histórico longo.

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
2. Inspeção do XML da RPI e resposta sobre o CNPJ do titular
3. Cruzamento
4. Script de consulta e relatório de cobertura
