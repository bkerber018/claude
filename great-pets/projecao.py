"""Projeção Great Pets — venda direta (conta Seller GREAT PETS, sortimento próprio) na Amazon BR.
Simulação para avaliar o investimento; não é meta de faturamento."""
import json, sys

MESES = ["nov/26","dez/26"] + [f"{m}/27" for m in "jan fev mar abr mai jun jul ago set out nov dez".split()] \
      + [f"{m}/28" for m in "jan fev mar abr mai jun jul ago set out nov".split()]
SAZ = {"jan":0.95,"fev":0.86,"mar":0.98,"abr":0.96,"mai":1.00,"jun":0.95,
       "jul":1.00,"ago":1.03,"set":1.00,"out":1.06,"nov":1.18,"dez":1.12}
MAT = [0.02,0.04,0.08,0.13,0.20,0.29,0.38,0.48,0.58,0.67,0.75,0.82,0.88,0.93,0.96,0.98,1.00]

INICIO_VENDA = 3          # índice de fev/27
SETUP, PARCELAS = 16000, 10
GATILHO, PCT_VAR = 50000, 0.02

def mat(k, lento=1.0):
    i = k / lento
    if i >= len(MAT) - 1: return 1.0
    lo = int(i); f = i - lo
    return MAT[lo] + (MAT[lo+1] - MAT[lo]) * f

def roda(potencial=150000, margem=0.20, lento=1.0):
    linhas, acum = [], 0
    for i, mes in enumerate(MESES):
        k = i - INICIO_VENDA
        gmv = round(potencial * mat(k, lento) * SAZ[mes[:3]]) if k >= 0 else 0
        midia = 0
        if i >= 5:                     # a partir de abr/27
            midia = 0.03 * gmv
            if i <= 8: midia = max(midia, 1000)   # mínimo até jul/27
        mensal = 4000 if i < 2 else 6000
        setup = SETUP / PARCELAS if i < PARCELAS else 0
        var = PCT_VAR * (gmv - GATILHO) if gmv > GATILHO else 0
        imp = mensal + setup + var
        res = margem * gmv - midia - imp
        acum += res
        linhas.append(dict(mes=mes, gmv=gmv, margem=margem*gmv, midia=midia, setup=setup,
                           mensal=mensal, var=var, impulsio=imp, resultado=res, acumulado=acum))
    return linhas

def resumo(l):
    pior = min(l, key=lambda r: r["acumulado"])
    paga = next((r["mes"] for r in l if r["mes"] != pior["mes"] and l.index(r) > l.index(pior) and r["acumulado"] >= 0), None)
    cruza = next((r["mes"] for r in l if r["gmv"] > GATILHO), None)
    return dict(pior=round(pior["acumulado"]), pior_mes=pior["mes"], paga=paga,
                final=round(l[-1]["acumulado"]), cruza_gatilho=cruza,
                var_total=round(sum(r["var"] for r in l)), gmv_nov28=l[-1]["gmv"])

if __name__ == "__main__":
    cen = {"base": roda(), "menor": roda(potencial=100000), "conservador": roda(margem=0.15, lento=1.5)}
    for n, l in cen.items(): print(n, resumo(l))
    print()
    for r in cen["base"]:
        print(f'{r["mes"]:7} gmv {r["gmv"]:>8,.0f}  marg {r["margem"]:>7,.0f}  midia {r["midia"]:>6,.0f}  imp {r["impulsio"]:>7,.0f} (var {r["var"]:>5,.0f})  res {r["resultado"]:>8,.0f}  acum {r["acumulado"]:>9,.0f}')
    json.dump({n: l for n, l in cen.items()}, open(sys.argv[1] if len(sys.argv) > 1 else "projecao.json", "w"), ensure_ascii=False, indent=1)
