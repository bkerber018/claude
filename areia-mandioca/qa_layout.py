#!/usr/bin/env python3
"""QA geometrico de .pptx sem renderizador.

Uso: python3 qa_layout.py arquivo.pptx [outro.pptx ...]

Verifica forma fora do palco, estouro estimado de texto e sobreposicao de
caixas de texto. Nao substitui olhar o arquivo -- so garante que nada esta
cortado. Requer python-pptx.
"""
import sys
from pptx import Presentation
from pptx.util import Emu

EMU_IN = 914400
# largura media de caractere como fracao do corpo da fonte, para as fontes do padrao
CHAR_W = 0.52
LINE_H = 1.22          # altura de linha como multiplo do corpo
TOL = 0.02             # tolerancia em polegadas


def inches(v):
    return None if v is None else v / EMU_IN


def text_of(shape):
    if not shape.has_text_frame:
        return "", None
    tf = shape.text_frame
    txt = tf.text
    size = None
    for p in tf.paragraphs:
        for r in p.runs:
            if r.font.size is not None:
                size = r.font.size.pt
                break
        if size:
            break
    return txt, size


def check(path):
    prs = Presentation(path)
    pw, ph = inches(prs.slide_width), inches(prs.slide_height)
    issues = []
    for idx, slide in enumerate(prs.slides, 1):
        boxes = []
        for shape in slide.shapes:
            if shape.left is None or shape.top is None:
                continue
            x, y = inches(shape.left), inches(shape.top)
            w = inches(shape.width) or 0
            h = inches(shape.height) or 0
            name = shape.shape_type

            if x < -TOL or y < -TOL or x + w > pw + TOL or y + h > ph + TOL:
                issues.append((idx, "fora do palco",
                               f"{name} em ({x:.2f},{y:.2f}) {w:.2f}x{h:.2f}"))

            txt, size = text_of(shape)
            if txt.strip() and size and w > 0:
                per_line = max(int(w / (size * CHAR_W / 72)), 1)
                lines = 0
                for para in txt.split("\n"):
                    lines += max(-(-len(para) // per_line), 1)
                need = lines * size * LINE_H / 72
                if need > h + TOL:
                    issues.append((idx, "texto estoura",
                                   f'"{txt[:42]}..." precisa ~{need:.2f}in, caixa tem {h:.2f}in'))
                # Para sobreposicao, use a extensao REAL do texto, nao a altura
                # declarada: caixa folgada com uma linha de texto nao colide com
                # o que esta abaixo dela, e contar a caixa gera falso positivo.
                boxes.append((x, y, w, min(need, h) if need else h, txt[:28]))

        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                a, b = boxes[i], boxes[j]
                ox = min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0])
                oy = min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1])
                if ox > TOL and oy > TOL:
                    issues.append((idx, "sobreposicao",
                                   f'"{a[4]}" x "{b[4]}" ({ox:.2f}x{oy:.2f}in)'))

    print(f"\n=== {path}  ({len(prs.slides.__iter__.__self__._sldIdLst)} slides, "
          f"{pw:.2f}x{ph:.2f}in)")
    if not issues:
        print("  OK - nenhum problema geometrico.")
    else:
        for n, kind, detail in issues:
            print(f"  slide {n:>2}  [{kind}]  {detail}")
        print(f"  -> {len(issues)} problema(s).")
    print("  Validacao geometrica, nao visual. Abra o arquivo antes de apresentar.")
    return len(issues)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    total = sum(check(p) for p in sys.argv[1:])
    sys.exit(1 if total else 0)
