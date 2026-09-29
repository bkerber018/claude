# -*- coding: utf-8 -*-
import re, html

# slide -> {índice do run: novo texto}
EDITS = {
3: {0:'O OBJETIVO', 1:'03 / 11',
    2:'Uma ficha que responde', 3:'às perguntas da Amazon.',
    5:'Arquitetura de marca.', 6:'Como Still Pet, Tudo Pet e Quick Pet convivem no canal.',
    8:'Ficha no padrão.', 9:'Título, atributo, categoria e conteúdo', 10:'do jeito que a Amazon filtra.',
    12:'Catálogo em ondas.', 13:'As 151 fichas no ar primeiro. Depois, dez', 14:'novos por mês. ', 15:'', 16:'',
    17:'A impulsio organiza o catálogo dentro da conta da ', 18:'Still Pet'},

4: {0:'ESCOPO · AUDITORIA E ARQUITETURA', 1:'04 / 11',
    2:'Antes de corrigir, decidir o padrão.',
    3:'O primeiro mês lê a conta inteira e define a régua que vale para todas as fichas.',
    4:'AS 151 FICHAS NO AR', 5:'Ler uma a uma: título, atributo, categoria,', 6:'conteúdo e erro de cadastro.',
    7:'ARQUITETURA DE MARCA', 8:'Definir como as três marcas convivem no', 9:'canal e para qual as fichas migram.',
    10:'PADRÃO DE FICHA', 11:'Título, atributo e categoria que valem', 12:'para todo o catálogo, não caso a caso.',
    13:'PLANO DE ONDAS', 14:'Ordem de execução das 151 fichas e', 15:'critério de prioridade para as seguintes.'},

5: {0:'ESCOPO · EXECUÇÃO DE CATÁLOGO', 1:'05 / 11',
    2:'Corrigir o que está no ar.', 3:'Publicar o que vem depois.',
    4:'01 / ONDA 1 — CORREÇÃO', 5:'As 151', 6:'fichas no ar.',
    7:'Correção de título e atributo.', 8:'Categoria e ficha técnica.',
    9:'Imagens fornecidas pela ', 10:'Still Pet', 11:'.', 12:'Migração de marca.',
    13:'02 / ONDA 2 — SKUS NOVOS', 14:'Dez', 15:'por mês.',
    16:'Cadastro dos produtos novos.', 17:'Mesmo padrão da Onda 1.',
    18:'Prioridade definida pela Still Pet.', 19:'A partir do mês 3.'},

6: {0:'OS SEIS MESES', 1:'06 / 11',
    2:'Três movimentos.', 3:'Uma entrega contínua.',
    4:'Mês 1', 5:'Arquitetura', 6:'Leitura das 151 fichas.', 7:'Decisão de marca.', 8:'', 9:'',
    10:'Padrão de ficha.', 11:'Plano de ondas.', 12:'',
    13:'Meses 1–3', 14:'Onda 1', 15:'151 fichas corrigidas.', 16:'Categoria, atributo e título', 17:'.',
    18:'Meses 3–6', 19:'Onda 2 e fechamento', 20:'Dez SKUs novos por mês.',
    21:'Revisão contra a linha de partida.', 22:'Entrega de padrão e planilha.',
    23:'O prazo corre a partir do recebimento de cada insumo. Atraso de material desloca a entrega no mesmo número de dias.'},

7: {0:'O QUE NÃO ESTÁ INCLUÍDO', 1:'07 / 11',
    2:'E dizemos isso antes', 3:'de vocês perguntarem.',
    4:'COMERCIAL COM A AMAZON', 5:'Negociação', 6:' de preço, prazo, pedido ou entrada de produto.',
    8:'Gestão de performance', 9:'Venda, sell-out, rentabilidade e meta de faturamento.',
    10:'Essa relação continua sendo de vocês, direto com a Amazon.',
    11:'Mídia paga', 12:'Retail media não entra. Tráfego para ficha incompleta', 13:'vira desconto, não venda.',
    14:'Foto, vídeo e criativo', 15:'Produção de imagem não está no escopo. Usamos o', 16:'material que vocês fornecerem.',
    17:'Atendimento e jurídico', 18:'SAC, devolução, disputa com plataforma e assunto', 19:'jurídico de marca seguem com vocês.'},

8: {0:'COMO O TRABALHO É MEDIDO', 1:'08 / 11',
    2:'Três lentes sobre', 3:'o que a operação controla.',
    4:'01', 5:'Corrigir', 6:'Fichas no padrão: 0 → 191.', 7:'Erros críticos: 2 → 0.', 8:'Erros de categoria: 5 → 0.',
    9:'02', 10:'Publicar', 11:'SKUs novos no ar.', 12:'Dez por mês, meses 3 a 6.', 13:'Mesmo padrão da Onda 1.',
    14:'03', 15:'Manter', 16:'Regressão de ficha.', 17:'Atributo que some após edição.', 18:'Relatório mensal de execução.',
    19:'Não há meta de faturamento: o pedido é decisão da Amazon, e o preço e o estoque são de vocês.',
    20:'Linha de partida medida em 23 de setembro de 2026.'},

9: {0:'O INVESTIMENTO', 1:'09 / 11',
    2:'Dentro do orçamento que vocês definiram.',
    3:'SETUP E ARQUITETURA', 4:'R$ ', 5:'2', 6:'.500', 7:'Pagamento único',
    8:'Auditoria das 151 fichas, arquitetura de marca, padrão e plano de ondas',
    9:'EXECUÇÃO DE CATÁLOGO', 10:'R$ 2.', 11:'5', 12:'00/mês',
    13:'Seis meses de execução',
    14:'Correção das fichas, cadastro dos SKUs novos, monitoramento', 15:'e relatório mensal.',
    16:'Contrato de seis meses. Total de R$ 17.500, sem remuneração variável.',
    17:'Mídia e investimentos realizados diretamente nos canais não estão incluídos.',
    18:'191 fichas no padrão ao fim do contrato.'},

10:{0:'TITULARIDADE E SAÍDA', 1:'10 / 11',
    2:'Tudo que for construído', 3:'é de vocês.',
    4:'DURANTE', 5:'A conta é da Still Pet', 6:'A impulsio opera dentro da conta de vocês. Nada fica hospedado conosco.',
    7:'NA SAÍDA', 8:'Entrega em 15 dias',
    9:'Acessos, fichas, conteúdo, padrão e planilha de controle ficam com a',
    10:'Still Pet, sem retenção de nada.'},

11:{0:'O PRÓXIMO PASSO', 1:'11 / 11',
    2:'Começar pela régua, não pela ficha.',
    3:'Quatro movimentos entre o aceite e a primeira ficha corrigida.',
    4:'01', 5:'Aceite e pagamento', 6:'do setup',
    7:'02', 8:'Acesso ao Vendor Central e planilha do ERP',
    9:'03', 10:'Kickoff de alinhamento em', 11:'até 48 horas',
    12:'04', 13:'Decisão sobre a arquitetura', 14:'de marca',
    15:'CORRIGIR', 16:'As 151 fichas no ar.',
    17:'PUBLICAR', 18:'Dez SKUs novos por', 19:'mês.',
    20:'MANTER', 21:'O padrão, ficha a ficha.',
    22:'impulsio · operação de canais digitais para indústrias e distribuidores'},
}

def esc(t):
    return html.escape(t, quote=False)

total = 0
for n, edits in EDITS.items():
    p = f"un/ppt/slides/slide{n}.xml"
    x = open(p, encoding="utf-8").read()
    idx = [0]
    def repl(m):
        i = idx[0]; idx[0] += 1
        if i in edits:
            return "<a:t>" + esc(edits[i]) + "</a:t>"
        return m.group(0)
    x2 = re.sub(r'<a:t>.*?</a:t>', repl, x, flags=re.S)
    assert idx[0] > 0, f"slide{n}: nenhum run encontrado"
    open(p, "w", encoding="utf-8").write(x2)
    total += len(edits)
    print(f"  slide{n}: {idx[0]} runs, {len(edits)} trocados")

print("total de trocas:", total)

# varredura final: nada de Poytara, nada de internacional
import glob
resto = []
for f in glob.glob("un/ppt/**/*.xml", recursive=True):
    c = open(f, encoding="utf-8", errors="ignore").read()
    for termo in ("Poytara", "internacional", "assortment", "119"):
        if termo.lower() in c.lower():
            resto.append((f.split('/')[-1], termo))
print("resíduos:", resto if resto else "nenhum")
