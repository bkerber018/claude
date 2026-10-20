# Nutral · análise de mercado — ficha, diagnóstico e pendências

Documento interno impulsio. Captura de dados: 20/10/2026. Base anterior: Raio-X e planilha de 29/09/2026 (`entrada/`).
Evidências numéricas em `Evidencias_Nutral_ML_2026-10-20.xlsx` (gerada por `build_evidencias.py`).

> Vendas e GMV citados aqui são **estimativas JoomPulse**. Servem para comparar marcas e catálogos, não para meta nem cobrança.

---

## 1. Ficha da conta

| Campo | Valor | Origem |
|---|---|---|
| Marca | Nutral (linhas Nutral, Nutral Ouro, Nutrafish, Nutral Bird, Nutral Dog) **e Mega Food** | Catálogo 2021 |
| Empresa | Nutral Indústria, Campinas-SP · nutral.com.br · megafoodpet.com.br | Catálogo 2021 |
| Razão social / CNPJ | — | **pendente** |
| Quem decide | Maurício (cargo não registrado) | Planilha 29/09, aba Resumo |
| Quem estará na sala | — | **pendente** |
| Tempo de mercado | Desde 1980 | Catálogo 2021 |
| Divisão do faturamento | — | **pendente** |
| SKUs / categorias | 28 apresentações no site atual (12 páginas). O catálogo 2021 tem muito mais, incluindo toda a linha Mega Food. Categorias: peixes ornamentais, lagos/carpas, répteis, aves, cães | Planilha + catálogo |
| Canais onde vende | Não foi identificada venda própria. Venda via revenda no ML, Shopee, Amazon e Cobasi | Raio-X + JoomPulse |
| Rede de revenda online | Sim: Acquapex, Turma Pet, POPi BOX, Aquaturbo, AquárioStop, Yellowfish, Fischcat Dog, Carmo Pets, Bonanza, MercadoAquário e outros | JoomPulse |
| Marca no INPI | — | **pendente** |
| ERP | — | **pendente** |
| Dor declarada (palavras do dono) | — | **pendente: não há transcrição** |
| Valores já ditos ao cliente | — | **pendente** |

---

## 2. Diagnóstico

### 2.1 A tese do Raio-X, testada

O Raio-X (slide 9 da numeração impressa) afirma que os revendedores "disputam o mesmo anúncio e derrubam a margem de toda a rede". **O dado de 20/10 não sustenta isso.**

Em **9 de 9 catálogos com mais de um vendedor**, o buy box **não** está com o menor preço:

| Produto | Menor preço | Buy box | Diferença |
|---|---|---|---|
| Nutrafish Básica 1 kg | R$ 148,99 | ACQUAPEX · R$ 210,50 | +41% |
| Carpa 2 kg | R$ 178,10 | AQUÁRIOSTOP SHOW · R$ 228,00 | +28% |
| Mega Food Jabuti 200 g | R$ 49,00 | AQUATURBO_SHOP · R$ 58,90 | +20% |
| Mega Food Bits Média 500 g | R$ 67,99 | YELLOWFISH · R$ 142,55 | +110% |
| Tartaruga Criador 1,3 kg | R$ 178,00 | TURMA PET · R$ 189,99 | +7% |

Leitura: quem vende não é quem cobra menos, e sim quem tem Full, reputação e histórico. O problema não é guerra de preço — é que **ninguém da Nutral decide quem ocupa o buy box**. Mesma inversão da São Benedito, e é ela que vende o trabalho: organização se compra, preço não.

### 2.2 O que mudou desde 29/09 (e vai aparecer se o Maurício abrir a página)

- **Carpa 2 kg**: buy box saiu de POPi BOX para AQUÁRIOSTOP SHOW. Faixa caiu de R$ 178,10–299,90 para R$ 178,10–252,00 (print de 20/10 confirma o teto de R$ 252).
- **Tartaruga Criador**: buy box saiu de POPi BOX para TURMA PET. Faixa de R$ 184,29–346,90 para R$ 178,00–236,90.
- Isso vira argumento, desde que dito antes: "em três semanas o buy box trocou de mão nos dois produtos principais, sem a Nutral decidir nada".

### 2.3 O que a planilha deixou de fora

1. **Nutrafish Básica 1 kg é o produto mais vendido da família** (catálogo MLB19939966, cerca de 63 pedidos/mês estimados, contra cerca de 15 da Carpa 2 kg). A planilha marcou "catálogo não identificado". O deck abre com a Carpa; deveria abrir com o Nutrafish.
2. **Mega Food é da mesma indústria** e foi tratada como ruído. Em Alimentos (Peixes), MEGAFOOD soma 14 vendedores, 75 produtos e R$ 12.028,28/mês estimados. Há produto Mega Food cadastrado com a marca NUTRAL (Carnívoros 1,5 kg) e um kit de terceiro que junta Nutricon (concorrente) com Mega Food.
3. **O tamanho da categoria**: Alimentos para peixes (MLB1094) somou R$ 2,70 mi estimados em ago/2026, com 1.089 vendedores e 792 marcas; o maior vendedor tem 14,6% dos pedidos. Categoria pulverizada, sem dono.
4. **Posição da Nutral**: 9ª marca da categoria (R$ 39.278,38/mês estimados, 25 vendedores, 84 produtos). Poytara lidera com R$ 758.141,85, 319 vendedores e 3.731 produtos. A diferença não é de produto, é de alcance de rede.

### 2.4 Achados que viram pergunta, não afirmação

| Achado | Pergunta para a sala | Se sim | Se não |
|---|---|---|---|
| Duas ofertas "POPi BOX EMBALAGENS" na Carpa 2 kg (print), ligadas no JoomPulse a duas contas: NETE4UVARIEDADES e SILVACIAVARIEDADES | "A POPi BOX compra de vocês direto? Vocês sabem que ela opera com duas contas?" | Credenciamento passa a ter regra de uma conta por parceiro; entra no escopo de governança | Vira caso de origem de produto a investigar — sem acusação |
| Conta LS20260722105541078 (nome gerado automaticamente) aparece em 7 dos 10 catálogos, sempre entre os três preços mais baixos | "Vocês reconhecem esse vendedor?" | Parceiro novo — orientar cadastro e preço sugerido | Mapear origem do estoque; monitoramento entra no escopo |
| Mega Food | "A Mega Food segue ativa? Entra no mesmo projeto?" | Escopo e volume de SKUs crescem; preço muda | Mantém só Nutral; Mega Food fica como onda 2 |

Cuidado: a POPi BOX pode ser cliente direto da Nutral. Nada no deck pode soar como suspeita sobre quem compra da fábrica.

---

## 3. Problemas no Raio-X de 29/09 para corrigir antes de reapresentar

1. **Postura contraditória**: o deck diz "sem precisar competir com quem já vende" (Protagonista); a planilha diz "loja oficial permite vender direto" (Protagonista + 3P). Isso decide deck e preço — precisa ser resolvido.
2. Slide 5 traz o buy box da POPi BOX, que já não vale.
3. Slide 9 afirma guerra de preço; o dado mostra o contrário (item 2.1).
4. Numeração duplicada (dois slides 07 e dois 08), texto cortado ("suple"), "analista papel", "Pelo analise", cartões brancos fora do padrão no slide "Uma marca com mais de 40 anos".
5. Slide 6 mistura o caso Tartaruga com o sinal de conteúdo do Nutrafish 250 g.

---

## 4. Prints que faltam (capturar até 5 dias antes da reunião)

| # | Canal | Busca exata | O que capturar | Onde entra |
|---|---|---|---|---|
| 1 | Mercado Livre | página do produto `MLB19939966` (Nutrafish 1 kg) | bloco do vendedor (buy box) e "outras ofertas" ordenado por preço | novo caso 1 |
| 2 | Mercado Livre | página do produto `MLB19999688` (Carpa 2 kg) | bloco do vendedor — o print atual mostra só a lista de ofertas | caso Carpa |
| 3 | Mercado Livre | `ração para peixe` (sem marca) | primeira página inteira, contagem visível | onde a Nutral aparece sem o nome |
| 4 | Mercado Livre | `ração nutral` | 6 primeiros, marcando Patrocinado | quem paga para aparecer no nome da marca |
| 5 | Mercado Livre | `ração mega food` | 6 primeiros | Mega Food no escopo |
| 6 | Mercado Livre | perfil das duas contas POPi BOX | página do vendedor de cada uma | pergunta 2.4 |

Captura de tela inteira, com data do sistema visível. Refazer 1 e 2 na véspera.
