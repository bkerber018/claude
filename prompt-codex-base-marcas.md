# Prompt para o Codex — base de prospecção de indústrias com marca registrada

> **Versão 3.** A v1 foi revisada pelo próprio Codex e a crítica dele foi incorporada.
> A inspeção da RPI, que a v1 pedia como primeira tarefa, **já foi feita** — o resultado está aqui dentro.
> Cole tudo abaixo da linha. É autocontido: não depende de nenhum contexto anterior.

---

## Contexto

Trabalho numa operadora de canais de marketplace. Vendemos operação de canal (Mercado Livre, Amazon, Shopee, TikTok Shop) para **donos de marca** — indústrias e importadores exclusivos. Não vendemos para varejo nem para distribuidor que só revende marca de terceiro: sem marca própria não há Brand Registry, não há controle de preço e não há buy box a proteger.

Preciso de uma base nacional que gere listas de prospecção de **fabricantes donos de marca registrada**, em qualquer segmento — pet, cosmético, alimento, utilidade doméstica, ferramenta, brinquedo, moda. O segmento é um filtro no fim, não um projeto separado.

Hoje o processo é o inverso e é ruim: pegamos uma lista pronta (expositores de feira, associados de entidade) e tentamos descobrir quem ali é fabricante. Medi numa base de 441 empresas:

- **9,3%** eram indústria de fato
- **60%** das empresas cujo nome sugeria "indústria" NÃO eram indústria pelo CNAE
- **100%** das que tinham "Import"/"Importação" na razão social não tinham CNAE de importação
- **~30%** das com "Distribuidora" no nome eram varejo na Receita
- **6%** dos CNPJs falhavam no dígito verificador — o número não existe

**Nome de empresa não informa atividade.** A lista tem que nascer do registro oficial.

## Objetivo

Um pipeline reprodutível que produza `industrias_com_marca`: uma linha por empresa, onde toda linha satisfaça:

1. **É indústria** — tem estabelecimento ativo com CNAE principal nas divisões 10 a 33
2. **Tem marca** — é titular de processo de marca no INPI
3. **Não é MEI** — e a situação cadastral é ativa

Depois quero filtrar por CNAE, UF, classe de Nice, porte e estado da marca, para montar a lista de cada campanha.

---

# Decisões já tomadas — implemente assim, não pergunte

A revisão anterior levantou seis ambiguidades reais. Todas estão decididas abaixo. **Se você discordar de alguma, diga antes de implementar — mas não pare o projeto para perguntar.**

### D1 · "É indústria" = qualquer estabelecimento, consolidado no CNPJ básico

A empresa entra se **qualquer estabelecimento ativo** tiver CNAE principal nas divisões 10–33. Não exijo que seja a matriz.

Motivo: fabricante com sede administrativa em CNAE de escritório ou holding, e fábrica numa filial, é caso comum. Exigir a matriz perde esses. Já vi acontecer na prática.

Consolide por **CNPJ básico** (8 dígitos) e preserve:

| Coluna | Conteúdo |
|---|---|
| `cnpj_basico` | chave da empresa |
| `cnpj_matriz` | CNPJ completo da matriz |
| `cnae_principal_matriz` | o que a matriz declara |
| `estabelecimentos_industriais` | lista de CNPJs completos com CNAE 10–33 |
| `qtd_estabelecimentos_ativos` | |
| `criterio_inclusao` | `MATRIZ_INDUSTRIAL` ou `FILIAL_INDUSTRIAL` |

Assim eu consigo, depois, apertar o critério sem reprocessar nada.

### D2 · "Marca" tem quatro estados, e eu quero os quatro

Não colapse em um booleano. Crie:

| Coluna | Significado |
|---|---|
| `tem_processo_inpi` | aparece como titular em qualquer processo |
| `tem_pedido_pendente` | depósito sem decisão final |
| `tem_registro_concedido` | houve concessão (`IPAS158`) |
| `tem_marca_viva` | concedido e **sem** extinção/nulidade/arquivamento posterior |
| `despacho_mais_recente` | código + data |
| `situacao_calculada_em` | data da revista mais recente processada |

**A lista comercial principal usa `tem_marca_viva`** — é o que habilita Brand Registry.

Mas `tem_pedido_pendente` **não é descarte, é gatilho de timing.** Empresa depositando marca agora é empresa prestes a lançar ou a proteger algo — é o melhor momento para uma abordagem. Quero essa lista separada, não misturada.

### D3 · Estado da marca se reconstrói por histórico, não por evento isolado

Este é o ponto conceitual mais importante do projeto.

**A RPI publica movimentação, não acervo.** Um processo aparece só na semana em que teve despacho. Encontrar uma concessão numa revista não significa que a marca está viva hoje — pode ter sido extinta depois.

Portanto: **agregue todos os despachos por número de processo, ordene por data e derive o estado final.** Não trate cada linha da RPI como verdade isolada. Eventos que mudam estado: concessão, prorrogação, arquivamento, extinção, nulidade, transferência de titularidade.

Levante a tabela completa de códigos IPAS no Manual de Marcas do INPI antes de fechar a regra. Os códigos que já identifiquei estão no apêndice.

### D4 · A junção é por CNPJ básico; o CNPJ completo fica guardado

Quando houver CNPJ (só virá da busca do INPI, ver D6), junte no **básico de 8 dígitos**, porque o INPI pode informar matriz ou filial e não há como saber qual.

Guarde sempre: valor bruto do INPI, valor normalizado, resultado da validação de DV, CNPJ básico derivado, método de correspondência e confiança.

Junção por nome nunca é apresentada como igualdade. Use `confianca_match` com estes níveis:

`EXATA_CNPJ` · `NOME_NORMALIZADO_UNICO` · `NOME_NORMALIZADO_AMBIGUO` · `NOME_CURTO_BAIXA_CONFIANCA` · `SEM_CORRESPONDENCIA` · `REVISADA_MANUALMENTE`

**Nada abaixo de `NOME_NORMALIZADO_UNICO` entra na lista comercial sem revisão.**

### D5 · Porte: excluo só MEI, o resto vira filtro

Exclua MEI — não sustenta operação de canal. Isso exige baixar e cruzar também o **conjunto do Simples/MEI** da Receita; coloque isso nos entregáveis intermediários.

ME, EPP e demais portes **ficam na base**, com o porte como coluna filtrável. Não corte por porte no pipeline: a decisão é por campanha, e eu não quero reprocessar para mudar de ideia.

### D6 · O CNPJ do titular não existe na RPI — confirmado

**Já inspecionei a revista RM2907 (22/09/2026).** O elemento `<titular>` tem exatamente três atributos: `nome-razao-social`, `pais`, `uf`. **Não há CPF nem CNPJ.**

Varri os 53 MB: os 312 CNPJs presentes no arquivo estão dentro de texto corrido de exigência ("comprovar vínculo de grupo econômico com a empresa X (CNPJ ...)") e se referem a **terceiros**, não ao titular.

Consequência: a descoberta é por nome, e a resolução de CNPJ vem da busca do INPI (ver Fonte 2B). Não perca tempo procurando CNPJ no XML.

### D7 · CNPJ inválido vai para tabela de rejeição, não some

A v1 se contradizia. A regra correta:

- Registro com DV inválido vai para `rejeitados`, com motivo `DV_INVALIDO`
- Fica **fora** de `industrias_com_marca`
- O relatório conta separadamente: encontrados, rejeitados por motivo, recuperados

Nada some em silêncio. Nada entra sem passar.

---

## Fonte 1 — Base CNPJ da Receita Federal

`https://dadosabertos.rfb.gov.br/CNPJ/`

Publicação mensal, ZIP com CSV separados por `;`, encoding **latin-1** (não UTF-8 — assumir errado quebra os acentos silenciosamente).

| Arquivo | Uso |
|---|---|
| `Empresas*.zip` | razão social, natureza jurídica, capital social, **porte** |
| `Estabelecimentos*.zip` | CNAE principal e secundários, situação cadastral, UF, município, matriz/filial |
| `Simples*.zip` | **identificação de MEI** (necessário para D5) |
| `Cnaes`, `Municipios`, `Naturezas` | tabelas de domínio |

Armadilhas:

- Dezenas de GB descompactados. **Não carregue em memória.** DuckDB lendo CSV direto é o caminho mais simples e rápido.
- CNPJ vem em **três colunas** (básico, ordem, DV). Junte para formar os 14 dígitos.
- `situacao_cadastral`: **02 = ativa**.
- `identificador_matriz_filial`: 1 = matriz, 2 = filial. Ver D1.
- `porte_empresa` está em `Empresas`, não em `Estabelecimentos`.
- Baixe só o mês mais recente; confira no diretório qual é.

**Entregável:** `empresas_industria`, conforme D1.

## Fonte 2 — INPI

O INPI não tem API pública. São dois caminhos com papéis diferentes.

### 2A · RPI em XML — descoberta em massa

`https://revistas.inpi.gov.br/rpi/`

Schema confirmado no apêndice. Medidas de uma revista:

| Medida | Valor |
|---|---|
| Tamanho | 53 MB (9 MB zipado) |
| Processos | 37.393 |
| Titulares brasileiros | 34.373 de 37.419 (92%) |
| PJ distintos (heurística de sufixo) | ~11.760 |
| PF distintos | ~12.366 |
| Com classe de Nice | 29.236 (78%) |
| **UF preenchida nos titulares BR** | **100%** |

Sobre a junção por nome, medido na própria revista:

- Normalize forte: maiúsculas, sem acento, sem pontuação, sem sufixo societário (LTDA, ME, EPP, EIRELI, S.A., CIA).
- **Colisão interna: 59 chaves ambíguas em ~24 mil — 0,25%.** Baixa. A colisão contra a Receita (bases distintas, grafias distintas) será maior: **meça e reporte**.
- **940 chaves têm menos de 12 caracteres** (BIONEXO, AGA FOOD, UZE TOP). Marque como `NOME_CURTO_BAIXA_CONFIANCA`, não descarte.
- A UF resolve pouco: testei e ela desfaz só **5%** das colisões, porque a maioria é dentro do mesmo estado. Use, mas não conte com ela.

Valide o parser com 12 semanas. **Antes de baixar o histórico longo, me diga quantas revistas pretende puxar e qual cobertura estima** — ver D3, doze semanas não são um acervo.

**Entregável:** `marcas_inpi` (evento por evento) e `marcas_estado` (estado consolidado por processo, conforme D3).

### 2B · Busca do INPI via navegador — resolução de CNPJ

`https://busca.inpi.gov.br/pePI/`

Formulário com sessão, feito para humano. **É a única fonte pública que pode ter o CNPJ do titular.**

**Primeira tarefa aqui:** abra um processo qualquer e me diga se a página de detalhe mostra CPF/CNPJ do titular. Se mostrar, o projeto fecha com junção exata. Se não mostrar, o CNPJ não existe em fonte pública do INPI e a junção fica por nome em definitivo — o que ainda funciona, mas com taxa de erro que precisa ser medida e declarada na entrega.

Papel: **resolver, não descobrir.** Roda sobre a lista curta saída do cruzamento.

Use Playwright com Chromium. Delay entre requisições, sem paralelismo agressivo. **Pare se aparecer captcha ou bloqueio — não contorne proteção de serviço público.** Se houver limite, respeite e me avise.

---

## Regras de qualidade que não se negociam

1. **Dado ausente vale mais que dado errado.** Campo não confirmado fica vazio. Um dado errado faz o vendedor abrir a call falando bobagem e queima o lead.
2. **Nunca infira atividade ou marca a partir do nome.** Os números no topo mostram erro de 30% a 100% conforme o rótulo.
3. **Confira CNPJ dígito a dígito** em toda junção. Homônimo é regra, não exceção.
4. **Valide o DV** antes de usar. Ver D7.
5. **Proveniência por coluna:** de qual arquivo e de qual data veio cada campo.

## Entregáveis

1. **Código versionado**, com README: como rodar do zero, quanto tempo e quanto disco.
2. **Banco local** (DuckDB ou SQLite) com `empresas_industria`, `marcas_inpi`, `marcas_estado`, `industrias_com_marca`, `rejeitados`.
3. **Script de consulta** que recebe filtros (CNAEs, UFs, classes de Nice, porte, estado da marca) e cospe CSV pronto para o comercial.
4. **Relatório de cobertura**, com números reais e não arredondados:
   - indústrias ativas no país
   - quantas têm ao menos um processo no INPI
   - percentual de junção atingido e **por que o resto não casou**
   - distribuição de `confianca_match`
   - rejeitados por motivo
   - processos cujo estado não pôde ser resolvido por falta de histórico
5. **Auditoria de amostra reproduzível:** sorteie 20 linhas **com semente fixa**, confira à mão na busca do INPI e na consulta de CNPJ, e registre por linha: data da verificação, URLs consultadas, campos conferidos, esperado × observado, tipo do erro, evidência. Reporte a **taxa de erro medida, com denominador explícito** (por empresa e por campo).

## Como quero que você trabalhe

Quatro checkpoints, não nove. Pare nestes, siga nos outros:

| # | Checkpoint | O que apresentar |
|---|---|---|
| 1 | **Busca do INPI tem CNPJ?** | resposta objetiva, com print ou trecho da página |
| 2 | **Layout da Receita confere?** | 10 registros de Estabelecimentos já interpretados |
| 3 | **Piloto de 12 semanas rodado** | métricas de junção, ambiguidade e estado não resolvido |
| 4 | **Antes da escala histórica** | volume, tempo e disco estimados |

Fora desses quatro, decida e siga. As decisões de modelagem estão em D1–D7.

Me avise se uma fonte sair do ar, mudar de formato ou se alguma premissa minha estiver errada — **prefiro replanejar a receber resultado que parece certo e não é.** Não invente workaround silencioso.

## Prioridade se faltar tempo

1. Receita filtrada por indústria (sozinho já é ordens de grandeza melhor que lista de feira)
2. Parser da RPI + reconstrução de estado (D3)
3. Cruzamento com `confianca_match`
4. Resolução de CNPJ via busca do INPI
5. Consulta, relatório e auditoria

---

# Apêndice — Schema real do XML da RPI

Verificado na revista **RM2907, de 22/09/2026**. Encoding UTF-8.

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
      <classe-nice codigo="35"><especificacao>...</especificacao></classe-nice>
    </lista-classe-nice>
    <classes-vienna><classe-vienna .../></classes-vienna>
  </processo>
</revista>
```

**Atributos confirmados, com contagem numa revista:**

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

Elementos de texto: `nome` (da marca), `especificacao`, `texto-complementar`, `procurador`, `apostila`.

**Despachos mais frequentes:**

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

**Sinal comercial extra:** `cedente`/`cessionario` marcam **transferência de titularidade**. Marca que trocou de dono indica movimento societário — vale como gatilho de prospecção por si só, junto com `tem_pedido_pendente` (D2). Quero essas duas listas separadas da principal.
