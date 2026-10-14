"""Gera a proposta comercial da Pet Toys (HTML) com a projeção calculada pelo
mesmo motor do simulador do Impulsio Proposal Hub (ver motor.py).

    python3 pettoys/build.py
"""
import pathlib
from motor import motor, payback, MAT_PADRAO

AQUI = pathlib.Path(__file__).parent
SAIDA = AQUI / "proposta" / "index.html"

# ───────────────────────── premissas ─────────────────────────
MAT_CONS = [0, 1, 2, 4, 7, 11, 15, 20, 26, 32, 38, 45, 51, 57, 63, 69, 74, 79, 84, 88, 91, 94, 96, 98, 99, 100, 100]
FASE1 = 3            # meses de Protagonista antes de abrir a venda direta
HORIZ = 25
MES_INI, ANO_INI = 10, 2026   # novembro de 2026 (índice 10)

def mat_fase(m):
    """Venda direta só existe depois da Fase 1; a rampa de maturação começa no mês 4."""
    return [0] * FASE1 + [x / 100 for x in m[1:]]

def mens(mm):
    return 3500 if mm <= 6 else 6200

BASE = dict(pot=200_000, marg=.20, adsP=.03, adsIni=FASE1 + 3, piso=1000, pisoAte=FASE1 + 6,
            setup=15_000, parc=6, mens=mens, varP=.02, gat=150_000,
            mIni=MES_INI, aIni=ANO_INI, n=HORIZ)

def roda(**ajuste):
    p = dict(BASE); mat = ajuste.pop("mat", MAT_PADRAO); p.update(ajuste)
    return motor(mat=mat_fase(mat), **p)

L = roda()
CEN = {
    "base": ("Base", L),
    "pot": ("Potencial de R$ 150 mil", roda(pot=150_000)),
    "cons": ("Conservador", roda(marg=.15, mat=MAT_CONS)),
}

def brl(v):
    s = f"{abs(round(v)):,.0f}".replace(",", ".")
    return ("−" if v < 0 else "") + "R$ " + s

def k(v):
    return ("−" if v < 0 else "") + f"{abs(v)/1000:,.0f}".replace(",", ".") + " mil"

def resumo(L):
    pior = min(L, key=lambda r: r["acum"])
    return dict(payback=payback(L) or "fora do horizonte", pior=pior, fim=L[-1]["acum"],
                gmv_fim=L[-1]["gmv"], fee=sum(r["imp"] for r in L[:12]))

R = {c: resumo(v[1]) for c, v in CEN.items()}
RB = R["base"]

MESES_LONGO = {"jan": "janeiro", "fev": "fevereiro", "mar": "março", "abr": "abril", "mai": "maio",
               "jun": "junho", "jul": "julho", "ago": "agosto", "set": "setembro", "out": "outubro",
               "nov": "novembro", "dez": "dezembro"}
def longo(rot):
    m, a = rot.split("/"); return f"{MESES_LONGO[m]} de 20{a}"

# ───────────────────────── gráficos SVG ─────────────────────────
W, H = 1000, 380
PL, PR, PT, PB = 70, 20, 24, 44

def escala(vmin, vmax):
    import math
    passo_bruto = (vmax - vmin) / 5
    mag = 10 ** math.floor(math.log10(passo_bruto))
    passo = min((m * mag for m in (1, 2, 2.5, 5, 10) if m * mag >= passo_bruto))
    lo = math.floor(vmin / passo) * passo; hi = math.ceil(vmax / passo) * passo
    return lo, hi, passo

def moldura(vmin, vmax, rots, cor_zero=True):
    lo, hi, passo = escala(vmin, vmax)
    n = len(rots)
    x = lambda i: PL + (W - PL - PR) * (i + .5) / n
    y = lambda v: PT + (H - PT - PB) * (hi - v) / (hi - lo)
    g = []
    v = lo
    while v <= hi + 1e-6:
        cls = "zero" if abs(v) < 1e-6 and cor_zero else "grid"
        g.append(f'<line class="{cls}" x1="{PL}" x2="{W-PR}" y1="{y(v):.1f}" y2="{y(v):.1f}"/>')
        g.append(f'<text class="ax" x="{PL-10}" y="{y(v)+4:.1f}" text-anchor="end">{k(v) if v else "0"}</text>')
        v += passo
    for i, r in enumerate(rots):
        if i % 3 == 0 or i == n - 1:
            g.append(f'<text class="ax" x="{x(i):.1f}" y="{H-PB+22}" text-anchor="middle">{r}</text>')
    return x, y, g

def faixa_fase(x, y0, y1):
    x0 = x(0) - (x(1) - x(0)) / 2; x1 = x(FASE1 - 1) + (x(1) - x(0)) / 2
    return (f'<rect class="f1" x="{x0:.1f}" y="{y0:.1f}" width="{x1-x0:.1f}" height="{y1-y0:.1f}"/>'
            f'<text class="tag" x="{x0+8:.1f}" y="{y0+16:.1f}">FASE 1</text>'
            f'<text class="tag" x="{x1+8:.1f}" y="{y0+16:.1f}">FASE 2 · VENDA DIRETA</text>')

def svg(corpo, rotulo):
    return f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="{rotulo}">{corpo}</svg>'

def graf_acumulado():
    vals = [r["acum"] for r in L]; rots = [r["rot"] for r in L]
    x, y, g = moldura(min(vals), max(vals), rots)
    g.insert(0, faixa_fase(x, PT, H - PB))
    pts = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(vals))
    area = f"{x(0):.1f},{y(0):.1f} {pts} {x(len(vals)-1):.1f},{y(0):.1f}"
    g.append(f'<polygon class="ar" points="{area}"/>')
    g.append(f'<polyline class="ln" points="{pts}"/>')
    ip = vals.index(min(vals))
    g.append(f'<circle class="dot hot" cx="{x(ip):.1f}" cy="{y(vals[ip]):.1f}" r="6"/>')
    g.append(f'<text class="lab hot" x="{x(ip):.1f}" y="{y(vals[ip])+26:.1f}" text-anchor="middle">pior momento · {brl(vals[ip])}</text>')
    pb = next(i for i, v in enumerate(vals) if v > 0)
    g.append(f'<circle class="dot grn" cx="{x(pb):.1f}" cy="{y(vals[pb]):.1f}" r="6"/>')
    g.append(f'<text class="lab grn" x="{x(pb)+14:.1f}" y="{y(vals[pb])+30:.1f}">investimento pago · {rots[pb]}</text>')
    return svg("".join(g), "Resultado acumulado da venda direta, cenário base")

def graf_gmv():
    rots = [r["rot"] for r in L]
    x, y, g = moldura(0, max(r["gmv"] for r in L) * 1.08, rots, cor_zero=False)
    g.insert(0, faixa_fase(x, PT, H - PB))
    bw = (x(1) - x(0)) * .62
    for i, r in enumerate(L):
        if r["gmv"] <= 0: continue
        cls = "bar bf" if r["rot"].startswith("nov") else "bar"
        g.append(f'<rect class="{cls}" x="{x(i)-bw/2:.1f}" y="{y(r["gmv"]):.1f}" width="{bw:.1f}" height="{y(0)-y(r["gmv"]):.1f}"/>')
    yg = y(BASE["gat"])
    g.append(f'<line class="gat" x1="{PL}" x2="{W-PR}" y1="{yg:.1f}" y2="{yg:.1f}"/>')
    g.append(f'<text class="lab amb" x="{PL+8}" y="{yg-8:.1f}">R$ 150 mil/mês · gatilho do variável</text>')
    return svg("".join(g), "Faturamento mensal projetado da venda direta")

def graf_cenarios():
    rots = [r["rot"] for r in L]
    todos = [r["acum"] for _, v in CEN.values() for r in v]
    x, y, g = moldura(min(todos), max(todos), rots)
    classes = {"base": "ln", "pot": "ln2", "cons": "ln3"}
    for c, (nome, serie) in CEN.items():
        pts = " ".join(f"{x(i):.1f},{y(r['acum']):.1f}" for i, r in enumerate(serie))
        g.append(f'<polyline class="{classes[c]}" points="{pts}"/>')
        u = serie[-1]
        g.append(f'<text class="lab {classes[c]}t" x="{x(len(serie)-1)-6:.1f}" y="{y(u["acum"])-10:.1f}" text-anchor="end">{nome}</text>')
    return svg("".join(g), "Resultado acumulado em três cenários").replace('class="chart"','class="chart c3"')

def tabela_mensal():
    linhas = []
    for r in L:
        cls = ' class="f1r"' if r["n"] <= FASE1 else (' class="bfr"' if r["rot"].startswith("nov") else "")
        linhas.append(
            f'<tr{cls}><td>{r["n"]}</td><td>{r["rot"]}</td><td>{brl(r["gmv"]) if r["gmv"] else "—"}</td>'
            f'<td>{brl(r["margem"]) if r["margem"] else "—"}</td><td>{brl(r["ads"]) if r["ads"] else "—"}</td>'
            f'<td>{brl(r["setup"] + r["mens"])}</td><td>{brl(r["var"]) if r["var"] else "—"}</td>'
            f'<td class="{"neg" if r["res"] < 0 else "pos"}">{brl(r["res"])}</td>'
            f'<td class="{"neg" if r["acum"] < 0 else "pos"}">{brl(r["acum"])}</td></tr>')
    return "".join(linhas)

# ───────────────────────── CSS adicional ─────────────────────────
CSS = """
<style>
.chart{width:100%;height:auto;max-height:52vh;display:block}
.chart .grid{stroke:var(--rule);stroke-width:1}
.chart .zero{stroke:var(--mute);stroke-width:1.2}
.chart .ax{fill:var(--mute);font-family:var(--fm);font-size:13px}
.chart .f1{fill:var(--ink3);opacity:.55}
.chart .tag{fill:var(--faint);font-family:var(--fm);font-size:11px;letter-spacing:.16em}
.chart .ar{fill:var(--seal);opacity:.12}
.chart .ln{fill:none;stroke:var(--seal-l);stroke-width:3;stroke-linejoin:round}
.chart .ln2{fill:none;stroke:var(--amber);stroke-width:2.4;stroke-dasharray:7 5}
.chart .ln3{fill:none;stroke:var(--hot);stroke-width:2.4;stroke-dasharray:2 5;stroke-linecap:round}
.chart .lnt{fill:var(--seal-l)} .chart .ln2t{fill:var(--amber)} .chart .ln3t{fill:var(--hot)}
.chart .lab{font-family:var(--fm);font-size:13px;font-weight:700}
.chart .hot{fill:var(--hot)} .chart .grn{fill:var(--green)} .chart .amb{fill:var(--amber)}
.chart .dot{stroke:var(--ink);stroke-width:3}
.chart .bar{fill:var(--seal);opacity:.85} .chart .bar.bf{fill:var(--hot);opacity:.95}
.chart .gat{stroke:var(--amber);stroke-width:1.6;stroke-dasharray:6 5}
.chart.c3 .ax{font-size:20px} .chart.c3 .lab{font-size:21px}
.leg{display:flex;flex-wrap:wrap;gap:18px;font-family:var(--fm);font-size:clamp(10px,.76vw,13px);
  letter-spacing:.1em;text-transform:uppercase;color:var(--mute);margin:6px 0 4px}
.leg i{display:inline-block;width:18px;height:3px;vertical-align:middle;margin-right:8px}
.prem{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1px;background:var(--rule);
  border:1px solid var(--rule);flex:0 1 auto;min-height:0;overflow-y:auto}
.pm{background:var(--ink2);padding:clamp(9px,1.3vh,16px) clamp(12px,1.1vw,20px);display:grid;
  grid-template-columns:minmax(0,1fr) auto;gap:4px 16px;align-items:baseline}
.pm .q{font-size:clamp(12px,.98vw,19px);color:var(--paper);font-weight:600}
.pm .v{font-family:var(--fm);font-size:clamp(12px,.98vw,19px);color:var(--hot);text-align:right;
  font-variant-numeric:tabular-nums;white-space:nowrap}
.pm .s{grid-column:1/-1;font-size:clamp(11px,.84vw,16px);line-height:1.4;color:var(--mute)}
.pm .s b{color:var(--text);font-weight:600}
.tbl{flex:1;min-height:0;overflow:auto;border:1px solid var(--rule)}
.tbl table{border-collapse:collapse;width:100%;font-family:var(--fm);font-size:clamp(10px,.78vw,14px);
  font-variant-numeric:tabular-nums}
.tbl th{position:sticky;top:0;background:var(--ink3);color:var(--mute);font-weight:400;
  letter-spacing:.08em;text-transform:uppercase;text-align:right;padding:8px 10px;white-space:nowrap}
.tbl td{text-align:right;padding:6px 10px;border-top:1px solid var(--rule);color:var(--text);white-space:nowrap}
.tbl th:nth-child(-n+2),.tbl td:nth-child(-n+2){text-align:left}
.tbl .neg{color:var(--hot)} .tbl .pos{color:var(--green)}
.tbl tr.f1r td{color:var(--faint)} .tbl tr.f1r td.neg{color:var(--hot-d)}
.tbl tr.bfr td:nth-child(2){color:var(--hot)}
.quote{border-left:3px solid var(--hot);padding:4px 0 4px clamp(12px,1.2vw,22px);
  font-size:clamp(14px,1.2vw,24px);line-height:1.38;color:var(--paper);margin:0 0 clamp(10px,1.6vh,18px)}
.quote span{display:block;font-family:var(--fm);font-size:clamp(10px,.72vw,13px);letter-spacing:.14em;
  text-transform:uppercase;color:var(--mute);margin-top:6px}
.phase{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--rule);border:1px solid var(--rule)}
.ph{background:var(--ink2);padding:clamp(14px,2.2vh,28px) clamp(14px,1.5vw,28px)}
.ph .m{font-family:var(--fm);font-size:clamp(10px,.78vw,14px);letter-spacing:.16em;text-transform:uppercase;
  color:var(--hot);margin-bottom:10px}
.ph .t{font-family:var(--fd);font-variation-settings:var(--exp);font-weight:800;font-size:clamp(20px,2.1vw,38px);
  color:var(--paper);line-height:1;margin-bottom:12px}
.ph p{margin:0 0 10px;font-size:clamp(13px,1.02vw,20px);line-height:1.42;color:var(--text)}
.ph .who{font-family:var(--fm);font-size:clamp(10px,.76vw,14px);letter-spacing:.1em;color:var(--mute);
  text-transform:uppercase;border-top:1px solid var(--rule);padding-top:10px;margin-top:12px}
@media(max-width:860px){.prem,.phase{grid-template-columns:1fr}}
</style>
"""

# ───────────────────────── slides ─────────────────────────
pior = RB["pior"]
SLIDES = []
def slide(html): SLIDES.append(html)

slide(f"""
<section class="slide">
  <div class="eyebrow">Proposta comercial <b>/</b> Mercado Livre e Amazon Brasil <b>/</b> outubro 2026</div>
  <h1>A Pet Toys dona<br>da <em>própria vitrine</em></h1>
  <p class="sub">Primeiro a marca governa o canal e a rede continua vendendo. Depois, quando vocês
  decidirem, a Pet Toys também vende direto, com a casa já arrumada.</p>
  <div class="figs">
    <div class="fig"><div class="n">2</div><div class="l">canais operados: Mercado Livre e Amazon</div></div>
    <div class="fig"><div class="n hot">2</div><div class="l">fases, a segunda por decisão de vocês</div></div>
    <div class="fig"><div class="n">40</div><div class="l">SKUs na primeira onda de catálogo</div></div>
  </div>
  <div class="kick">Preparado para Luzival Leão, Pet Toys · Grupo Toys
    <div class="small">impulsio · operação de canais digitais para indústrias e distribuidores</div></div>
</section>""")

slide("""
<section class="slide">
  <div class="eyebrow">O ponto de partida <b>/</b> 02</div>
  <h1>O que o diagnóstico<br>já mediu</h1>
  <div class="ev wide">
    <div class="col">
      <p class="sub">O levantamento de 5 de outubro capturou em tela o que o comprador vê hoje, com
      fonte e data em cada número. Esta proposta parte dele.</p>
      <p class="small">Nenhum dado interno da Pet Toys foi usado. O produto não é o problema: um
      revendedor da rede, a Dona Patinha, vende a aranha 5139 com reputação MercadoLíder e mais de mil
      vendas. A rede sabe vender a marca. Falta critério sobre quem a representa.</p>
    </div>
    <div class="col">
      <div class="rows">
        <div class="row"><span>Fichas da marca na Amazon, linha de cães</span><span>15</span></div>
        <div class="row"><span>Títulos sem o nome Pet Toys</span><span class="hot">12 de 15</span></div>
        <div class="row"><span>Fichas sem nenhuma avaliação</span><span class="hot">14 de 15</span></div>
        <div class="row"><span>Fichas com escolha de cor</span><span class="amb">0 de 15</span></div>
        <div class="row"><span>Vendedores na Amazon com critério visível</span><span class="amb">0 de 8</span></div>
        <div class="row"><span>Preço do mesmo Pet Ball, do menor ao maior</span><span class="amb">R$ 8 a R$ 45,99</span></div>
        <div class="row"><span>Loja oficial no Mercado Livre</span><span class="hot">não encontrada</span></div>
      </div>
      <p class="small" style="margin-top:12px">Amazon.com.br e Mercado Livre, capturas de 05/10/2026.</p>
    </div>
  </div>
  <div class="kick">Toda revisão do contrato compara contra esta linha de partida.</div>
</section>""")

slide("""
<section class="slide">
  <div class="eyebrow">O que ouvimos de vocês <b>/</b> 03</div>
  <h1>Três pontos da conversa<br>que desenham <em>a proposta</em></h1>
  <div class="ev">
    <div class="col">
      <div class="quote">A dificuldade não é vender. É ter gente para operar o canal de ponta a ponta.
        <span>Estrutura</span></div>
      <div class="quote">A estratégia hoje é abastecer a rede, que já vende nos marketplaces, inclusive
        um parceiro que opera de dentro da sede.<span>Relação com a rede</span></div>
      <div class="quote">Se o trabalho de organizar for feito, faz sentido a Pet Toys também vender,
        com o estoque indo para o centro de distribuição do marketplace.<span>Venda direta</span></div>
    </div>
    <div class="col">
      <h2>Como isso vira desenho</h2>
      <div class="rows">
        <div class="row"><span>Falta de time interno</span><span>a impulsio opera</span></div>
        <div class="row"><span>Rede que já vende</span><span>Fase 1 protege</span></div>
        <div class="row"><span>Vontade de vender direto</span><span>Fase 2 libera</span></div>
        <div class="row"><span>Linha de alimento nova</span><span>entra na onda 1</span></div>
        <div class="row"><span>Estúdio próprio de foto e vídeo</span><span>vira insumo</span></div>
      </div>
      <p class="small" style="margin-top:12px">A venda direta não começa no primeiro dia. Abrir uma loja
      que disputa com a rede antes de ter critério de canal cria o conflito que vocês querem evitar.</p>
    </div>
  </div>
  <div class="kick">Organizar antes de vender. A ordem é o que protege quem já compra de vocês.</div>
</section>""")

slide(f"""
<section class="slide">
  <div class="eyebrow">O modelo <b>/</b> 04</div>
  <h1>Duas fases,<br>uma decisão <em>no meio</em></h1>
  <div class="phase">
    <div class="ph"><div class="m">Fase 1 · meses 1 a 3 · nov/26 a jan/27</div>
      <div class="t">Marca Protagonista</div>
      <p>A Pet Toys passa a ser dona da ficha: título, cor, foto, vídeo e atributos que todos os
      vendedores usam. A rede credenciada continua vendendo, com estoque e preço próprios.</p>
      <p>Registro da marca nos dois canais, loja oficial no Mercado Livre, Brand Store na Amazon e
      critério de credenciamento da rede.</p>
      <div class="who">Quem vende: a rede credenciada</div></div>
    <div class="ph"><div class="m">Fase 2 · a partir do mês 4 · fev/27</div>
      <div class="t">Protagonista + venda direta</div>
      <p>A loja oficial também vende, com estoque da Pet Toys no Full do Mercado Livre. A rede segue
      vendendo nas mesmas fichas, agora padronizadas.</p>
      <p>Planejamento de envio ao Full, mídia paga a partir do terceiro mês de venda e lançamento
      digital da linha de alimento.</p>
      <div class="who">Quem vende: a rede e a Pet Toys, lado a lado</div></div>
  </div>
  <p class="small" style="margin-top:clamp(12px,2vh,20px)">A Fase 2 depende de aprovação interna de
  vocês. Se ela não vier, o contrato segue na Fase 1 com o mesmo fixo e sem nenhum variável. Na
  Amazon, o modelo em que ela compra da fábrica e revende (1P) fica como próximo horizonte: a ficha
  sai pronta desta fase para quando a negociação avançar.</p>
  <div class="kick">Variável só existe onde a operação realiza a venda. Na Fase 1, quem vende é a rede.</div>
</section>""")

slide("""
<section class="slide">
  <div class="eyebrow">O que a impulsio executa <b>/</b> 05</div>
  <h1>O escopo,<br>frente por frente</h1>
  <div class="tiles">
    <div class="tile"><div class="k">01 · Governança de marca</div><div class="t">Quem representa a Pet Toys</div>
      <div class="l">Registro da marca no Mercado Livre e Brand Registry na Amazon, critério de credenciamento
      da rede, monitoramento de vendedores e denúncia pelas ferramentas oficiais de anúncios que usam a
      marca sem ser da fábrica.</div></div>
    <div class="tile"><div class="k">02 · Catálogo e conteúdo</div><div class="t">Uma ficha por produto</div>
      <div class="l">Título com a marca, variação de cor numa ficha só, atributos de filtro, categoria
      certa, vídeo, conteúdo A+ na Amazon e loja oficial com vitrine por linha.</div></div>
    <div class="tile"><div class="k">03 · Arquitetura de canais</div><div class="t">O papel de cada canal</div>
      <div class="l">Sortimento por canal, diretriz de posicionamento de preço, planejamento de estoque no
      Full e preparação da ficha para o modelo 1P da Amazon.</div></div>
    <div class="tile"><div class="k">04 · Mídia, na Fase 2</div><div class="t">Depois da ficha pronta</div>
      <div class="l">Mercado Ads e Sponsored Products a partir do terceiro mês de venda direta. A verba
      é paga por vocês direto à plataforma.</div></div>
  </div>
  <div class="kick">Tráfego pago para ficha sem a marca no título e sem cor vira desconto, não venda. Por isso a mídia vem por último.</div>
</section>""")

slide("""
<section class="slide">
  <div class="eyebrow">Catálogo em ondas <b>/</b> 06</div>
  <h1>Quarenta primeiro.<br><em>O resto em ondas.</em></h1>
  <div class="ev">
    <div class="col">
      <h2>Onda 1, dentro do setup</h2>
      <div class="rows">
        <div class="row"><span>SKUs da curva A de brinquedos e comedouros</span><span>definidos com vocês</span></div>
        <div class="row"><span>Linha de alimento, lançada há 45 dias</span><span>incluída</span></div>
        <div class="row"><span>As 15 fichas atuais da Amazon</span><span>corrigidas</span></div>
        <div class="row"><span>Total da onda 1</span><span class="grn">40 SKUs</span></div>
        <div class="row"><span>Publicação</span><span class="mut">meses 1 a 3</span></div>
      </div>
    </div>
    <div class="col">
      <h2>Ondas seguintes</h2>
      <div class="rows">
        <div class="row"><span>SKU novo</span><span>R$ 90 por SKU, por canal</span></div>
        <div class="row"><span>Correção de ficha existente</span><span>R$ 60 por SKU, por canal</span></div>
        <div class="row"><span>Tamanho e ordem da onda</span><span class="mut">vocês decidem</span></div>
      </div>
      <p class="small" style="margin-top:14px">O catálogo da linha pet tem cerca de 50 brinquedos para
      cães, comedouros, bebedouros e seis linhas para gatos. Subir tudo de uma vez produz fichas
      medianas. Em ondas, cada uma sai no padrão e a seguinte aproveita o que a anterior ensinou.</p>
    </div>
  </div>
  <div class="kick">Onda nova só começa com a anterior publicada. Catálogo meio corrigido não sustenta o seguinte.</div>
</section>""")

slide("""
<section class="slide">
  <div class="eyebrow">Como o trabalho anda <b>/</b> 07</div>
  <h1>Do kickoff à<br>venda direta</h1>
  <div class="timeline">
    <div class="tl"><div class="m">Nov/26 · mês 1</div><div class="t">Fundação</div>
      <ul><li>Registro da marca nos canais</li><li>Padrão de ficha e de título</li><li>Seleção dos 40 SKUs</li><li>Critério da rede</li></ul></div>
    <div class="tl"><div class="m">Dez/26 a jan/27</div><div class="t">Onda 1 no ar</div>
      <ul><li>Loja oficial e Brand Store</li><li>40 fichas publicadas</li><li>Cor como variação</li><li>Rede credenciada</li></ul></div>
    <div class="tl"><div class="m">Fev/27 · mês 4</div><div class="t">Venda direta</div>
      <ul><li>Primeiro envio ao Full</li><li>Loja oficial vendendo</li><li>Linha de alimento no ar</li></ul></div>
    <div class="tl"><div class="m">Abr/27 em diante</div><div class="t">Escala</div>
      <ul><li>Mídia paga</li><li>Ondas seguintes de catálogo</li><li>Ficha pronta para o 1P</li></ul></div>
  </div>
  <p class="small" style="margin-top:clamp(12px,2vh,20px)">Novembro é o pico de vocês. Por isso o mês 1 é
  de fundação, que pede decisão e informação, não operação de pedido. O prazo de cada entrega corre a
  partir do recebimento do insumo; se um material atrasar, a entrega desloca o mesmo número de dias, com
  aviso por escrito no momento em que o atraso aparece.</p>
  <div class="kick">A Black Friday de 2027 é a primeira em que a Pet Toys vende direto, com catálogo e histórico já formados.</div>
</section>""")

slide("""
<section class="slide">
  <div class="eyebrow">O que não está incluído <b>/</b> 08</div>
  <h1>E dizemos isso<br><em>antes</em> de vocês perguntarem</h1>
  <div class="no">
    <div><b>Preço de revenda</b>A rede define o próprio preço. A impulsio monitora e orienta posicionamento; não impõe preço a terceiro, porque impor preço de revenda com punição é infração à ordem econômica.</div>
    <div><b>Logística e faturamento</b>Separação, nota fiscal e envio ao Full ficam com a Pet Toys. Nós entregamos o plano de envio por SKU; a expedição é de vocês.</div>
    <div><b>Verba de mídia</b>O investimento em anúncios é pago por vocês direto à plataforma, fora deste contrato.</div>
    <div><b>Negociação 1P com a Amazon</b>Pedido, preço de compra e prazo são relação direta de vocês com a Amazon. Preparamos a ficha e o sortimento.</div>
    <div><b>Assunto jurídico de marca</b>Registro no INPI, contrafação e notificação são do jurídico da Pet Toys. A impulsio atua na operação, pelas ferramentas oficiais dos canais.</div>
    <div><b>SAC e devolução</b>Atendimento ao comprador da venda direta segue com vocês, com roteiro de respostas preparado por nós.</div>
  </div>
  <div class="kick">Escopo que não está escrito vira discussão no mês quatro. Preferimos ter essa conversa agora.</div>
</section>""")

slide("""
<section class="slide">
  <div class="eyebrow">Como o trabalho é medido <b>/</b> 09</div>
  <h1>Pelo que a operação<br>controla</h1>
  <div class="ev">
    <div class="col">
      <h2>Os indicadores do contrato</h2>
      <div class="rows">
        <div class="row"><span>Fichas com Pet Toys no título</span><span>3 de 15 &rarr; 40 de 40</span></div>
        <div class="row"><span>Fichas com escolha de cor</span><span>0 &rarr; todas com variação</span></div>
        <div class="row"><span>Loja oficial e Brand Store</span><span>nenhuma &rarr; as duas no ar</span></div>
        <div class="row"><span>Vendedores credenciados</span><span>0 de 8 &rarr; critério publicado</span></div>
        <div class="row"><span>Dispersão de preço por SKU</span><span>medida todo mês</span></div>
        <div class="row"><span>Ruptura nas fichas da onda 1</span><span>medida todo mês</span></div>
      </div>
    </div>
    <div class="col">
      <h2>O que não prometemos</h2>
      <p class="sub"><strong>Meta de faturamento.</strong> Faturamento depende de preço, estoque e
      decisões que são de vocês e da plataforma.</p>
      <p class="small">A projeção das páginas seguintes é uma simulação com premissas abertas, feita
      para vocês avaliarem o investimento. Não é meta e não é compromisso de resultado.</p>
    </div>
  </div>
  <div class="kick">É mais fácil vender promessa de faturamento. Preferimos vender o que dá para conferir na tela.</div>
</section>""")

slide(f"""
<section class="slide">
  <div class="eyebrow">O investimento <b>/</b> 10</div>
  <h1>Seis mil por mês<br>no primeiro semestre</h1>
  <div class="price">
    <div class="pc">
      <div class="k">Meses 1 a 6</div>
      <div class="v">R$ 6.000<small> /mês</small></div>
      <div class="d">Setup de R$ 15.000 em 6 parcelas de R$ 2.500, mais operação mensal de R$ 3.500.
      O setup cobre a fundação de marca nos dois canais, o padrão de ficha e a onda 1 de 40 SKUs.</div>
    </div>
    <div class="pc">
      <div class="k">Mês 7 em diante</div>
      <div class="v">R$ 6.200<small> /mês</small></div>
      <div class="d">Mercado Livre R$ 4.500 mais Amazon R$ 1.700. Operação contínua de catálogo,
      governança, arquitetura de canal e, na Fase 2, gestão da venda direta e da mídia.</div>
    </div>
  </div>
  <div class="rows" style="margin-top:clamp(12px,2vh,22px)">
    <div class="row"><span>Variável, só na Fase 2, sobre a venda direta</span><span>2% do que passar de R$ 150 mil/mês</span></div>
    <div class="row"><span>Exemplo: mês com R$ 180 mil de venda direta</span><span>2% × R$ 30 mil = R$ 600</span></div>
    <div class="row"><span>Base de cálculo</span><span class="mut">relatório da conta da Pet Toys</span></div>
    <div class="row"><span>Ondas adicionais de catálogo</span><span class="mut">R$ 90 SKU novo · R$ 60 correção · por canal</span></div>
  </div>
  <p class="small" style="margin-top:12px">Até R$ 150 mil por mês de venda direta não há variável. A venda
  da rede nunca entra na conta. A venda direta parte do zero, então a base é zero, e isso fica escrito no contrato.</p>
  <div class="kick">O variável só começa quando a operação já passou de R$ 150 mil por mês. Antes disso, o fixo paga o trabalho.</div>
</section>""")

slide("""
<section class="slide">
  <div class="eyebrow">O mercado <b>/</b> 11</div>
  <h1>O tamanho<br>da <em>prateleira</em></h1>
  <div class="ev wide">
    <div class="col">
      <div class="figs">
        <div class="fig"><div class="n">R$ 16<small> mi</small></div><div class="l">por mês, brinquedos, comedouros e bebedouros de cães e gatos</div></div>
      </div>
      <p class="sub" style="margin-top:clamp(14px,2.4vh,26px)">Comedouros e bebedouros crescem mais rápido
      que brinquedos: <strong>+77%</strong> em um ano para cães e <strong>+93%</strong> para gatos.
      É a linha do comedouro alto, que um revendedor já vende em quatro cores numa ficha só.</p>
      <p class="small">Hoje o campo de marca PETTOYS soma cerca de R$ 7 mil/mês em 338 anúncios e 88
      vendedores, só 9 com venda. Parte desses anúncios nem é da fábrica, porque "pet toys" é também
      um termo genérico.</p>
    </div>
    <div class="col">
      <div class="rows">
        <div class="row"><span>Brinquedos para cães</span><span>R$ 3,4 mi · +29%</span></div>
        <div class="row"><span>Brinquedos para gatos</span><span>R$ 1,5 mi · −5%</span></div>
        <div class="row"><span>Comedouros e bebedouros, cães</span><span>R$ 7,2 mi · +77%</span></div>
        <div class="row"><span>Comedouros e bebedouros, gatos</span><span>R$ 3,9 mi · +93%</span></div>
        <div class="row"><span>5ª maior marca em brinquedos para cães</span><span class="amb">≈ R$ 87 mil/mês</span></div>
        <div class="row"><span>5ª maior marca em comedouros para cães</span><span class="amb">≈ R$ 82 mil/mês</span></div>
      </div>
      <p class="small" style="margin-top:12px">Estimativas JoomPulse sobre dados públicos do Mercado Livre,
      setembro de 2026, variação contra setembro de 2025. Servem para dimensionar a prateleira, não são
      faturamento auditado.</p>
    </div>
  </div>
  <div class="kick">Os R$ 200 mil da projeção equivalem a 1,2% dessa prateleira, o patamar de uma marca entre as cinco maiores em brinquedos e em comedouros ao mesmo tempo.</div>
</section>""")

slide(f"""
<section class="slide">
  <div class="eyebrow">A projeção · premissas <b>/</b> 12</div>
  <h1>De onde vem<br><em>cada número</em></h1>
  <div class="prem">
    <div class="pm"><div class="q">Início do contrato</div><div class="v">nov/2026</div>
      <div class="s">Mês 1 é a assinatura. Venda direta só a partir do <b>mês 4 (fev/27)</b>; os três primeiros meses são Fase 1, sem venda direta na conta.</div></div>
    <div class="pm"><div class="q">Potencial da venda direta em regime</div><div class="v">R$ 200 mil/mês</div>
      <div class="s">Premissa alinhada na conversa: 1,2% da prateleira de R$ 16 mi da página 11. Corresponde à operação madura, no <b>mês 20 (jun/28)</b>. Cenário alternativo com R$ 150 mil na página 15.</div></div>
    <div class="pm"><div class="q">Margem sobre a venda</div><div class="v">20%</div>
      <div class="s">Margem da Pet Toys já descontados comissão do marketplace, frete e imposto. Faixa informada por vocês: <b>15% a 20%</b>. O conservador usa 15%.</div></div>
    <div class="pm"><div class="q">Maturação do canal</div><div class="v">18 meses até 100%</div>
      <div class="s">Rampa padrão de canal novo com catálogo novo: 2% do potencial no 1º mês de venda, 48% no 8º, 100% no 17º. Histórico e avaliações levam tempo.</div></div>
    <div class="pm"><div class="q">Sazonalidade</div><div class="v">varejo pet</div>
      <div class="s">Consumo recorrente, picos suaves: fevereiro a 0,86 do mês médio, <b>novembro a 1,18</b> (Black Friday), dezembro a 1,12.</div></div>
    <div class="pm"><div class="q">Mídia paga</div><div class="v">3% do GMV</div>
      <div class="s">A partir do 3º mês de venda direta (abr/27), com verba mínima de R$ 1.000/mês até o 6º. Paga à plataforma, fora do contrato.</div></div>
    <div class="pm"><div class="q">Contrato impulsio</div><div class="v">R$ 6.000 → R$ 6.200</div>
      <div class="s">R$ 2.500 de setup + R$ 3.500 de operação nos meses 1 a 6; R$ 6.200 do mês 7 em diante; 2% sobre o excedente de R$ 150 mil.</div></div>
    <div class="pm"><div class="q">Horizonte</div><div class="v">25 meses</div>
      <div class="s">Novembro de 2026 a novembro de 2028, passando por <b>duas Black Fridays</b> de venda direta.</div></div>
  </div>
  <div class="kick">Todas as premissas são editáveis na planilha que acompanha esta proposta. Troquem pelos números de vocês.</div>
</section>""")

slide(f"""
<section class="slide">
  <div class="eyebrow">A projeção · resultado acumulado <b>/</b> 13</div>
  <h1>O investimento se paga<br>em <em>{longo(RB['payback'])}</em></h1>
  <div class="leg"><span><i style="background:var(--seal-l)"></i>resultado acumulado da venda direta, depois do contrato e da mídia</span></div>
  {graf_acumulado()}
  <div class="figs" style="margin-top:clamp(8px,1.4vh,16px)">
    <div class="fig"><div class="n hot" style="font-size:clamp(28px,3.6vw,64px)">{k(pior['acum'])}</div><div class="l">pior momento do caixa · {pior['rot']}</div></div>
    <div class="fig"><div class="n" style="font-size:clamp(28px,3.6vw,64px)">{RB['payback']}</div><div class="l">acumulado volta ao positivo</div></div>
    <div class="fig"><div class="n" style="font-size:clamp(28px,3.6vw,64px)">{k(RB['fim'])}</div><div class="l">acumulado em nov/28, 25 meses</div></div>
  </div>
  <div class="kick">Resultado = margem de 20% sobre a venda direta, menos mídia, menos contrato impulsio. A venda da rede não entra.</div>
</section>""")

slide(f"""
<section class="slide">
  <div class="eyebrow">A projeção · venda direta mês a mês <b>/</b> 14</div>
  <h1>A curva de<br>venda direta</h1>
  <div class="leg"><span><i style="background:var(--seal)"></i>venda direta projetada (GMV)</span><span><i style="background:var(--hot)"></i>novembro · Black Friday</span><span><i style="background:var(--amber)"></i>gatilho do variável</span></div>
  {graf_gmv()}
  <div class="kick">Pela premissa, a venda direta cruza R$ 150 mil na Black Friday de 2027. Só a partir daí existe variável, e só sobre o excedente.</div>
</section>""")

cb, cp, cc = R["base"], R["pot"], R["cons"]
slide(f"""
<section class="slide">
  <div class="eyebrow">A projeção · cenários <b>/</b> 15</div>
  <h1>Se as premissas<br><em>não se confirmarem</em></h1>
  <div class="ev wide">
    <div class="col">
      <div class="leg"><span><i style="background:var(--seal-l)"></i>base</span><span><i style="background:var(--amber)"></i>potencial R$ 150 mil</span><span><i style="background:var(--hot)"></i>conservador</span></div>
      {graf_cenarios()}
    </div>
    <div class="col">
      <div class="rows">
        <div class="row"><span><b style="color:var(--paper)">Base</b> · R$ 200 mil, 20%, 18 meses</span><span></span></div>
        <div class="row"><span>pior caixa · paga em</span><span>{k(cb['pior']['acum'])} · {cb['payback']}</span></div>
        <div class="row"><span>acumulado em 25 meses</span><span class="grn">{k(cb['fim'])}</span></div>
        <div class="row"><span><b style="color:var(--paper)">Potencial menor</b> · R$ 150 mil</span><span></span></div>
        <div class="row"><span>pior caixa · paga em</span><span>{k(cp['pior']['acum'])} · {cp['payback']}</span></div>
        <div class="row"><span>acumulado em 25 meses</span><span class="grn">{k(cp['fim'])}</span></div>
        <div class="row"><span><b style="color:var(--paper)">Conservador</b> · margem 15%, rampa 1,5× mais lenta</span><span></span></div>
        <div class="row"><span>pior caixa · paga em</span><span>{k(cc['pior']['acum'])} · {cc['payback']}</span></div>
        <div class="row"><span>acumulado em 25 meses</span><span class="grn">{k(cc['fim'])}</span></div>
      </div>
    </div>
  </div>
  <div class="kick">Mesmo no conservador o investimento volta dentro do horizonte. O que muda é quanto tempo o caixa fica negativo.</div>
</section>""")

slide(f"""
<section class="slide">
  <div class="eyebrow">A projeção · o que fica de fora <b>/</b> 16</div>
  <h1>A conta é<br><em>conservadora</em> de propósito</h1>
  <div class="ev">
    <div class="col">
      <h2>Não entra na projeção</h2>
      <div class="rows">
        <div class="row"><span>Venda da rede depois da Fase 1</span><span class="mut">fichas melhores, mais giro</span></div>
        <div class="row"><span>Pedidos da Amazon no modelo 1P</span><span class="mut">quando a negociação avançar</span></div>
        <div class="row"><span>Recorrência da linha de alimento</span><span class="mut">Programe e Poupe na Amazon</span></div>
        <div class="row"><span>Shopee e TikTok Shop</span><span class="mut">fase futura</span></div>
      </div>
    </div>
    <div class="col">
      <h2>Por que deixar de fora</h2>
      <p class="sub">A projeção conta só o que a venda direta gera para a Pet Toys. O efeito na rede é real,
      mas aparece como pedido de revendedor, e misturar as duas coisas inflaria o número.</p>
      <p class="small">O potencial de R$ 200 mil é premissa, não medição. Os valores de mercado do
      diagnóstico são estimativas de plataforma e não servem de base para cobrança.</p>
    </div>
  </div>
  <div class="kick">Se algo der certo fora desta conta, ele aparece no pedido da rede e no da Amazon, não nesta curva.</div>
</section>""")

slide(f"""
<section class="slide">
  <div class="eyebrow">A projeção · mês a mês <b>/</b> 17</div>
  <h1>A tabela<br>completa</h1>
  <div class="tbl"><table>
    <thead><tr><th>Mês</th><th></th><th>Venda direta</th><th>Margem 20%</th><th>Mídia</th><th>impulsio fixo</th><th>Variável</th><th>Resultado</th><th>Acumulado</th></tr></thead>
    <tbody>{tabela_mensal()}</tbody>
  </table></div>
  <div class="kick" style="font-size:clamp(12px,1.1vw,22px)">Meses 1 a 3 em cinza: Fase 1, sem venda direta na conta. O mesmo modelo está na planilha editável.</div>
</section>""")

slide("""
<section class="slide">
  <div class="eyebrow">O que precisamos de vocês <b>/</b> 18</div>
  <h1>O que destrava<br>cada entrega</h1>
  <div class="ev">
    <div class="col">
      <div class="rows">
        <div class="row"><span>Acesso às contas de Mercado Livre e Amazon</span><span class="mut">semana 1</span></div>
        <div class="row"><span>Situação da marca no INPI</span><span class="mut">semana 1</span></div>
        <div class="row"><span>Planilha de produtos do ERP, com medidas e EAN</span><span class="mut">semana 1</span></div>
        <div class="row"><span>Lista de revendedores atuais da rede</span><span class="mut">mês 1</span></div>
        <div class="row"><span>Registro MAPA da linha de alimento</span><span class="mut">mês 1</span></div>
        <div class="row"><span>Fotos e vídeos do estúdio interno, por briefing</span><span class="mut">por onda</span></div>
        <div class="row"><span>Aprovação interna da Fase 2</span><span class="mut">até jan/27</span></div>
      </div>
    </div>
    <div class="col">
      <h2>Parada de relógio</h2>
      <p class="sub">O prazo de cada entrega corre <strong>a partir do recebimento do insumo</strong>, não da data do contrato.</p>
      <p class="small">A situação no INPI é a que mais trava: registro de marca no Mercado Livre e Brand
      Registry na Amazon dependem dela. Com "Pet Toys" sendo também o nome da categoria em inglês, vale
      confirmar se o registro cobre o nome ou o logotipo.</p>
      <p class="small" style="margin-top:12px">O estúdio de vocês é vantagem real: o conteúdo sai com a
      cara da fábrica, sem custo de produção externa. Nós entregamos o briefing de cada imagem e vídeo a
      partir do que funciona na categoria.</p>
    </div>
  </div>
  <div class="kick">A conta, o registro, as fichas e o conteúdo são da Pet Toys, durante o contrato e depois dele.</div>
</section>""")

slide("""
<section class="slide">
  <div class="eyebrow">O próximo passo <b>/</b> 19</div>
  <h1>Quatro movimentos<br>para começar em novembro</h1>
  <div class="tiles">
    <div class="tile"><div class="k">01</div><div class="t">Validação interna</div>
      <div class="l">Vocês levam esta proposta e a planilha para a diretoria. Ajustamos premissas juntos, se precisar.</div></div>
    <div class="tile"><div class="k">02</div><div class="t">Aceite</div>
      <div class="l">Assinatura e primeira parcela do setup.</div></div>
    <div class="tile"><div class="k">03</div><div class="t">Kickoff</div>
      <div class="l">Em até 48 horas do aceite, com acessos e planilha do ERP.</div></div>
    <div class="tile"><div class="k">04</div><div class="t">Seleção da onda 1</div>
      <div class="l">Os 40 SKUs, escolhidos com vocês a partir da curva de venda.</div></div>
  </div>
  <div class="kick">impulsio · operação de canais digitais para indústrias e distribuidores
    <div class="small">Proposta válida por 30 dias · outubro de 2026</div></div>
</section>""")

# ───────────────────────── montagem ─────────────────────────
head = (AQUI / "proposta" / "_head.html").read_text()
head = head.replace("<title>Proposta StillPet Amazon</title>", "<title>Proposta Pet Toys</title>")
tail = (AQUI / "proposta" / "_tail.html").read_text()
tail = tail.replace("<em>01</em> / 11", f"<em>01</em> / {len(SLIDES):02d}")
html = head + CSS + '\n<div class="topbar"><i id="fill"></i></div>\n<div class="deck" id="deck">\n' \
       + "\n".join(SLIDES) + "\n\n</div>\n" + tail
SAIDA.write_text(html)
print(f"{SAIDA} · {len(SLIDES)} slides · payback {RB['payback']} · pior {brl(pior['acum'])} em {pior['rot']}")
for c, r in R.items():
    print(c, r["payback"], brl(r["pior"]["acum"]), brl(r["fim"]))
