/* Componentes do padrão Marca Protagonista para pptxgenjs.
 * Uso:  const D = require("./deck.js");  const pres = D.novo("Título");
 * Copie assets/bg_dark.png e assets/bg_blue.png para o diretório de trabalho. */
const pptxgen = require("pptxgenjs");

const BLUE = "3B82F6", BLUE_L = "6EA8FF", BLUE_PALE = "A8C8FF",
      BLUE_SUB = "C9D8FF", BLUE_NUM = "8FB8FF", BLUE_DK = "244C86";
const T_H1 = "F3F5FA", T_SUB = "EFEFEF", T_BODY = "F3F3F3", T_KICK = "E9EBF2",
      T_ITEM = "DBE3F5", T_DIM = "8B93A4", T_PAGE = "7C8494", T_SRC = "5C6375";
const WHITE = "FFFFFF", AMBER = "F0A23B";
const FH = "Space Grotesk", FB = "Manrope", FM = "JetBrains Mono";
const L = 1.25, W = 17.5, PAGE_W = 20, PAGE_H = 11.25;

/* defineLayout PRECISA vir antes de qualquer addSlide */
function novo(titulo) {
  const p = new pptxgen();
  p.defineLayout({ name: "SB", width: PAGE_W, height: PAGE_H });
  p.layout = "SB";
  p.title = titulo;
  return p;
}

function slide(pres, eyebrow, page, o = {}) {
  const s = pres.addSlide();
  s.background = { path: o.blue ? "bg_blue.png" : "bg_dark.png" };
  if (eyebrow) s.addText(eyebrow, {
    x: L, y: 0.82, w: 13, h: 0.5, isTextBox: true, margin: 0,
    fontFace: FM, fontSize: 23, bold: true,
    color: o.blue ? BLUE_PALE : BLUE_L, charSpacing: 1.2,
  });
  if (page) s.addText(page, {
    x: 15.9, y: 0.88, w: 2.85, h: 0.42, isTextBox: true, margin: 0, align: "right",
    fontFace: FM, fontSize: 16, color: T_PAGE,
  });
  return s;
}

const h1 = (s, t, o = {}) => s.addText(t, {
  x: L, y: o.y ?? 1.55, w: W, h: o.h ?? 1.05, isTextBox: true, margin: 0,
  fontFace: FH, fontSize: o.size ?? 44, bold: true, color: o.color ?? T_H1,
  lineSpacingMultiple: 1.0,
});

const sub = (s, t, o = {}) => s.addText(t, {
  x: L, y: o.y ?? 2.85, w: o.w ?? W, h: o.h ?? 0.6, isTextBox: true, margin: 0,
  fontFace: FB, fontSize: o.size ?? 25, color: o.color ?? T_SUB, lineSpacingMultiple: 1.0,
});

function kicker(pres, s, t, o = {}) {
  const y = o.y ?? 9.8;
  s.addShape(pres.ShapeType.rect, { x: L, y: y - 0.32, w: 0.46, h: 0.021, fill: { color: BLUE } });
  s.addText(t, {
    x: L, y, w: W, h: o.h ?? 0.65, isTextBox: true, margin: 0,
    fontFace: FB, fontSize: o.size ?? 24, color: o.color ?? T_KICK, lineSpacingMultiple: 1.0,
  });
}

const card = (pres, s, x, y, w, h, o = {}) => s.addShape(pres.ShapeType.rect, {
  x, y, w, h,
  fill: { color: o.fill ?? WHITE, transparency: o.transparency ?? 95 },
  line: o.line ? { color: o.line, width: 1.5 } : undefined,
});

const divider = (pres, s, x, y, w) => s.addShape(pres.ShapeType.rect, {
  x, y, w, h: 0.0104, fill: { color: T_KICK, transparency: 86 },
});

const source = (s, t) => s.addText(t, {
  x: L, y: 10.64, w: W, h: 0.3, isTextBox: true, margin: 0,
  fontFace: FM, fontSize: 11, color: T_SRC,
});

/* Lista de itens com marcador fino. items = [[titulo, descricao], ...] */
function lista(pres, s, items, o = {}) {
  const x = o.x ?? L, w = o.w ?? 10.4;
  let y = o.y ?? 4.85;
  items.forEach((it, i) => {
    s.addShape(pres.ShapeType.rect, { x, y: y + 0.23, w: 0.23, h: 0.021, fill: { color: BLUE } });
    s.addText(it[0], { x: x + 0.45, y: y - 0.02, w: w - 0.45, h: 0.5, isTextBox: true, margin: 0,
      fontFace: FH, fontSize: o.size ?? 25, bold: true, color: T_H1 });
    if (it[1]) s.addText(it[1], { x: x + 0.45, y: y + 0.5, w: w - 0.45, h: 0.45, isTextBox: true,
      margin: 0, fontFace: FB, fontSize: 19, color: T_BODY });
    y += o.step ?? 1.14;
    if (i < items.length - 1 && o.divider !== false) divider(pres, s, x, y - 0.22, w);
  });
  return y;
}

/* Barra horizontal comparativa. rows = [[valor, rotulo, tag|null, destaque], ...] */
function barras(pres, s, rows, o = {}) {
  const max = o.max ?? Math.max(...rows.map((r) => r[0]));
  const barX = o.barX ?? 4.05, barMax = o.barMax ?? 4.6, step = o.step ?? 0.5;
  const fmt = o.fmt ?? ((v) => "R$ " + v.toFixed(2).replace(".", ","));
  let y = o.y ?? 3.35;
  rows.forEach((r) => {
    const [v, rotulo, tag, hl] = r;
    s.addText(fmt(v), { x: L, y, w: 2.45, h: 0.44, isTextBox: true, margin: 0,
      align: "right", valign: "middle", fontFace: FH, fontSize: 20, bold: true,
      color: hl ? WHITE : T_ITEM });
    s.addShape(pres.ShapeType.rect, { x: barX, y: y + 0.155,
      w: Math.max((barMax * v) / max, 0.1), h: 0.145, fill: { color: hl ? BLUE : BLUE_DK } });
    s.addText(rotulo, { x: 9.15, y, w: 5.3, h: 0.44, isTextBox: true, margin: 0,
      valign: "middle", fontFace: FB, fontSize: 17, color: hl ? T_H1 : T_DIM });
    if (tag) s.addText(tag, { x: 14.6, y, w: 4.15, h: 0.44, isTextBox: true, margin: 0,
      align: "right", valign: "middle", fontFace: FM, fontSize: 12,
      color: hl ? AMBER : T_SRC, charSpacing: 0.6 });
    y += step;
  });
  return y;
}

module.exports = { novo, slide, h1, sub, kicker, card, divider, source, lista, barras,
  BLUE, BLUE_L, BLUE_PALE, BLUE_SUB, BLUE_NUM, BLUE_DK, T_H1, T_SUB, T_BODY, T_KICK,
  T_ITEM, T_DIM, T_PAGE, T_SRC, WHITE, AMBER, FH, FB, FM, L, W, PAGE_W, PAGE_H };
