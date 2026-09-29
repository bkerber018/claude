import re, glob, os

FONTE = ("[Fontes] Evidências coletadas em amazon.com.br entre 22 e 23/09/2026 "
         "(prints de tela arquivados). Catálogo de 151 anúncios sob a marca Tudo Pet, "
         "verificado por busca de marca na Amazon Brasil. Escopo, prazos e valores "
         "conforme alinhado em reunião com a Still Pet. Nenhum número neste documento "
         "é estimativa: cada dado tem print datado. [/Fontes]")

total = 0
for f in sorted(glob.glob("un/ppt/notesSlides/notesSlide*.xml"),
                key=lambda p: int(re.search(r'(\d+)\.xml', p).group(1))):
    x = open(f, encoding="utf-8").read()
    n = [0]
    def sub(m):
        n[0] += 1
        return "<a:t>%s</a:t>" % (FONTE if n[0] == 1 else "")
    y = re.sub(r'<a:t>.*?</a:t>', sub, x, flags=re.S)
    open(f, "w", encoding="utf-8").write(y)
    total += n[0]
    print(f"  {os.path.basename(f)}: {n[0]} runs zerados")
print("total:", total)
