# -*- coding: utf-8 -*-
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

F = "Arial"
H_FILL = PatternFill("solid", fgColor="1F3864")
H_FONT = Font(name=F, bold=True, color="FFFFFF", size=10)
TITLE  = Font(name=F, bold=True, size=14, color="1F3864")
SUB    = Font(name=F, italic=True, size=9, color="595959")
BODY   = Font(name=F, size=10)
BOLD   = Font(name=F, size=10, bold=True)
RED    = Font(name=F, size=10, bold=True, color="C00000")
YEL    = PatternFill("solid", fgColor="FFF2CC")
GRY    = PatternFill("solid", fgColor="F2F2F2")
THIN   = Border(*[Side(style="thin", color="BFBFBF")]*4)
WRAP   = Alignment(wrap_text=True, vertical="top")
TOP    = Alignment(vertical="top")

wb = Workbook()

def header(ws, row, cols):
    for i, c in enumerate(cols, 1):
        cell = ws.cell(row=row, column=i, value=c)
        cell.fill = H_FILL; cell.font = H_FONT
        cell.alignment = Alignment(wrap_text=True, vertical="center")
        cell.border = THIN
    ws.freeze_panes = ws.cell(row=row+1, column=1)

def widths(ws, ws_widths):
    for i, w in enumerate(ws_widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

def fill(ws, start, rows, wrapcols=()):
    for r, data in enumerate(rows, start):
        for c, v in enumerate(data, 1):
            cell = ws.cell(row=r, column=c, value=v)
            cell.font = BODY; cell.border = THIN
            cell.alignment = WRAP if c in wrapcols else TOP
        if r % 2 == 0:
            for c in range(1, len(data)+1):
                ws.cell(row=r, column=c).fill = GRY

# ---------------- 1. LEIA-ME ----------------
ws = wb.active; ws.title = "Leia-me"
widths(ws, [4, 30, 100])
ws["B2"] = "StillPet / Tudo Pet - Planilha de evidencias | Amazon Brasil"; ws["B2"].font = TITLE
ws["B3"] = "Fase 1 do diagnostico de canal - impulsio"; ws["B3"].font = SUB

meta = [
    ("Data de captura", "23/09/2026"),
    ("Canal", "Amazon.com.br"),
    ("CEP de referencia", "12244000 - Sao Jose dos Campos/SP"),
    ("Metodo", "Captura de tela do operador + WebSearch. JoomPulse NAO cobre Amazon; WebFetch em dominio Amazon e bloqueado."),
    ("Marcas rastreadas", "Tudo Pet (151 resultados no filtro de marca) | Still Pet | Quick Pet (aparece em embalagem)"),
    ("Validade", "Refazer as buscas na vespera da apresentacao. O cliente refaz a busca na frente do operador."),
]
r = 5
for k, v in meta:
    ws.cell(row=r, column=2, value=k).font = BOLD
    c = ws.cell(row=r, column=3, value=v); c.font = BODY; c.alignment = WRAP
    r += 1

r += 1
ws.cell(row=r, column=2, value="REGRA DA CASA").font = RED
ws.cell(row=r, column=3, value="Todo numero desta planilha veio de print datado. Nenhuma linha e estimativa da impulsio apresentada como fato. Celulas marcadas 'n/d' nao foram capturadas - NAO preencher por deducao.").font = BODY
ws.cell(row=r, column=3).alignment = WRAP
ws.cell(row=r, column=3).fill = YEL
r += 2

ws.cell(row=r, column=2, value="LIMITES DO QUE FOI VERIFICADO").font = RED
r += 1
limites = [
    "O filtro de marca 'Tudo Pet' devolve 151 resultados. NAO foi verificado quantos desses sao 1P (Amazon) e quantos sao 3P.",
    "'19 resultados' para 'still pet' e busca por TEXTO, nao contagem de marca - inclui concorrentes patrocinados. A contagem real de ASINs sob a marca Still Pet ainda nao foi capturada.",
    "Na busca generica, foram vistos os 48 primeiros de mais de 2.000. Nao se pode afirmar ausencia em toda a busca - apenas nos 48 primeiros e entre as marcas que a Amazon destaca no filtro.",
    "Na Bica Pedra existem '+2 ofertas'. NAO foi verificado se a Amazon 1P e uma delas nem a que preco.",
]
for l in limites:
    ws.cell(row=r, column=3, value="- " + l).font = BODY
    ws.cell(row=r, column=3).alignment = WRAP
    ws.row_dimensions[r].height = 28
    r += 1

r += 1
ws.cell(row=r, column=2, value="ABAS").font = BOLD
abas = [
    ("Vendedores", "Quem anuncia o catalogo da marca na Amazon hoje"),
    ("ASINs StillPet", "O catalogo documentado: preco, vendedor, estoque, avaliacoes, categoria"),
    ("Erros de cadastro", "Lista acionavel, priorizada por impacto - insumo do plano da Fase 1"),
    ("Benchmark", "Quem ocupa as buscas da categoria e a que preco"),
    ("Buscas", "Termos capturados, volume de resultados e onde a marca aparece"),
]
for k, v in abas:
    r += 1
    ws.cell(row=r, column=2, value=k).font = BODY
    ws.cell(row=r, column=3, value=v).font = BODY

# ---------------- 2. VENDEDORES ----------------
ws = wb.create_sheet("Vendedores")
widths(ws, [4, 32, 12, 38, 52])
ws["B2"] = "Vendedores no catalogo da marca Tudo Pet"; ws["B2"].font = TITLE
ws["B3"] = 'Fonte: filtro lateral "Vendido por", pagina da marca Tudo Pet, Amazon.com.br, 23/09/2026'; ws["B3"].font = SUB
header(ws, 5, ["", "Vendedor", "Modalidade", "O que e", "Evidencia capturada"])
vend = [
    ("", "Amazon.com.br", "1P", "Compra da StillPet desde 2019", "Buy Box em Coleira Estampas, Bebedouro Passaros, Comedouro Oval, Limpaquarium, Anel Macico, Comedouro Gato 100ml"),
    ("", "Cobasi - Essencial para a vida", "3P", "Grande rede varejista - cliente da Quick", "Ganha a Buy Box da Bica Pedra Calopsitas, que tem selo Escolha da Amazon"),
    ("", "Emporio Animal", "3P", "Revendedor", "Ganha a Buy Box do Bebedouro Hamster Drink Mouse 120ml"),
    ("", "Only Fish", "3P", "Especialista em aquarismo", "Listado no filtro de vendedores da marca"),
    ("", "Paraiso dos passaros", "3P", "Especialista em aves", "Listado no filtro de vendedores da marca"),
]
fill(ws, 6, vend, wrapcols=(4, 5))
for rr in range(6, 11):
    ws.row_dimensions[rr].height = 30
ws["B12"] = "TOTAL: 5 vendedores. 1 e a Amazon, que compra da StillPet. Os outros 4 chegaram sozinhos."
ws["B12"].font = RED
ws.merge_cells("B12:E12")
ws["B14"] = "LEITURA: Only Fish e Paraiso dos passaros sao especialistas de categoria e ocupam justamente as duas linhas de nicho da fabrica (aquarismo e aves). A rede fatiou o catalogo por categoria. A organizacao existe - so nao e da marca."
ws["B14"].font = BODY; ws["B14"].alignment = WRAP; ws["B14"].fill = YEL
ws.merge_cells("B14:E15")

# ---------------- 3. ASINs ----------------
ws = wb.create_sheet("ASINs StillPet")
widths(ws, [4, 52, 11, 11, 22, 16, 9, 8, 34, 20])
ws["B2"] = "Catalogo StillPet documentado na Amazon Brasil"; ws["B2"].font = TITLE
ws["B3"] = "Fonte: prints da pagina de marca e das fichas de produto, Amazon.com.br, 23/09/2026. 'n/d' = nao capturado."; ws["B3"].font = SUB
header(ws, 5, ["", "Produto", "Marca cadastrada", "Preco (R$)", "Vendedor (Buy Box)", "Estoque", "Avaliacoes", "Nota", "Categoria (breadcrumb)", "Selo / observacao"])
asins = [
 ("","Coleira P/Gato Elastico Estampas e Cores Variadas","Tudo Pet",13.81,"Amazon.com.br","Em estoque",842,4.2,"Gatos > Antipulgas e Carrapatos > Coleiras Antipulgas","Escolha da Amazon"),
 ("","Coleira P/Gato Elastico Con Guizo","Tudo Pet",12.07,"Amazon.com.br","Em estoque",156,4.2,"Gatos > Roupas","Preco exibido por kg"),
 ("","Comedouro Oval com 4 Furos p/ Passaros, Gigante","Tudo Pet",9.36,"Amazon.com.br","Sob encomenda",18,4.7,"Aves e Passaros > Comedouros","Material declarado: 'Madeira ou Plastico'"),
 ("","Bica Pedra Peq. para Passaros Calopsitas","Tudo Pet",12.99,"Cobasi","Em estoque",64,4.7,"Aves e Passaros > Brinquedos","Escolha da Amazon | frete R$5,90 | +2 ofertas"),
 ("","Bebedouro Grande para Passaros","Tudo Pet",18.32,"Amazon.com.br","Em estoque",29,3.7,"Aves e Passaros > Comedouros","2a oferta: Emporio Animal R$11,25 (-39%), FBA, 368 aval / 95% positivas"),
 ("","Bebedouro Beija-Flor Monsenhor 300ml","Tudo Pet",26.05,"n/d","Somente 1",23,3.8,"n/d",""),
 ("","Comedouro e Bebedouro Pesado Filhote Grande 450ml Rosa","Tudo Pet",34.90,"SEM BUY BOX","n/d",182,4.8,"n/d","'Nenhuma opcao de compra em destaque'"),
 ("","Comedouro Papagaio para Passaros","Tudo Pet",13.53,"n/d","Somente 2",20,3.9,"n/d",""),
 ("","Ninho de Madeira Pinus Calopsyta 'Para Caes'","Tudo Pet",39.90,"n/d","Somente 6",12,4.6,"n/d","Titulo diz 'Para Caes' - e ninho de ave"),
 ("","Comedouro e Bebedouro Pesado Mini Gato 150ml Vermelho","Tudo Pet",28.66,"n/d","Sob encomenda",1,5.0,"n/d","Selo 'Still Pet' no molde do produto"),
 ("","Limpa Facil Mini para Peixes","Tudo Pet",22.83,"n/d","n/d",57,3.6,"n/d",""),
 ("","Bebedouro Cacula para Passaros","Tudo Pet",8.40,"n/d","n/d",5,3.5,"n/d",""),
 ("","Comedouro e Bebedouro Pesado Medio 1500ml Azul","Tudo Pet",None,"n/d","n/d",210,4.7,"n/d","Selo 'Still Pet' no molde do produto"),
 ("","Comedouro e Bebedouro Pesado Grande 2500ml Vermelho","Tudo Pet",None,"n/d","n/d",7,5.0,"n/d","Selo 'Still Pet' no molde do produto"),
 ("","Compressor de Ar 5W 110V Maxxi Power para Peixes","Tudo Pet",None,"n/d","n/d",10,4.6,"n/d","Marca de terceiro (Maxxi) sob Tudo Pet"),
 ("","Refil Filtro HF 0600 para Peixes","Tudo Pet",35.90,"n/d","Somente 1",4,5.0,"n/d","Marca de terceiro (HF) sob Tudo Pet"),
 ("","Bebedouro Plastico Hamster Drink Mouse Inox 120ml","Tudo Pet",19.90,"Emporio Animal","Somente 7",35,4.4,"Roedores e Pequenos Animais","CNPJ 56.640.212/0001-98 na embalagem | peso '10 g'"),
 ("","Divisor 02 Saidas para Peixes","Tudo Pet",29.13,"n/d","Sob encomenda",5,4.6,"n/d",""),
 ("","Limpador de Esponja No 1 para Peixes","Tudo Pet",26.76,"n/d","Sob encomenda",56,4.1,"n/d",""),
 ("","Mangueira Aquario Silicone Rolo 2m","Tudo Pet",17.50,"n/d","Somente 8",97,4.4,"n/d",""),
 ("","Compressor de Ar 2,5W 220V Maxxi Power para Peixes","Tudo Pet",39.80,"n/d","n/d",65,4.5,"n/d","Marca de terceiro (Maxxi) sob Tudo Pet"),
 ("","Pa para Racao Azul","Tudo Pet",17.63,"n/d","n/d",19,4.3,"n/d",""),
 ("","Mangueira Aquario Rolo 2m","Tudo Pet",None,"n/d","n/d",7,4.3,"n/d",""),
 ("","Comedouro e Bebedouro Luxo Cao Transparente 300ml Vermelho","Tudo Pet",9.90,"n/d","n/d",4,3.8,"n/d","Comparavel direto: concorrentes 300ml de R$7,29 a R$13,20"),
 ("","Comedouro Transparente para Gato 100ml","Tudo Pet",21.92,"Amazon.com.br","Somente 1",4,5.0,"Cachorros > Potes e Tigelas","Produto de gato em categoria de cachorro | preco por kg"),
 ("","Tubo de Exercicios Curvo","Tudo Pet",21.79,"n/d","n/d",None,None,"n/d","Preco exibido por kg"),
 ("","Limpaquarium 1o Estagio Automatico","Still Pet",55.50,"Amazon.com.br","Somente 1",7,3.7,"Peixes e Animais Aquaticos > Acessorios para Aquario","Embalagem traz logo 'Quick Pet' | preco por kg | +2 ofertas"),
 ("","Anel Macico Cores Variadas","Still Pet",27.85,"Amazon.com.br","Sob encomenda",1,5.0,"Cachorros > Brinquedos > Mordedores","Selo 'Still Pet Forca Animal' | marca ausente do titulo"),
]
fill(ws, 6, asins, wrapcols=(2, 9, 10))
last = 5 + len(asins)
for rr in range(6, last+1):
    ws.row_dimensions[rr].height = 28
    ws.cell(row=rr, column=4).number_format = '#,##0.00'
s = last + 2
ws.cell(row=s, column=2, value="ASINs documentados").font = BOLD
ws.cell(row=s, column=3, value=f"=COUNTA(B6:B{last})").font = BODY
ws.cell(row=s+1, column=2, value="Sob marca 'Tudo Pet'").font = BODY
ws.cell(row=s+1, column=3, value=f'=COUNTIF(C6:C{last},"Tudo Pet")').font = BODY
ws.cell(row=s+2, column=2, value="Sob marca 'Still Pet'").font = BODY
ws.cell(row=s+2, column=3, value=f'=COUNTIF(C6:C{last},"Still Pet")').font = BODY
ws.cell(row=s+3, column=2, value="Em ruptura ('Somente X') ou sob encomenda").font = BODY
ws.cell(row=s+3, column=3, value=f'=COUNTIF(F6:F{last},"Somente*")+COUNTIF(F6:F{last},"Sob encomenda")').font = BODY
ws.cell(row=s+4, column=2, value="Buy Box em terceiro ou inexistente").font = RED
ws.cell(row=s+4, column=3, value=f'=COUNTA(E6:E{last})-COUNTIF(E6:E{last},"Amazon.com.br")-COUNTIF(E6:E{last},"n/d")').font = RED
ws.cell(row=s+6, column=2, value="Universo total do filtro de marca 'Tudo Pet': 151 resultados (print 23/09/2026). Esta aba documenta a amostra capturada, nao o catalogo inteiro.").font = SUB
ws.merge_cells(start_row=s+6, start_column=2, end_row=s+6, end_column=10)

# ---------------- 4. ERROS ----------------
ws = wb.create_sheet("Erros de cadastro")
widths(ws, [4, 46, 24, 46, 46, 12])
ws["B2"] = "Erros de cadastro identificados - lista acionavel"; ws["B2"].font = TITLE
ws["B3"] = "Cada linha e uma tarefa da Fase 1. Prioridade = impacto em busca, conversao ou risco de devolucao."; ws["B3"].font = SUB
header(ws, 5, ["", "Produto / escopo", "Tipo de erro", "O que esta no ar hoje", "Por que custa dinheiro", "Prioridade"])
erros = [
 ("","Catalogo inteiro (151 ASINs)","Atributos de filtro ausentes","Campos Especie, Capacidade (mL) e Recursos (anti-formiga, antiderrapante, antivomito) nao preenchidos","Cada filtro que o comprador clica e uma pergunta que a ficha nao responde. A marca some da busca filtrada.","CRITICO"),
 ("","Comedouro e Bebedouro Pesado Filhote 450ml Rosa","Sem Buy Box","'Nenhuma opcao de compra em destaque' - 4,8 estrelas e 182 avaliacoes","ASIN forte sem botao de compra em um clique. Venda perdida todo dia, reparavel em dias.","CRITICO"),
 ("","Still Pet / Tudo Pet / Quick Pet","Conflito de identidade de marca","Tres marcas circulando no mesmo catalogo sem hierarquia","Sete anos de autoridade diluidos em tres baldes. O algoritmo trata como tres marcas desconhecidas.","ALTO"),
 ("","Comedouros pesados (varios ASINs)","Marca do produto x marca da ficha","Selo 'Still Pet' moldado no plastico, campo Marca = 'Tudo Pet'","A marca de 40 anos e invisivel no canal. Quem compra nunca ve 'Still Pet'.","ALTO"),
 ("","Limpaquarium 1o Estagio","Marca do produto x marca da ficha","Cadastro 'Still Pet', embalagem na galeria traz logo 'Quick Pet'","Terceira identidade na mesma ficha. Confunde comprador e algoritmo.","ALTO"),
 ("","Bica Pedra Calopsitas","Descricao factualmente errada","'Funcao do produto: espelho para passaros' - o produto e pedra de calcio para bico","Risco de devolucao e reclamacao em um ASIN com selo Escolha da Amazon.","ALTO"),
 ("","Coleira P/Gato Elastico Estampas","Categoria errada","Gatos > Antipulgas e Carrapatos > Coleiras Antipulgas","Coleira decorativa vendida como antipulgas. Ranqueia na busca errada e gera devolucao.","ALTO"),
 ("","Coleira P/Gato Elastico Con Guizo","Categoria errada","Gatos > Roupas","Duas coleiras quase identicas em duas categorias, nenhuma em 'Coleiras'.","ALTO"),
 ("","Comedouro Transparente para Gato 100ml","Categoria errada","Cachorros > Potes e Tigelas","Produto de gato indexado em cachorro. Aparece em busca de roedor e some da busca de gato.","ALTO"),
 ("","Bica Pedra Calopsitas","Categoria errada","Aves e Passaros > Brinquedos","Suplemento de calcio classificado como brinquedo.","ALTO"),
 ("","Ninho de Madeira Pinus Calopsyta","Titulo errado","Titulo termina em 'Para Caes'","Ninho de ave anunciado para cachorro. Zero relevancia na busca certa.","ALTO"),
 ("","Comedouro Oval Passaros / Anel Macico / Comedouro Gato 100ml","Atributo invalido preenchido","'Adequacao do controle por radio: Passaros / Mastigar / Uso interno com gatos'","Campo de eletronico de controle remoto preenchido com texto aleatorio. Assinatura de upload em massa sem mapa de atributo.","MEDIO"),
 ("","Comedouro Oval para Passaros","Material indefinido","Material: 'Madeira ou Plastico'","Filtro de Material nao alcanca o produto.","MEDIO"),
 ("","Bebedouro Passaros / Drink Mouse","Peso irreal","'Peso do produto: 10 Gramas'","Peso errado afeta calculo de frete e elegibilidade logistica.","MEDIO"),
 ("","Anel Macico / Limpaquarium","Marca ausente do titulo","'Anel Macico Cores Variadas' - sem marca","Padrao de titulo inconsistente com o resto do catalogo, que comeca com 'Tudo Pet'.","MEDIO"),
 ("","Maxxi Power, HF 0600, Drink Mouse","Marca de terceiro sob a marca propria","Produtos de outros fabricantes cadastrados sob 'Tudo Pet'","Diluicao da marca e obstaculo para Brand Registry. Bate com os ~20%% de revenda declarados na call.","MEDIO"),
 ("","Coleira Con Guizo, Limpaquarium, Comedouro Gato, Tubo Exercicios","Unidade de medida errada","Preco exibido 'por kg' em produto que nao se vende por peso","Distorce a comparacao de preco na busca. ATENCAO: erro comum na categoria - ver aba Benchmark.","BAIXO"),
 ("","Coleira P/Gato Elastico Con Guizo","Idioma no titulo","'Con Guizo' - espanhol","Prejudica a correspondencia com o termo de busca em portugues.","BAIXO"),
 ("","Varios ASINs","Erro de digitacao repetido","'Medioio' em multiplos titulos","Termo de busca 'medio' nao casa com o titulo.","BAIXO"),
]
fill(ws, 6, erros, wrapcols=(2,3,4,5))
lastE = 5 + len(erros)
for rr in range(6, lastE+1):
    ws.row_dimensions[rr].height = 42
    p = ws.cell(row=rr, column=6)
    p.alignment = Alignment(horizontal="center", vertical="top")
    if p.value == "CRITICO":
        p.font = RED; p.fill = PatternFill("solid", fgColor="FFC7CE")
    elif p.value == "ALTO":
        p.font = Font(name=F, size=10, bold=True, color="9C5700"); p.fill = PatternFill("solid", fgColor="FFEB9C")
sE = lastE + 2
ws.cell(row=sE, column=2, value="Itens CRITICOS").font = RED
ws.cell(row=sE, column=3, value=f'=COUNTIF(F6:F{lastE},"CRITICO")').font = RED
ws.cell(row=sE+1, column=2, value="Itens ALTO").font = BOLD
ws.cell(row=sE+1, column=3, value=f'=COUNTIF(F6:F{lastE},"ALTO")').font = BODY
ws.cell(row=sE+2, column=2, value="Total de itens").font = BODY
ws.cell(row=sE+2, column=3, value=f"=COUNTA(C6:C{lastE})").font = BODY

# ---------------- 5. BENCHMARK ----------------
ws = wb.create_sheet("Benchmark")
widths(ws, [4, 20, 50, 12, 12, 8, 34])
ws["B2"] = "Quem ocupa as buscas da categoria"; ws["B2"].font = TITLE
ws["B3"] = "Fonte: buscas 'comedouro bebedouro cachorro plastico' e 'comedouro para roedor', Amazon.com.br, 23/09/2026"; ws["B3"].font = SUB
header(ws, 5, ["", "Marca", "Produto", "Preco (R$)", "Avaliacoes", "Nota", "Sinal capturado"])
bench = [
 ("","Mr Pet / SmartyKat","Comedouro Gato 120ml",3.38,207,4.5,"Mais vendido | +900 compras no mes"),
 ("","Furacao Pet","Comedouro Gato Anti Formiga 200ml Vermelho",3.58,97,4.5,"+100 compras no mes"),
 ("","Mr Pet / SmartyKat","Comedouro Econ Pata-Osso Filhote",4.23,346,4.6,"Escolha da Amazon | +100 compras no mes"),
 ("","Furacao Pet","Comedouro Plastica Gato Anti-Formiga 200ml Rosa",5.94,102,4.5,"Oferta"),
 ("","Furacao Pet","Comedouro Pop N.3 1000ml Azul",6.56,181,4.8,""),
 ("","Mr Pet","Comedouro Ecol Anti-Formiga Filhote",6.63,111,4.5,""),
 ("","Lilopety","Comedouro P 300ml Rosa",7.29,108,4.8,"Comparavel direto ao Luxo 300ml da StillPet (R$9,90)"),
 ("","Pet Injet","Comedouro Anti-Formiga Filhote Lilas",8.84,90,4.6,""),
 ("","Furacao Pet","Comedouro Pop N.4 1900ml Rosa",9.36,24,4.6,""),
 ("","Sem marca","Comedouro Antiformiga 300ml BPA Free",11.90,20,4.3,"Pequenas empresas"),
 ("","Furacao Pet","Comedouro Anti Formiga 350ml Vermelho",12.74,539,4.6,""),
 ("","Sanremo","Comedouro Cao Plastico 300ml Linha Pet",13.20,91,4.7,"Comparavel direto ao Luxo 300ml da StillPet"),
 ("","Furacao Pet","Comedouro Anti-Formiga N.1 350ml Rosa",14.44,143,4.6,"3 ofertas a partir de R$11,59"),
 ("","Chalesco","Tigela Inox 360ml",14.90,594,4.6,""),
 ("","Furacao Pet","Comedouro Anti-Formiga Luxo Duplo P Rosa",14.99,202,4.7,""),
 ("","Chalesco","Drinker 125ml para Roedores",15.50,407,4.6,"No 1 entre os melhores avaliados | +50 compras no mes"),
 ("","Chalesco","Drinker 250ml para Roedores",15.83,286,4.6,"+50 compras no mes"),
 ("","MY PET BRASIL","Comedouro Alto Ergonomico Anti-Formiga Gatos",16.05,167,4.4,"Oferta"),
 ("","Chalesco","Tigela Inox 750ml para Caes",19.00,1500,4.7,"No 1 entre os melhores avaliados | +50 compras no mes"),
 ("","Kaytee","Tigela Stoneware 3 In",20.00,2700,4.7,""),
 ("","Chalesco","Comedouro Suporte Simples 300ml Passaros Inox",20.10,195,4.6,"Concorrente direto da linha de aves da StillPet"),
 ("","Chalesco","Comedouro Inox 240ml",22.52,370,4.6,""),
 ("","Ferplast","Sirio L300 Alimentador Passaros Inox 0,3L",23.78,206,4.6,"Concorrente direto da linha de aves"),
 ("","MY PET BRASIL","Comedouro plastico para Roedores (cores sortidas)",24.48,2,5.0,"MARCA EM DESTAQUE | 93% positivas de 10K+ clientes | 10K+ pedidos recentes | vendido pela Amazon 1P"),
 ("","Pet Games","Bebedouro Funcional Alto Dog Drink P",25.18,245,4.8,""),
 ("","MY PET BRASIL","Comedouro Dupla Funcao 2 em 1",27.90,330,4.1,""),
 ("","Pet Games","Comedouro Brinquedo Redondog P",28.90,1900,4.5,"+50 compras no mes"),
 ("","Chalesco","Comedouro Duplo Cromado 360ml",38.00,2700,4.5,"+50 compras no mes"),
 ("","Pet Games","Comedouro Lento Mini Pet Fit Pink",39.00,1300,4.6,""),
 ("","Ferplast","PA 1088 Tigela Hamster ceramica 0,18L",46.90,6,5.0,""),
 ("","Chalesco","Bebedouro com Suporte e Comedouro Medio Azul",82.99,495,4.2,"+50 compras no mes"),
]
fill(ws, 6, bench, wrapcols=(3,7))
lastB = 5 + len(bench)
for rr in range(6, lastB+1):
    ws.row_dimensions[rr].height = 26
    ws.cell(row=rr, column=4).number_format = '#,##0.00'
sB = lastB + 2
ws.cell(row=sB, column=2, value="Preco mediano dos comparaveis").font = BOLD
ws.cell(row=sB, column=4, value=f"=MEDIAN(D6:D{lastB})").font = BODY
ws.cell(row=sB, column=4).number_format = '#,##0.00'
ws.cell(row=sB+1, column=2, value="Preco do comparavel StillPet (Luxo 300ml)").font = BOLD
ws.cell(row=sB+1, column=4, value=9.90).font = BODY
ws.cell(row=sB+1, column=4).number_format = '#,##0.00'
ws.cell(row=sB+1, column=7, value="Abaixo da mediana da categoria - e mesmo assim nao aparece nos 48 primeiros").font = RED

sB += 4
ws.cell(row=sB, column=2, value="TOPO PATROCINADO DA BUSCA 'comedouro para roedor' - todos importados").font = RED
sB += 1
header(ws, sB, ["", "Marca / vendedor", "Produto", "Preco (R$)", "Prazo", "", "Observacao"])
imp = [
 ("","Generico / mufern","Comedouro para Passarinho Plastico PP 6 Pecas Gaiola",143.62,"6 a 16 out",None,"Compra Internacional | Patrocinado 1o lugar"),
 ("","Generico / springway","Tigela de Ceramica Morango Comedouro para Roedores",104.90,"6 a 16 out",None,"Compra Internacional | categorizado em 'Substratos e Areia'"),
 ("","IEUDNS / LOVIVER US","Comedouro Dispensador para Coelhos e Chinchilas",254.91,"6 a 16 out",None,"Compra Internacional | Somente 1 em estoque"),
 ("","Generico / xinyee","Comedouro Automatico para Tanques Carpas Koi Tartarugas",1055.32,"7 a 19 out",None,"Compra Internacional | categorizado em 'Aves e Passaros'"),
]
fill(ws, sB+1, imp, wrapcols=(3,7))
for rr in range(sB+1, sB+5):
    ws.row_dimensions[rr].height = 26
    ws.cell(row=rr, column=4).number_format = '#,##0.00'
ws.cell(row=sB+6, column=2, value="LEITURA: os quatro primeiros lugares da busca sao produto importado generico, de R$104 a R$1.055, com tres semanas de entrega e categoria errada. A StillPet fabrica no Brasil, entrega amanha via 1P e vende a R$9,36. Nao esta perdendo para um concorrente melhor - esta perdendo para produto pior, mais caro e mais lento, que preencheu a ficha e comprou o anuncio.").font = BODY
ws.cell(row=sB+6, column=2).alignment = WRAP
ws.cell(row=sB+6, column=2).fill = YEL
ws.merge_cells(start_row=sB+6, start_column=2, end_row=sB+8, end_column=7)

# ---------------- 6. BUSCAS ----------------
ws = wb.create_sheet("Buscas")
widths(ws, [4, 42, 16, 60, 40])
ws["B2"] = "Buscas capturadas"; ws["B2"].font = TITLE
ws["B3"] = "Amazon.com.br, 23/09/2026, CEP 12244000"; ws["B3"].font = SUB
header(ws, 5, ["", "Termo / filtro", "Resultados", "Onde a StillPet aparece", "Marcas que a Amazon destaca no filtro"])
buscas = [
 ("","Filtro de marca: Tudo Pet","151","Universo do catalogo. 5 vendedores no filtro 'Vendido por'.","n/a"),
 ("","Busca por texto: 'still pet'","19","Os 2 primeiros sao PATROCINADOS de concorrentes (Petsko, newpet). Depois aparecem Limpaquarium e Anel Macico (marca Still Pet) e itens Tudo Pet.","n/a"),
 ("","'comedouro bebedouro cachorro plastico'","mais de 2.000","NENHUM produto Tudo Pet ou Still Pet nos 48 primeiros.","Pet Games, VDRBG, Chalesco, Great Pets, FURACAOPET, MRPET, MY PET BRASIL"),
 ("","'comedouro para roedor'","999","Aparece somente o 'Tudo Pet Comedouro Transparente para GATO 100ml' - produto errado, puxado pela categorizacao em Cachorros. A linha de roedores da fabrica nao aparece.","Pet Games, Chalesco, FURACAOPET, MRPET, MY PET BRASIL, Ferplast"),
]
fill(ws, 6, buscas, wrapcols=(2,4,5))
for rr in range(6, 10):
    ws.row_dimensions[rr].height = 60
ws.cell(row=12, column=2, value="ACHADO: em nenhuma das duas buscas genericas a marca da fabrica esta entre as marcas que a Amazon destaca. Em ambas, MY PET BRASIL esta - e a My Pet Brasil e distribuidora que revende StillPet (mypetbrasil.com/stillpet).").font = BODY
ws.cell(row=12, column=2).alignment = WRAP
ws.cell(row=12, column=2).fill = YEL
ws.merge_cells("B12:E14")


# ---------------- 7. DISPERSAO DE PRECO ----------------
ws = wb.create_sheet("Dispersao de preco")
widths(ws, [4, 34, 18, 14, 16, 20, 30])
ws["B2"] = "Dispersao de preco no mesmo ASIN"; ws["B2"].font = TITLE
ws["B3"] = "Fonte: tela 'outros vendedores', Amazon.com.br, 23/09/2026"; ws["B3"].font = SUB
header(ws, 5, ["", "Produto (mesmo ASIN)", "Vendedor", "Preco (R$)", "Logistica", "Entrega", "Reputacao do vendedor"])
disp = [
 ("","Tudo Pet Bebedouro Grande para Passaros","Amazon.com.br (1P)",18.32,"Amazon","Amanha, 24/set","-"),
 ("","Tudo Pet Bebedouro Grande para Passaros","Emporio Animal (3P)",11.25,"Enviado pela Amazon (FBA)","Domingo, 27/set","368 avaliacoes | 95% positivas em 12 meses"),
]
fill(ws, 6, disp, wrapcols=(2,3,5,7))
for rr in range(6, 8):
    ws.row_dimensions[rr].height = 30
    ws.cell(row=rr, column=4).number_format = '#,##0.00'
ws.cell(row=9, column=2, value="Diferenca").font = BOLD
ws.cell(row=9, column=4, value="=D7-D6").font = RED
ws.cell(row=9, column=4).number_format = '#,##0.00'
ws.cell(row=10, column=2, value="Terceiro mais barato que a Amazon 1P em").font = BOLD
ws.cell(row=10, column=4, value="=D7/D6-1").font = RED
ws.cell(row=10, column=4).number_format = '0.0%'
ws.cell(row=11, column=2, value="Multiplo entre a maior e a menor oferta").font = BOLD
ws.cell(row=11, column=4, value="=D6/D7").font = BODY
ws.cell(row=11, column=4).number_format = '0.00"x"'

ws.cell(row=13, column=2, value="O QUE A PROPRIA AMAZON EXIBE NA PAGINA").font = RED
ws.cell(row=14, column=2, value="'Disponivel a um preco mais baixo em outros vendedores que talvez nao ofereçam a entrega Prime gratis.' - a ressalva sobre Prime nao se aplica: o Emporio Animal usa FBA, entao o envio tambem e da Amazon.").font = BODY
ws.cell(row=14, column=2).alignment = WRAP; ws.cell(row=14, column=2).fill = YEL
ws.merge_cells("B14:G16")

ws.cell(row=18, column=2, value="HIPOTESE DE CAUSA - NAO CONFIRMADA, NAO LEVAR AO DECK SEM O CARLOS CONFIRMAR").font = RED
cadeia = [
 "1. Na call, a Beatriz declarou que a Amazon exigia desconto de 8% a 11% e que a StillPet 'subia um pouco o preco justamente para ter esse desconto'.",
 "2. A Amazon monta a margem dela sobre um custo ja inflado - o 1P chega a R$18,32.",
 "3. Um revendedor compra no atacado normal e lista via FBA a R$11,25, com margem.",
 "4. A propria pagina da Amazon avisa o comprador que existe mais barato ao lado.",
 "5. O ASIN 1P perde venda, e o algoritmo de compra da Amazon reduz o pedido de reposicao.",
 "6. Foi exatamente o que a StillPet descreveu: o produto que representava 60-70% da venda na Amazon caiu.",
 "7. A conclusao da fabrica virou 'a Amazon e burocratica e nao funciona'. A evidencia aponta para arquitetura de preco, nao burocracia.",
]
rr = 19
for c in cadeia:
    ws.cell(row=rr, column=2, value=c).font = BODY
    ws.cell(row=rr, column=2).alignment = WRAP
    ws.merge_cells(start_row=rr, start_column=2, end_row=rr, end_column=7)
    ws.row_dimensions[rr].height = 26
    rr += 1

rr += 1
ws.cell(row=rr, column=2, value="RESTRICAO LEGAL - Lei 12.529/2011").font = RED
rr += 1
ws.cell(row=rr, column=2, value="Monitorar preco e orientar posicionamento: pode. Impor preco minimo de revenda com punicao: NAO. A correcao aqui e no preco de sell-in que a StillPet pratica com a Amazon e com os distribuidores - o que e 100% legal e 100% sob controle dela. Nunca escrever 'MAP enforcement', 'preco minimo aplicado' ou 'garantimos que ninguem venda abaixo de X'.").font = BODY
ws.cell(row=rr, column=2).alignment = WRAP; ws.cell(row=rr, column=2).fill = YEL
ws.merge_cells(start_row=rr, start_column=2, end_row=rr+2, end_column=7)


wb.save("Evidencias_StillPet_Amazon_BR_2026-09-23.xlsx")
print("ok")
