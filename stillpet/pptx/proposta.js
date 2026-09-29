const D = require("./deck.js");
const { L, W, BLUE, BLUE_L, BLUE_PALE, BLUE_NUM, BLUE_DK, T_H1, T_SUB, T_BODY,
        T_ITEM, T_DIM, T_SRC, WHITE, AMBER, FH, FB, FM } = D;

const pres = D.novo("Proposta — Catálogo Amazon 1P — Still Pet");
const N = 11;
const pg = (i) => String(i).padStart(2, "0") + " / " + N;
const SRC = "Escopo e condições conforme reunião de alinhamento. Números de catálogo: levantamento impulsio na Amazon.com.br, 23 set 2026.";

/* número grande com rótulo */
function numero(s, x, y, valor, rotulo, o = {}) {
  s.addText(valor, { x, y, w: o.w ?? 4.6, h: 1.5, isTextBox: true, margin: 0,
    fontFace: FH, fontSize: o.size ?? 96, bold: true,
    color: o.color ?? T_H1, lineSpacingMultiple: 0.85 });
  s.addText(rotulo, { x, y: y + 1.5, w: o.w ?? 4.6, h: 0.8, isTextBox: true, margin: 0,
    fontFace: FM, fontSize: 14, color: T_DIM, charSpacing: 1.4 });
}

/* linha de tabela: rótulo à esquerda, valor à direita */
function linhas(s, rows, o = {}) {
  const x = o.x ?? L, w = o.w ?? 17.5;
  let y = o.y ?? 4.4;
  rows.forEach((r, i) => {
    s.addText(r[0], { x, y, w: w * 0.62, h: 0.52, isTextBox: true, margin: 0,
      valign: "middle", fontFace: FB, fontSize: o.size ?? 20, color: T_BODY });
    s.addText(r[1], { x: x + w * 0.62, y, w: w * 0.38, h: 0.52, isTextBox: true, margin: 0,
      align: "right", valign: "middle", fontFace: FM, fontSize: (o.size ?? 20) - 3,
      color: r[2] ?? T_ITEM });
    y += o.step ?? 0.62;
    if (i < rows.length - 1) D.divider(pres, s, x, y - 0.08, w);
  });
  return y;
}

/* caixa com rótulo, título e descrição */
function caixa(s, x, y, w, h, kicker, titulo, desc, o = {}) {
  D.card(pres, s, x, y, w, h, { transparency: o.tr ?? 94, line: o.line });
  s.addText(kicker, { x: x + 0.42, y: y + 0.36, w: w - 0.84, h: 0.34, isTextBox: true, margin: 0,
    fontFace: FM, fontSize: 13, bold: true, color: o.kc ?? BLUE_L, charSpacing: 1.4 });
  s.addText(titulo, { x: x + 0.42, y: y + 0.78, w: w - 0.84, h: 0.62, isTextBox: true, margin: 0,
    fontFace: FH, fontSize: o.ts ?? 24, bold: true, color: T_H1, lineSpacingMultiple: 1.0 });
  if (desc) s.addText(desc, { x: x + 0.42, y: y + 1.44, w: w - 0.84, h: h - 1.8, isTextBox: true,
    margin: 0, fontFace: FB, fontSize: o.ds ?? 16, color: T_BODY, lineSpacingMultiple: 1.0 });
}

/* ───────── 01 · CAPA ───────── */
let s = D.slide(pres, "PROPOSTA — CATÁLOGO AMAZON 1P", pg(1), { blue: true });
s.addText("Still Pet", { x: L, y: 3.05, w: W, h: 0.7, isTextBox: true, margin: 0,
  fontFace: FM, fontSize: 22, color: BLUE_PALE, charSpacing: 1.6 });
D.h1(s, "Organizar o catálogo\nda Still Pet na Amazon", { y: 3.85, h: 2.4, size: 62 });
D.sub(s, "Seis meses para colocar no padrão tudo que já está no ar,\ne abrir espaço para o que vem depois.", { y: 6.5, h: 1.2 });
D.kicker(pres, s, "O diagnóstico vocês já receberam. Esta é a execução dele.", { y: 9.9 });
D.source(s, SRC);

/* ───────── 02 · O PONTO DE PARTIDA ───────── */
s = D.slide(pres, "O PONTO DE PARTIDA", pg(2));
D.h1(s, "O que já está medido.", { y: 1.55 });
D.sub(s, "O diagnóstico de 23 de setembro mapeou a conta inteira, com print e data em cada número.\nEsta proposta parte dele, não de suposição.", { y: 2.75, h: 1.1 });
numero(s, L, 4.35, "151", "FICHAS DA MARCA NO AR");
numero(s, 6.5, 4.35, "0", "DENTRO DO PADRÃO", { color: AMBER });
numero(s, 11.75, 4.35, "19", "ERROS DE CADASTRO MAPEADOS", { color: AMBER, w: 6.2 });
linhas(s, [
  ["Erros críticos abertos", "2"],
  ["Marcas da mesma fábrica concorrendo entre si", "3", AMBER],
  ["Buy box perdida ou vazia", "2 fichas", AMBER],
  ["Ruptura no catálogo documentado", "13 de 28", AMBER],
], { y: 7.1, step: 0.6 });
D.kicker(pres, s, "O trabalho não começa do zero. Começa de um levantamento que vocês já têm na mão.");
D.source(s, SRC);

/* ───────── 03 · O OBJETIVO ───────── */
s = D.slide(pres, "O OBJETIVO", pg(3));
D.h1(s, "Uma ficha que responde\nàs perguntas da Amazon.", { y: 1.55, h: 2.1 });
caixa(s, L, 4.3, 5.5, 4.5, "01", "Arquitetura\nde marca",
  "Definir como Still Pet, Tudo Pet e Quick Pet convivem no canal, e migrar as fichas para essa decisão.");
caixa(s, 7.25, 4.3, 5.5, 4.5, "02", "Ficha\nno padrão",
  "Título, atributos, categoria e conteúdo preenchidos do jeito que a Amazon filtra e o comprador procura.");
caixa(s, 13.25, 4.3, 5.5, 4.5, "03", "Catálogo\nem ondas",
  "Os 151 primeiro. Depois, dez produtos novos por mês, na ordem que vocês definirem.");
D.kicker(pres, s, "O produto de vocês já compete. O que falta é a informação chegar junto com ele.");
D.source(s, SRC);

/* ───────── 04 · ESCOPO ───────── */
s = D.slide(pres, "ESCOPO · O QUE A IMPULSIO EXECUTA", pg(4));
D.h1(s, "O escopo, entrega\npor entrega.", { y: 1.55, h: 2.1 });
s.addText("01 / AUDITORIA E ARQUITETURA", { x: L, y: 4.2, w: 8.2, h: 0.4, isTextBox: true,
  margin: 0, fontFace: FM, fontSize: 14, bold: true, color: BLUE_L, charSpacing: 1.4 });
linhas(s, [
  ["Leitura das 151 fichas, uma a uma", "mês 1", T_DIM],
  ["Arquitetura das três marcas", "mês 1", T_DIM],
  ["Padrão de ficha e de título", "mês 1", T_DIM],
  ["Mapa de categoria e atributos", "mês 1", T_DIM],
  ["Plano de ondas, com prioridade", "mês 1", T_DIM],
], { x: L, w: 8.2, y: 4.85, size: 17, step: 0.56 });
s.addText("02 / EXECUÇÃO DE CATÁLOGO", { x: 10.55, y: 4.2, w: 8.2, h: 0.4, isTextBox: true,
  margin: 0, fontFace: FM, fontSize: 14, bold: true, color: BLUE_L, charSpacing: 1.4 });
linhas(s, [
  ["Correção das 151 fichas no ar", "meses 1–3", T_DIM],
  ["Cadastro de 10 SKUs novos por mês", "meses 3–6", T_DIM],
  ["Correção de categoria e atributo", "contínuo", T_DIM],
  ["Monitoramento de regressão de ficha", "contínuo", T_DIM],
  ["Relatório de execução", "mensal", T_DIM],
], { x: 10.55, w: 8.2, y: 4.85, size: 17, step: 0.56 });
s.addText("Imagens e informação técnica de produto são fornecidas pela Still Pet. A impulsio organiza, não produz foto nem vídeo.",
  { x: L, y: 8.15, w: W, h: 0.5, isTextBox: true, margin: 0, fontFace: FB, fontSize: 16, color: T_DIM });
D.kicker(pres, s, "191 fichas no padrão ao fim de seis meses: as 151 que já estão no ar, mais 40 novas.");
D.source(s, SRC);

/* ───────── 05 · O QUE NÃO ESTÁ INCLUÍDO ───────── */
s = D.slide(pres, "O QUE NÃO ESTÁ INCLUÍDO", pg(5));
D.h1(s, "E dizemos isso antes\nde vocês perguntarem.", { y: 1.55, h: 2.1 });
const fora = [
  ["COMERCIAL COM A AMAZON", "Nenhuma negociação de preço, prazo, pedido ou entrada de produto. Essa relação continua sendo de vocês."],
  ["GESTÃO DE PERFORMANCE", "Não acompanhamos venda, sell-out, rentabilidade nem metas de faturamento neste contrato."],
  ["MÍDIA PAGA", "Retail media não entra. Tráfego para ficha incompleta vira desconto, não venda."],
  ["FOTO, VÍDEO E CRIATIVO", "Produção de imagem não está no escopo. Trabalhamos com o material que vocês fornecerem."],
  ["ATENDIMENTO AO COMPRADOR", "SAC, devolução e disputa com a plataforma seguem com vocês."],
  ["ASSUNTO JURÍDICO DE MARCA", "Registro e contrafação são do departamento legal da Still Pet. A impulsio atua na operação."],
];
fora.forEach((f, i) => {
  const col = i % 3, row = Math.floor(i / 3);
  const x = L + col * 6.0, y = 4.3 + row * 2.65;
  D.card(pres, s, x, y, 5.55, 2.3, { transparency: 94 });
  s.addText(f[0], { x: x + 0.38, y: y + 0.3, w: 4.8, h: 0.34, isTextBox: true, margin: 0,
    fontFace: FM, fontSize: 12, bold: true, color: AMBER, charSpacing: 1.2 });
  s.addText(f[1], { x: x + 0.38, y: y + 0.75, w: 4.8, h: 1.3, isTextBox: true, margin: 0,
    fontFace: FB, fontSize: 15, color: T_BODY, lineSpacingMultiple: 1.0 });
});
D.kicker(pres, s, "Escopo que não está escrito vira discussão no mês quatro. Preferimos a discussão agora.");
D.source(s, SRC);

/* ───────── 06 · OS SEIS MESES ───────── */
s = D.slide(pres, "OS SEIS MESES", pg(6));
D.h1(s, "Quatro tempos.\nUma entrega contínua.", { y: 1.55, h: 2.1 });
const fases = [
  ["MÊS 1", "Arquitetura", "Leitura das 151 fichas.\nDecisão de marca.\nPadrão de ficha.\nPlano de ondas."],
  ["MESES 1–3", "Onda 1", "151 fichas corrigidas.\nCategoria e atributo.\nTítulo e conteúdo.\nMigração de marca."],
  ["MESES 3–6", "Onda 2", "10 SKUs novos por mês.\nPrioridade definida por vocês.\nMesmo padrão da Onda 1."],
  ["MÊS 6", "Fechamento", "Revisão contra a linha de partida.\nEntrega de planilha e padrão.\nPlano da onda seguinte."],
];
fases.forEach((f, i) => {
  const x = L + i * 4.45;
  D.card(pres, s, x, 4.3, 4.1, 4.3, { transparency: 94 });
  s.addText(f[0], { x: x + 0.36, y: 4.62, w: 3.4, h: 0.34, isTextBox: true, margin: 0,
    fontFace: FM, fontSize: 13, bold: true, color: BLUE_L, charSpacing: 1.3 });
  s.addText(f[1], { x: x + 0.36, y: 5.06, w: 3.4, h: 0.55, isTextBox: true, margin: 0,
    fontFace: FH, fontSize: 24, bold: true, color: T_H1 });
  s.addText(f[2], { x: x + 0.36, y: 5.72, w: 3.4, h: 2.4, isTextBox: true, margin: 0,
    fontFace: FB, fontSize: 15, color: T_BODY, lineSpacingMultiple: 1.0 });
});
s.addText("O prazo corre a partir do recebimento de cada insumo. Se um material atrasa, a entrega desloca o mesmo número de dias, com aviso por escrito no momento em que o atraso aparece.",
  { x: L, y: 8.9, w: W, h: 0.6, isTextBox: true, margin: 0, fontFace: FB, fontSize: 16, color: T_DIM });
D.kicker(pres, s, "A Onda 2 só começa depois que a Onda 1 estiver publicada.");
D.source(s, SRC);

/* ───────── 07 · COMO SE MEDE ───────── */
s = D.slide(pres, "COMO O TRABALHO É MEDIDO", pg(7));
D.h1(s, "Pelo que a operação\ncontrola.", { y: 1.55, h: 2.1 });
s.addText("OS INDICADORES DO CONTRATO", { x: L, y: 4.2, w: 8.2, h: 0.4, isTextBox: true,
  margin: 0, fontFace: FM, fontSize: 14, bold: true, color: BLUE_L, charSpacing: 1.4 });
linhas(s, [
  ["Fichas no padrão", "0 → 191"],
  ["Erros críticos abertos", "2 → 0"],
  ["Erros de categoria", "5 → 0"],
  ["Marcas na arquitetura", "3 soltas → 1 decidida"],
  ["SKUs novos publicados", "10 por mês"],
], { x: L, w: 8.2, y: 4.85, size: 17, step: 0.58 });
s.addText("O QUE NÃO PROMETEMOS", { x: 10.55, y: 4.2, w: 8.2, h: 0.4, isTextBox: true,
  margin: 0, fontFace: FM, fontSize: 14, bold: true, color: AMBER, charSpacing: 1.4 });
s.addText("Meta de faturamento. Na Amazon 1P o faturamento depende do pedido que a Amazon decide fazer, do preço que vocês praticam e do estoque que vocês têm. Nada disso está sob controle da operação.",
  { x: 10.55, y: 4.85, w: 8.2, h: 1.7, isTextBox: true, margin: 0, fontFace: FB, fontSize: 18,
    color: T_BODY, lineSpacingMultiple: 1.0 });
s.addText("Também não prometemos que a Amazon vai comprar os produtos novos. O que fazemos é deixar a ficha pronta e correta para quando ela comprar. A decisão de compra é dela.",
  { x: 10.55, y: 6.6, w: 8.2, h: 1.5, isTextBox: true, margin: 0, fontFace: FB, fontSize: 16,
    color: T_DIM, lineSpacingMultiple: 1.0 });
D.kicker(pres, s, "É mais fácil vender promessa de faturamento. É mais honesto vender o que dá para conferir na tela.");
D.source(s, SRC);

/* ───────── 08 · O INVESTIMENTO ───────── */
s = D.slide(pres, "O INVESTIMENTO", pg(8), { blue: true });
D.h1(s, "Dentro do orçamento\nque vocês definiram.", { y: 1.55, h: 2.1 });
D.card(pres, s, L, 4.25, 8.5, 3.5, { transparency: 92 });
s.addText("SETUP E ARQUITETURA", { x: L + 0.5, y: 4.62, w: 7.5, h: 0.36, isTextBox: true,
  margin: 0, fontFace: FM, fontSize: 14, bold: true, color: BLUE_PALE, charSpacing: 1.4 });
s.addText("R$ 2.500", { x: L + 0.5, y: 5.08, w: 7.5, h: 1.1, isTextBox: true, margin: 0,
  fontFace: FH, fontSize: 60, bold: true, color: WHITE });
s.addText("Pagamento único, na assinatura", { x: L + 0.5, y: 6.2, w: 7.5, h: 0.38, isTextBox: true,
  margin: 0, fontFace: FM, fontSize: 14, color: BLUE_PALE });
s.addText("Auditoria das 151 fichas, arquitetura das três marcas, padrão de ficha, mapa de categoria e plano de ondas.",
  { x: L + 0.5, y: 6.68, w: 7.5, h: 0.85, isTextBox: true, margin: 0, fontFace: FB,
    fontSize: 16, color: T_BODY, lineSpacingMultiple: 1.0 });
D.card(pres, s, 10.25, 4.25, 8.5, 3.5, { transparency: 92 });
s.addText("EXECUÇÃO MENSAL", { x: 10.75, y: 4.62, w: 7.5, h: 0.36, isTextBox: true,
  margin: 0, fontFace: FM, fontSize: 14, bold: true, color: BLUE_PALE, charSpacing: 1.4 });
s.addText("R$ 2.500", { x: 10.75, y: 5.08, w: 7.5, h: 1.1, isTextBox: true, margin: 0,
  fontFace: FH, fontSize: 60, bold: true, color: WHITE });
s.addText("Por mês, durante seis meses", { x: 10.75, y: 6.2, w: 7.5, h: 0.38, isTextBox: true,
  margin: 0, fontFace: FM, fontSize: 14, color: BLUE_PALE });
s.addText("Execução do catálogo, correção contínua, monitoramento de regressão de ficha e relatório mensal.",
  { x: 10.75, y: 6.68, w: 7.5, h: 0.85, isTextBox: true, margin: 0, fontFace: FB,
    fontSize: 16, color: T_BODY, lineSpacingMultiple: 1.0 });
linhas(s, [
  ["Total do contrato, seis meses", "R$ 17.500", WHITE],
  ["Fichas entregues no padrão", "191"],
  ["Remuneração variável", "não há", WHITE],
], { y: 8.1, size: 19, step: 0.58 });
D.kicker(pres, s, "Sem variável: quem decide o volume comprado é a Amazon, e não cobramos percentual sobre decisão que não é nossa nem de vocês.", { size: 20 });
D.source(s, SRC);

/* ───────── 09 · O QUE PRECISAMOS ───────── */
s = D.slide(pres, "O QUE PRECISAMOS DE VOCÊS", pg(9));
D.h1(s, "Cinco insumos,\ne o relógio para.", { y: 1.55, h: 2.1 });
linhas(s, [
  ["Acesso ao Vendor Central", "semana 1", T_DIM],
  ["Planilha de produtos do ERP", "semana 1", T_DIM],
  ["Decisão sobre arquitetura de marca", "mês 1", AMBER],
  ["Imagens de produto em alta resolução", "por onda", T_DIM],
  ["Ficha técnica: medida, peso, capacidade", "por onda", T_DIM],
], { x: L, w: 8.2, y: 4.35, size: 18, step: 0.62 });
D.card(pres, s, 10.55, 4.25, 8.2, 4.2, { transparency: 94 });
s.addText("PARADA DE RELÓGIO", { x: 11.05, y: 4.62, w: 7.2, h: 0.36, isTextBox: true,
  margin: 0, fontFace: FM, fontSize: 14, bold: true, color: BLUE_L, charSpacing: 1.4 });
s.addText("O prazo de cada entrega corre a partir do recebimento do insumo, não da data do contrato.",
  { x: 11.05, y: 5.1, w: 7.2, h: 1.1, isTextBox: true, margin: 0, fontFace: FH, fontSize: 21,
    bold: true, color: T_H1, lineSpacingMultiple: 1.0 });
s.addText("Se um material atrasar, a entrega desloca o mesmo número de dias e avisamos por escrito no momento em que o atraso aparece, não no fim do mês.",
  { x: 11.05, y: 6.35, w: 7.2, h: 1.1, isTextBox: true, margin: 0, fontFace: FB, fontSize: 16,
    color: T_BODY, lineSpacingMultiple: 1.0 });
s.addText("A decisão de arquitetura de marca é a que mais trava: sem ela a correção não começa, porque não se sabe para qual marca migrar.",
  { x: 11.05, y: 7.5, w: 7.2, h: 0.85, isTextBox: true, margin: 0, fontFace: FB, fontSize: 15,
    color: T_DIM, lineSpacingMultiple: 1.0 });
D.kicker(pres, s, "A informação técnica do produto está com vocês. Sem ela, nenhuma ficha fica pronta.");
D.source(s, SRC);

/* ───────── 10 · TITULARIDADE ───────── */
s = D.slide(pres, "TITULARIDADE E SAÍDA", pg(10));
D.h1(s, "Tudo que for construído\né de vocês.", { y: 1.55, h: 2.1 });
D.sub(s, "A impulsio opera dentro da conta da Still Pet. Nada fica hospedado conosco.", { y: 3.85, h: 0.6 });
linhas(s, [
  ["Acessos administrativos", "Still Pet"],
  ["Fichas e conteúdo produzido", "Still Pet"],
  ["Padrão, planilha e arquitetura", "Still Pet"],
  ["Entrega na saída", "15 dias"],
  ["Vigência do contrato", "6 meses"],
], { y: 4.9, size: 20, step: 0.66 });
s.addText("Se ao fim dos seis meses vocês quiserem internalizar a operação, entregamos planilha, padrão e acessos em quinze dias, sem retenção de nada.",
  { x: L, y: 8.4, w: W, h: 0.6, isTextBox: true, margin: 0, fontFace: FB, fontSize: 17, color: T_DIM });
D.kicker(pres, s, "Organizar a casa de vocês, não alugá-la.");
D.source(s, SRC);

/* ───────── 11 · PRÓXIMO PASSO ───────── */
s = D.slide(pres, "O PRÓXIMO PASSO", pg(11), { blue: true });
D.h1(s, "Quatro movimentos\npara começar.", { y: 1.55, h: 2.1 });
const passos = [
  ["01", "Aceite", "Assinatura e pagamento do setup."],
  ["02", "Acessos", "Vendor Central e planilha do ERP, na primeira semana."],
  ["03", "Kickoff", "Reunião de alinhamento em até 48 horas do aceite."],
  ["04", "Arquitetura", "A decisão sobre as três marcas, que destrava a Onda 1."],
];
passos.forEach((p, i) => {
  const x = L + i * 4.45;
  D.card(pres, s, x, 4.3, 4.1, 3.4, { transparency: 92 });
  s.addText(p[0], { x: x + 0.36, y: 4.6, w: 3.4, h: 0.5, isTextBox: true, margin: 0,
    fontFace: FM, fontSize: 15, bold: true, color: BLUE_PALE, charSpacing: 1.4 });
  s.addText(p[1], { x: x + 0.36, y: 5.12, w: 3.4, h: 0.55, isTextBox: true, margin: 0,
    fontFace: FH, fontSize: 25, bold: true, color: WHITE });
  s.addText(p[2], { x: x + 0.36, y: 5.78, w: 3.4, h: 1.5, isTextBox: true, margin: 0,
    fontFace: FB, fontSize: 16, color: T_BODY, lineSpacingMultiple: 1.0 });
});
s.addText("Ao fim dos seis meses a Still Pet tem 191 fichas no padrão, uma arquitetura de marca decidida e um catálogo pronto para receber o restante do portfólio.",
  { x: L, y: 8.2, w: W, h: 0.7, isTextBox: true, margin: 0, fontFace: FB, fontSize: 18, color: T_BODY });
D.kicker(pres, s, "impulsio · operação de canais digitais para indústrias e distribuidores", { size: 20 });
D.source(s, "Proposta válida por 30 dias · setembro de 2026");

pres.writeFile({ fileName: "Proposta-Catalogo-Amazon-StillPet.pptx" })
  .then((f) => console.log("ok:", f));
