# Pet Toys — proposta comercial (Mercado Livre e Amazon Brasil)

Sponsor: Luzival Leão. Outubro de 2026. Fases: Protagonista (meses 1–3) → Protagonista + 3P via Full (mês 4+).

| Arquivo | Para quem | O que é |
|---|---|---|
| **Proposta_PetToys.pdf** | cliente | Proposta de 19 páginas com premissas, projeção e cenários |
| **Projecao_PetToys.xlsx** | cliente | Projeção com fórmulas vivas; as células laranja são editáveis |
| **Contexto-PetToys-Diagnostico.pdf** | cliente | Diagnóstico de canal, capturas de 05/10/2026 |
| **mensagem-whatsapp.md** | envio | Texto da mensagem que acompanha os anexos |
| **manual-interno-pettoys.md** | **interno** | Horas, custo, margem, capacidade e riscos. Não enviar |
| proposta/index.html | apresentação | Versão navegável (← → e F para tela cheia) |

## Como regenerar

```
python3 build.py      # proposta/index.html (motor.py = réplica do simulador do Proposal Hub)
python3 planilha.py   # Projecao_PetToys.xlsx
NODE_PATH=$(npm root -g) node pdf.js $PWD/proposta/index.html <dir_png>   # depois junte os PNGs em PDF
```

As premissas ficam no topo de `build.py` (`BASE`, `FASE1`, `MES_INI`). A planilha foi recalculada
no LibreOffice e bate com a apresentação: pior caixa −R$ 33.500 (mai/27), investimento pago em out/27, acumulado de R$ 322.665 em nov/28.
