"""Gera Projecao-Retorno.xlsx com fórmulas vivas. Premissas em azul são editáveis."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import LineChart, Reference

wb = Workbook()
p = wb.active; p.title = "Premissas"
azul = Font(color="0000FF"); neg = Font(bold=True)
prem = [
  ("Faturamento-alvo do canal (R$/mês)", 150000, "alvo", '#,##0'),
  ("Fee fixo mensal (R$)", 2900, "fixo", '#,##0'),
  ("Variável sobre o excedente", 0.02, "variavel", '0.0%'),
  ("Isenção do variável (R$/mês)", 50000, "isencao", '#,##0'),
  ("Meses com preço de entrada", 3, "pen", '0'),
  ("Margem de contribuição no preço de entrada", 0.05, "mpen", '0.0%'),
  ("Margem de contribuição depois (CONFIRMAR COM O CLIENTE)", 0.15, "mbase", '0.0%'),
  ("Formato da rampa (expoente)", 1.6, "curva", '0.0'),
]
p["A1"] = "Premissas da projeção — cenário, não meta"; p["A1"].font = Font(bold=True, size=13)
p["A2"] = "Células em azul são editáveis. Margem de contribuição = venda − produto − taxa do canal − frete − impostos."
names = {}
for i, (rot, v, n, fmt) in enumerate(prem, start=4):
    p.cell(i, 1, rot); c = p.cell(i, 2, v); c.font = azul; c.number_format = fmt
    names[n] = f"Premissas!$B${i}"
p["A13"] = "Cenários: mês em que o canal atinge o faturamento-alvo"; p["A13"].font = neg
cen = [("Conservador", 18), ("Base", 12), ("Acelerado", 6)]
for j, (n, T) in enumerate(cen):
    p.cell(14 + j, 1, n); c = p.cell(14 + j, 2, T); c.font = azul
p["A18"] = "Fora da conta: mídia paga, embalagem nova (clichê ≈ R$ 6 mil), capital de giro do estoque no Full, migração de venda hoje feita por distribuidores."
p.column_dimensions["A"].width = 62; p.column_dimensions["B"].width = 14

N = names
for j, (nome, _) in enumerate(cen):
    ws = wb.create_sheet(nome)
    T = f"Premissas!$B${14 + j}"
    hdr = ["Mês", "Faturamento", "Margem de contribuição", "Fee impulsio", "Resultado do mês", "Acumulado"]
    for k, h in enumerate(hdr, 1):
        ws.cell(1, k, h).font = neg; ws.column_dimensions["ABCDEF"[k-1]].width = 22
    for m in range(1, 25):
        r = m + 1
        ws.cell(r, 1, m)
        ws.cell(r, 2, f"={N['alvo']}*MIN(1,(A{r}/{T})^{N['curva']})")
        ws.cell(r, 3, f"=B{r}*IF(A{r}<={N['pen']},{N['mpen']},{N['mbase']})")
        ws.cell(r, 4, f"={N['fixo']}+{N['variavel']}*MAX(0,B{r}-{N['isencao']})")
        ws.cell(r, 5, f"=C{r}-D{r}")
        ws.cell(r, 6, f"=E{r}" if m == 1 else f"=F{r-1}+E{r}")
        for c in range(2, 7): ws.cell(r, c).number_format = '#,##0;[Red]-#,##0'
    ws["H2"] = "Mês do retorno"; ws["I2"] = '=IFERROR(INDEX(A2:A25,MATCH(1,INDEX((F2:F25>=0)*1,0),0)),"após 24")'
    ws["H3"] = "Pior momento de caixa"; ws["I3"] = "=MIN(0,MIN(F2:F25))"
    ws["H4"] = "Fee pago nos 6 primeiros meses"; ws["I4"] = "=SUM(D2:D7)"
    ws["H5"] = "Acumulado em 24 meses"; ws["I5"] = "=F25"
    for c in ("I3", "I4", "I5"): ws[c].number_format = '#,##0;[Red]-#,##0'
    for c in ("H2", "H3", "H4", "H5"): ws[c].font = neg
    ws.column_dimensions["H"].width = 30; ws.column_dimensions["I"].width = 14
    ch = LineChart(); ch.title = f"{nome}: faturamento e acumulado"; ch.height = 9; ch.width = 20
    ch.add_data(Reference(ws, min_col=2, min_row=1, max_row=25), titles_from_data=True)
    ch.add_data(Reference(ws, min_col=6, min_row=1, max_row=25), titles_from_data=True)
    ch.set_categories(Reference(ws, min_col=1, min_row=2, max_row=25))
    ws.add_chart(ch, "H8")
wb.save("Projecao-Retorno.xlsx"); print("ok")
