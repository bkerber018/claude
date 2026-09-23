# StillPet / Tudo Pet — Diagnóstico de canal (Amazon Brasil)

Fase 1 do `diagnostico-marketplace` da impulsio. Captura de **23/09/2026**, Amazon.com.br, CEP 12244000.

## Arquivos

- `Evidencias_StillPet_Amazon_BR_2026-09-23.xlsx` — planilha de evidências (7 abas)
- `build.py` — script que gera a planilha; editar aqui e rodar `python3 build.py` para atualizar

## Abas

| Aba | Conteúdo |
|---|---|
| Leia-me | Método, fontes, e **os limites do que foi verificado** |
| Vendedores | Os 5 vendedores no catálogo da marca Tudo Pet |
| ASINs StillPet | 28 ASINs: preço, vendedor, estoque, avaliações, categoria |
| Erros de cadastro | 19 itens acionáveis, priorizados (2 críticos, 9 altos) |
| Benchmark | 31 concorrentes que ocupam as buscas + os importados do topo patrocinado |
| Buscas | Termos capturados e onde a marca aparece (ou não) |
| Dispersão de preço | Mesmo ASIN a R$18,32 (1P) e R$11,25 (3P) |

## Regra da casa

Todo número tem fonte e data de print. Células `n/d` não foram capturadas — **não preencher por dedução**.
A cadeia causal da aba "Dispersão de preço" está marcada como **hipótese a confirmar com o cliente**.

## Restrição legal

Monitorar preço e orientar posicionamento: pode. Impor preço mínimo de revenda com punição: não
(Lei 12.529/2011). A correção proposta é no preço de sell-in da própria fábrica.

## Nota técnica

O LibreOffice deste ambiente não conseguiu recalcular o arquivo (timeout). As fórmulas são todas
`COUNTA`/`COUNTIF`/`MEDIAN`/aritmética e calculam normalmente ao abrir no Excel ou Google Sheets;
apenas não há valores em cache gravados.
