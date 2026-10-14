"""Motor da projeção — réplica fiel do simulador do Impulsio Proposal Hub (Lovable)."""
MES=['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez']
SAZ_PET=[.88,.86,1.00,.98,1.02,.95,1.00,1.03,1.00,1.06,1.18,1.12]
MAT_PADRAO=[0,2,4,8,13,20,28,38,48,58,65,74,81,86,90,94,97,100]

def motor(pot,marg,adsP,adsIni,piso,pisoAte,setup,parc,mens,varP,gat,mIni,aIni,n,mat,saz=SAZ_PET,exc=True):
    """mens: função(mês)->mensalidade. mat: lista de maturação (0-1) por mês."""
    L=[];acum=0
    for k in range(n):
        idx=(mIni+k)%12; ano=aIni+(mIni+k)//12; mm=k+1
        m=mat[k] if k<len(mat) else 1
        gmv=round(pot*m*saz[idx]/500)*500
        margem=gmv*marg
        ads=0 if (mm<adsIni or gmv==0) else (max(gmv*adsP,piso) if mm<=pisoAte else gmv*adsP)
        st=setup/parc if mm<=parc else 0
        men=mens(mm)
        vr=((gmv-gat)*varP if exc else gmv*varP) if gmv>gat else 0
        imp=st+men+vr; res=margem-ads-imp; acum+=res
        L.append(dict(n=mm,rot=f"{MES[idx]}/{str(ano)[2:]}",gmv=gmv,margem=margem,ads=ads,setup=st,mens=men,var=vr,imp=imp,res=res,acum=acum,mat=m,saz=saz[idx]))
    return L
def payback(L):
    for r in L:
        if r['acum']>0: return r['rot']
    return None
