/* Gera os decks da linha de mandioca no padrão Marca Protagonista.
 *   node build.js
 * Saída: 01-Diagnostico.pptx · 02-Proposta-Comercial.pptx · COMPLETO.pptx · 03-Anexo-EUA.pptx */
const D = require("./deck.js");
const M = require("./modelo.js");
const { L, W, BLUE, BLUE_L, BLUE_PALE, BLUE_NUM, BLUE_DK, T_H1, T_SUB, T_BODY,
        T_ITEM, T_DIM, T_SRC, WHITE, AMBER, FH, FB, FM } = D;

/* PENDENTE: confirmar a razão social / marca-mãe antes de apresentar. */
const CLIENTE = "[NOME DA EMPRESA]";
const DATA = "outubro de 2026";

const SRC_ML = "JoomPulse · Mercado Livre · Areias Higiênicas (MLB251837) · jul/2026. GMV e pedidos são estimativas da plataforma, não faturamento auditado.";
const SRC_CALL = "Fonte: reunião de descoberta com a diretoria · " + DATA + ".";
const SRC_MODELO = "Projeção impulsio. Cenário, não meta. Premissas na planilha Projecao-Retorno.xlsx; margem de contribuição a confirmar com vocês.";

/* ───────── formatação ───────── */
const milhar = (v) => Math.round(v).toLocaleString("pt-BR");
const brl = (v) => "R$ " + milhar(v);
const mil = (v) => (v < 0 ? "−" : "") + "R$ " + (Math.abs(v) / 1000).toLocaleString("pt-BR", { maximumFractionDigits: 1 }) + " mil";

/* ───────── componentes locais ───────── */
function numero(pres, s, x, y, valor, rotulo, o = {}) {
  s.addText(valor, { x, y, w: o.w ?? 5.2, h: 1.4, isTextBox: true, margin: 0,
    fontFace: FH, fontSize: o.size ?? 80, bold: true,
    color: o.color ?? T_H1, lineSpacingMultiple: 0.85 });
  s.addText(rotulo, { x, y: y + 1.45, w: o.w ?? 5.2, h: o.rh ?? 0.8, isTextBox: true, margin: 0,
    fontFace: FM, fontSize: 14, color: T_DIM, charSpacing: 1.4 });
}

function linhas(pres, s, rows, o = {}) {
  const x = o.x ?? L, w = o.w ?? W, split = o.split ?? 0.62;
  let y = o.y ?? 4.4;
  rows.forEach((r, i) => {
    s.addText(r[0], { x, y, w: w * split, h: 0.52, isTextBox: true, margin: 0,
      valign: "middle", fontFace: FB, fontSize: o.size ?? 20, color: T_BODY });
    s.addText(r[1], { x: x + w * split, y, w: w * (1 - split), h: 0.52, isTextBox: true, margin: 0,
      align: "right", valign: "middle", fontFace: FM, fontSize: (o.size ?? 20) - 3,
      color: r[2] ?? T_ITEM });
    y += o.step ?? 0.62;
    if (i < rows.length - 1) D.divider(pres, s, x, y - 0.08, w);
  });
  return y;
}

function caixa(pres, s, x, y, w, h, kicker, titulo, desc, o = {}) {
  D.card(pres, s, x, y, w, h, { transparency: o.tr ?? 94, line: o.line });
  s.addText(kicker, { x: x + 0.42, y: y + 0.36, w: w - 0.84, h: 0.34, isTextBox: true, margin: 0,
    fontFace: FM, fontSize: 13, bold: true, color: o.kc ?? BLUE_L, charSpacing: 1.4 });
  s.addText(titulo, { x: x + 0.42, y: y + 0.78, w: w - 0.84, h: o.th ?? 0.62, isTextBox: true, margin: 0,
    fontFace: FH, fontSize: o.ts ?? 24, bold: true, color: T_H1, lineSpacingMultiple: 1.0 });
  if (desc) {
    const dy = y + 0.78 + (o.th ?? 0.62) + 0.12;
    s.addText(desc, { x: x + 0.42, y: dy, w: w - 0.84, h: y + h - dy - 0.3, isTextBox: true,
      margin: 0, fontFace: FB, fontSize: o.ds ?? 16, color: T_BODY, lineSpacingMultiple: 1.0, valign: "top" });
  }
}

function rotulo(s, t, x, y, w, o = {}) {
  s.addText(t, { x, y, w, h: 0.4, isTextBox: true, margin: 0, fontFace: FM, fontSize: 14,
    bold: true, color: o.color ?? BLUE_L, charSpacing: 1.4 });
}

function texto(s, t, x, y, w, h, o = {}) {
  s.addText(t, { x, y, w, h, isTextBox: true, margin: 0, fontFace: o.font ?? FB,
    fontSize: o.size ?? 17, bold: o.bold ?? false, color: o.color ?? T_BODY,
    lineSpacingMultiple: 1.0, valign: o.valign ?? "top", align: o.align ?? "left" });
}

/* ───────── projeção ───────── */
const proj = Object.fromEntries(M.CENARIOS.map((c) => [c.id, M.projetar(c.T)]));
const base = proj.base;
const labels = base.meses.map((r) => String(r.m));
const fee6 = base.meses.slice(0, 6).reduce((a, r) => a + r.fee, 0);

const chartBase = {
  chartColors: [BLUE_DK, BLUE, BLUE_PALE],
  catAxisLabelColor: "8B93A4", valAxisLabelColor: "8B93A4",
  catAxisLabelFontFace: FM, valAxisLabelFontFace: FM,
  catAxisLabelFontSize: 11, valAxisLabelFontSize: 11,
  catAxisLineShow: false, valAxisLineShow: false,
  valGridLine: { color: "2A3142", size: 0.75 }, catGridLine: { style: "none" },
  showLegend: true, legendPos: "t", legendColor: "DBE3F5", legendFontFace: FB, legendFontSize: 14,
  lineSize: 3, lineDataSymbol: "none",
  catAxisTitle: "mês", showCatAxisTitle: true, catAxisTitleColor: "8B93A4",
  catAxisTitleFontSize: 11, catAxisTitleFontFace: FM,
};

/* ═════════════════════ DIAGNÓSTICO ═════════════════════ */
const DIAG = [

/* 01 · CAPA */
(pres, pg) => {
  const s = D.slide(pres, "DIAGNÓSTICO DE CANAL · MERCADO LIVRE", pg, { blue: true });
  s.addText(CLIENTE, { x: L, y: 3.05, w: W, h: 0.7, isTextBox: true, margin: 0,
    fontFace: FM, fontSize: 22, color: AMBER, charSpacing: 1.6 });
  D.h1(s, "A areia de mandioca\nno Mercado Livre", { y: 3.85, h: 2.4, size: 62 });
  D.sub(s, "O que o canal mostra hoje, onde a linha de vocês cabe\ne quanto ela pode devolver.", { y: 6.5, h: 1.2 });
  D.kicker(pres, s, "O diagnóstico vem antes do contrato. Vocês decidem depois de ver.", { y: 9.9 });
  D.source(s, "Preparado pela impulsio · " + DATA);
  s.addNotes("Abrir agradecendo o tempo e lembrando o combinado da última conversa: trazer o estudo de mercado e a projeção de retorno. Dizer que a primeira metade é diagnóstico e a segunda, proposta, em arquivos separados.");
},

/* 02 · O QUE OUVIMOS */
(pres, pg) => {
  const s = D.slide(pres, "O QUE OUVIMOS", pg);
  D.h1(s, "O ponto de partida,\nnas palavras de vocês.", { y: 1.55, h: 2.1 });
  const falas = [
    ["AREIA COMUM", "“80% das vendas em volume. Muito peso e pouco valor agregado.”"],
    ["MANDIOCA", "“É mais cara e está tendo uma saída melhor.” Lançada em julho, na casa dos cem mil por mês via distribuidores."],
    ["A DÚVIDA", "“Nossa maior dúvida é atingir esse público do valor agregado.”"],
  ];
  falas.forEach((f, i) => {
    const x = L + i * 5.95;
    D.card(pres, s, x, 4.25, 5.6, 3.3, { transparency: 94 });
    s.addText(f[0], { x: x + 0.4, y: 4.6, w: 4.8, h: 0.34, isTextBox: true, margin: 0,
      fontFace: FM, fontSize: 13, bold: true, color: i === 2 ? AMBER : BLUE_L, charSpacing: 1.4 });
    texto(s, f[1], x + 0.4, 5.1, 4.8, 2.2, { font: FH, size: 21, bold: true, color: T_H1 });
  });
  linhas(pres, s, [
    ["Tempo de fábrica", "19 anos"],
    ["Canal de venda hoje", "distribuidores"],
    ["Distância até o CD do Mercado Livre em Ribeirão Preto", "≈ 90 km"],
  ], { y: 7.85, size: 18, step: 0.56 });
  D.kicker(pres, s, "A pergunta deste estudo: o comprador online paga pelo valor agregado?");
  D.source(s, SRC_CALL);
},

/* 03 · O CONTEXTO · TAMANHO */
(pres, pg) => {
  const s = D.slide(pres, "O CONTEXTO", pg);
  D.h1(s, "Areia higiênica no Mercado Livre:\nR$ 4,9 milhões por mês.", { y: 1.55, h: 2.1 });
  numero(pres, s, L, 4.2, "R$ 4,88 mi", "GMV ESTIMADO / MÊS", { size: 64, w: 5.6 });
  numero(pres, s, 7.2, 4.2, "97.828", "PEDIDOS / MÊS", { size: 64, w: 5.2 });
  numero(pres, s, 13.0, 4.2, "R$ 49,86", "TICKET MÉDIO", { size: 64, w: 5.75 });
  linhas(pres, s, [
    ["Vendedores com venda no mês", "1.270 de 2.232"],
    ["Produtos com venda no mês", "1.249 de 11.881"],
    ["Concentração (monopolização)", "baixa"],
    ["Saturação de oferta", "alta", AMBER],
  ], { y: 6.75, size: 18, step: 0.56 });
  D.kicker(pres, s, "Ninguém é dono da categoria. E nove em cada dez anúncios não vendem nada no mês.");
  D.source(s, SRC_ML);
  s.addNotes("Antecipar a objeção: esses números são estimativa da JoomPulse, não faturamento. Servem para dimensionar e comparar, e vocês vão achar coisas que não batem com o que sabem do mercado. Se baterem diferente, me falem: vocês conhecem a categoria melhor do que qualquer base de dados.\n\nO dado de 1.249 produtos com venda em 11.881 é o que sustenta a frase de fecho: cerca de 89% dos produtos cadastrados não venderam no mês.");
},

/* 04 · O CONTEXTO · DOIS SINAIS */
(pres, pg) => {
  const s = D.slide(pres, "O CONTEXTO", pg);
  D.h1(s, "Dois números que mudam\na estratégia.", { y: 1.55, h: 2.1 });
  numero(pres, s, L, 4.25, "−27%", "TICKET MÉDIO EM 11 MESES", { size: 80, w: 8, color: AMBER });
  texto(s, "De R$ 68,67 para R$ 49,86. A média da categoria está descendo por preço. Quem compete só por preço compete com essa curva.", L, 6.6, 7.8, 1.6, { size: 19 });
  numero(pres, s, 10.55, 4.25, "3,42%", "DOS ANÚNCIOS USAM FULL", { size: 80, w: 8 });
  texto(s, "Quase ninguém na categoria entrega pelo estoque do Mercado Livre. Vocês estão a 90 km de um centro de distribuição dele.", 10.55, 6.6, 8.2, 1.6, { size: 19 });
  D.kicker(pres, s, "Peso e frete são a dor da categoria. Para quem fabrica perto do CD, viram vantagem.");
  D.source(s, SRC_ML);
},

/* 05 · O DIAGNÓSTICO · QUEM LIDERA */
(pres, pg) => {
  const s = D.slide(pres, "O DIAGNÓSTICO", pg);
  D.h1(s, "Duas das quatro maiores marcas\nda categoria são biodegradáveis.", { y: 1.55, h: 2.1 });
  D.sub(s, "GMV estimado por marca no Mercado Livre, por mês.", { y: 3.75, h: 0.5, size: 20, color: T_DIM });
  D.barras(pres, s, [
    [396, "VivaVerde", "BIODEGRADÁVEL", true],
    [308, "Kadi", null, false],
    [192, "Chalesco", null, false],
    [191, "Catbio", "MANDIOCA", true],
    [180, "GreatPets", null, false],
    [144, "WiseCat", null, false],
    [143, "Bento", null, false],
  ], { y: 4.55, step: 0.62, barMax: 4.6, fmt: (v) => "R$ " + v + " mil" });
  D.kicker(pres, s, "O comprador do Mercado Livre já paga pelo valor agregado. A dúvida de vocês tem resposta no dado.");
  D.source(s, "JoomPulse · Mercado Livre · GMV estimado por marca · jul/2026. Classificação das linhas conforme comunicação das próprias marcas.");
  s.addNotes("Este é o slide que responde à dúvida que eles trouxeram. VivaVerde e Catbio somam cerca de R$ 587 mil por mês, perto de 12% da categoria inteira, vendendo areia vegetal mais cara que a média.\n\nNão dizer que essas marcas vendem mais caro sem ter o print de preço na mão. Se perguntarem o preço, abrir a busca ao vivo.");
},

/* 06 · O DIAGNÓSTICO · ML x SHOPEE */
(pres, pg) => {
  const s = D.slide(pres, "O DIAGNÓSTICO", pg);
  D.h1(s, "O concorrente direto vende\n19 vezes mais na Shopee.", { y: 1.55, h: 2.1 });
  rotulo(s, "CATBIO · AREIA DE MANDIOCA · GMV / MÊS", L, 4.15, 9);
  D.barras(pres, s, [
    [3670, "Shopee", "19×", true],
    [191, "Mercado Livre", null, false],
  ], { y: 4.75, step: 0.7, barMax: 4.6, fmt: (v) => v >= 1000 ? "R$ 3,67 mi" : "R$ 191 mil" });
  rotulo(s, "AS DUAS CATEGORIAS, LADO A LADO", L, 6.45, 9);
  linhas(pres, s, [
    ["GMV / mês · Mercado Livre", "R$ 4,88 mi"],
    ["GMV / mês · Shopee*", "R$ 20,2 mi"],
    ["Receita por vendedor com venda · ML / Shopee", "R$ 3,8 mil / R$ 16,0 mil"],
  ], { y: 7.0, size: 17, step: 0.55, split: 0.55 });
  D.kicker(pres, s, "O Mercado Livre é o começo pela logística. A Shopee entra na conversa pelo volume.");
  D.source(s, "JoomPulse · jul/2026. *Na Shopee a categoria é Caixas e Camas de Gato (100923): inclui acessórios, então não se compara 1 para 1 com Areias Higiênicas.");
  s.addNotes("Ser honesto sobre a comparação de categorias: a da Shopee é mais larga e inclui caixa de areia e cama. Por isso o número forte do slide é o da Catbio, que é marca contra marca.\n\nSe perguntarem por que não começar pela Shopee: o Mercado Livre tem o CD de Ribeirão Preto perto da fábrica e o Full ainda é raro na categoria. A Shopee entra como segundo canal, avaliada a partir do mês 4.");
},

/* 07 · O DIAGNÓSTICO · A LINHA DE VOCÊS HOJE */
(pres, pg) => {
  const s = D.slide(pres, "O DIAGNÓSTICO", pg);
  D.h1(s, "O produto de vocês já está no canal.\nA marca, ainda não.", { y: 1.55, h: 2.1 });
  D.card(pres, s, L, 4.2, 10.2, 5.0, { transparency: 96, line: "2A3142" });
  texto(s, "PRINT PENDENTE\n\nMercado Livre · busca “areia de mandioca” e busca pelo nome da marca\nTela inteira, com data visível · capturar até 5 dias antes da reunião",
    L + 0.5, 5.3, 9.2, 2.8, { font: FM, size: 14, color: T_DIM, align: "center", valign: "middle" });
  rotulo(s, "O QUE VIMOS NA CALL", 12.0, 4.2, 6.75);
  texto(s, "Anúncio de produto de vocês com “Nacional Pet” no campo marca, no lugar do fabricante.\n\nOs anúncios encontrados são de terceiros. Nenhum é da fábrica.", 12.0, 4.75, 6.75, 2.4, { size: 17 });
  rotulo(s, "A PERGUNTA", 12.0, 7.3, 6.75, { color: AMBER });
  texto(s, "Quem são os vendedores que anunciam hoje? São distribuidores de vocês?", 12.0, 7.8, 6.75, 1.4, { font: FH, size: 20, bold: true, color: T_H1 });
  D.kicker(pres, s, "Quando a marca não organiza o anúncio, quem organiza é o revendedor.");
  D.source(s, "Observação feita em tela compartilhada durante a reunião de descoberta. Print a capturar.");
  s.addNotes("Fazer a pergunta e esperar. Não afirmar quem são os vendedores.\n\nSE FOREM DISTRIBUIDORES DELES: ótimo, isso vira o argumento da loja oficial. A rede já vende online, só não organizada. Com a loja oficial, a marca corrige ficha e campo de marca uma vez e todos os revendedores credenciados se beneficiam. No escopo, entra o credenciamento.\n\nSE NÃO SOUBEREM OU NÃO FOREM: não insinuar nada sobre o distribuidor. Dizer que é levantamento de mercado e que o primeiro mês de operação inclui mapear quem vende o produto e de onde vem a mercadoria. Não muda o preço.");
},

/* 08 · O DIAGNÓSTICO · POR QUE A MANDIOCA */
(pres, pg) => {
  const s = D.slide(pres, "O DIAGNÓSTICO", pg);
  D.h1(s, "Por onde começar:\no produto que aguenta o frete.", { y: 1.55, h: 2.1 });
  caixa(pres, s, L, 4.2, 8.5, 4.6, "AREIA COMUM", "O carro-chefe da fábrica,\no pior produto para o canal",
    "Pouco valor por quilo. O frete come a margem antes de o produto chegar.\n\nCompete na média da categoria, que perdeu 27% de ticket em onze meses.", { kc: AMBER, th: 1.15 });
  caixa(pres, s, 10.25, 4.2, 8.5, 4.6, "AREIA DE MANDIOCA", "Valor agregado que\ndá para contar",
    "Biodegradável, pode ir ao vaso sanitário, segmento com líderes já estabelecidos no canal.\n\nCada benefício vira conteúdo de anúncio, e conteúdo sustenta preço.", { th: 1.15 });
  D.kicker(pres, s, "A areia comum continua com os distribuidores, onde ela funciona.");
  D.source(s, SRC_CALL + " Dados de categoria: " + SRC_ML.split(". ")[0] + ".");
},

/* 09 · A TESE */
(pres, pg) => {
  const s = D.slide(pres, "A TESE", pg);
  D.h1(s, "Vender benefício,\nnão quilo.", { y: 1.55, h: 2.1 });
  caixa(pres, s, L, 4.2, 5.55, 4.7, "01 · CONTEÚDO", "O anúncio explica\no porquê do preço",
    "Vídeo com veterinário, descarte no vaso, menos poeira. Produzido pelo time de vocês, com o roteiro que a análise de concorrência indicar.", { th: 1.15 });
  caixa(pres, s, 7.2, 4.2, 5.55, 4.7, "02 · ENTREGA", "Full a partir\ndo CD de Ribeirão",
    "Entrega rápida numa categoria em que só 3,42% dos anúncios usam o estoque do Mercado Livre. Habilitado depois que a conta ganha reputação.", { th: 1.15 });
  caixa(pres, s, 13.15, 4.2, 5.6, 4.7, "03 · OFERTA", "Testar antes de\nmudar a fábrica",
    "Kit com dois pacotes, saco de 8 kg com etiqueta adesiva. Mede a demanda antes de investir em clichê e embalagem nova.", { th: 1.15 });
  D.kicker(pres, s, "No digital uma oferta se testa em semanas. Embalagem nova leva 30 a 40 dias.");
  D.source(s, SRC_CALL);
},

/* 10 · O MODELO */
(pres, pg) => {
  const s = D.slide(pres, "O MODELO · MARCA PROTAGONISTA + VENDA DIRETA", pg, { blue: true });
  D.h1(s, "Uma loja oficial.\nDuas formas de vender.", { y: 1.55, h: 2.1 });
  caixa(pres, s, L, 4.2, 17.5, 1.9, "A VITRINE", "Loja oficial da marca-mãe, com as linhas organizadas dentro dela",
    null, { tr: 90, kc: BLUE_PALE, th: 0.6 });
  texto(s, "Uma marca por loja confunde o comprador. A marca-mãe dá credibilidade e as linhas aparecem como coleções.", L + 0.42, 5.55, 16.5, 0.5, { size: 16 });
  caixa(pres, s, L, 6.4, 8.55, 2.7, "VENDA DIRETA", "A fábrica vende na própria conta",
    "Estoque no Full, preço do próprio catálogo definido por vocês.", { tr: 90, kc: BLUE_PALE });
  caixa(pres, s, 10.2, 6.4, 8.55, 2.7, "REDE CREDENCIADA", "Distribuidores vendem pela loja oficial",
    "Quem vocês habilitarem vende sob a vitrine da marca.", { tr: 90, kc: BLUE_PALE });
  D.kicker(pres, s, "A marca é dona da vitrine. Quem vende nela, vocês escolhem.");
  D.source(s, "Modelo proposto pela impulsio a partir da reunião de descoberta.");
},

/* 11 · O CONFLITO */
(pres, pg) => {
  const s = D.slide(pres, "O CONFLITO, COM NOME", pg);
  D.h1(s, "Vocês vão disputar a vitrine\ncom quem compra de vocês.", { y: 1.55, h: 2.1 });
  D.sub(s, "Esconder isso seria pior. A saída é combinar papéis antes de abrir a loja.", { y: 3.75, h: 0.5, size: 21, color: T_DIM });
  const itens = [
    ["SORTIMENTO", "Kits e formatos exclusivos do online, para não colidir com o pacote que o distribuidor leva à loja física."],
    ["PREÇO DO PRÓPRIO CATÁLOGO", "Vocês definem o preço do que a fábrica vende. Cada revendedor mantém autonomia sobre o preço dele."],
    ["CREDENCIAMENTO", "Critério escrito para quem vende pela loja oficial, comunicado à rede antes do lançamento."],
  ];
  itens.forEach((it, i) => {
    const x = L + i * 5.95;
    D.card(pres, s, x, 4.75, 5.6, 3.9, { transparency: 94 });
    s.addText(it[0], { x: x + 0.4, y: 5.1, w: 4.8, h: 0.34, isTextBox: true, margin: 0,
      fontFace: FM, fontSize: 13, bold: true, color: BLUE_L, charSpacing: 1.4 });
    texto(s, it[1], x + 0.4, 5.6, 4.8, 2.8, { size: 18 });
  });
  D.kicker(pres, s, "Conflito ignorado vira guerra de preço em poucos meses. Conflito combinado vira divisão de papéis.");
  D.source(s, "A impulsio não impõe preço a revendedores: orientamos posicionamento do catálogo próprio da marca (Lei 12.529/2011).");
  s.addNotes("Se perguntarem se dá para impedir distribuidor de vender mais barato: não. Imposição de preço de revenda é infração à ordem econômica. O que dá para fazer é diferenciar sortimento, organizar a vitrine e escolher quem vende pela loja oficial.");
},

/* 12 · OS LIMITES */
(pres, pg) => {
  const s = D.slide(pres, "OS LIMITES", pg);
  D.h1(s, "O que a impulsio faz,\ne o que não faz.", { y: 1.55, h: 2.1 });
  const fora = [
    ["REDES SOCIAIS E CRIAÇÃO", "Instagram e arte continuam com o time de vocês. Nós trazemos a demanda e o briefing."],
    ["TREINAMENTO", "Não vendemos curso. Operamos a conta, com analista dedicado e reunião mensal de resultado."],
    ["MÍDIA PAGA ANTES DA HORA", "Anúncio pago só depois do catálogo publicado. Tráfego para ficha incompleta vira desconto."],
    ["PREÇO DO REVENDEDOR", "Não impomos preço a ninguém. Orientamos o posicionamento do catálogo de vocês."],
    ["PROMESSA DE FATURAMENTO", "Projetamos cenário. Respondemos pelo que a operação controla."],
    ["ASSUNTO JURÍDICO DE MARCA", "Registro e contrafação ficam com o jurídico de vocês. Nós atuamos na operação."],
  ];
  fora.forEach((f, i) => {
    const col = i % 3, row = Math.floor(i / 3);
    const x = L + col * 6.0, y = 4.2 + row * 2.6;
    D.card(pres, s, x, y, 5.55, 2.3, { transparency: 94 });
    s.addText(f[0], { x: x + 0.38, y: y + 0.3, w: 4.8, h: 0.34, isTextBox: true, margin: 0,
      fontFace: FM, fontSize: 12, bold: true, color: AMBER, charSpacing: 1.2 });
    texto(s, f[1], x + 0.38, y + 0.75, 4.8, 1.3, { size: 15 });
  });
  D.kicker(pres, s, "Escopo que não está escrito vira discussão no mês quatro. Preferimos a discussão agora.");
  D.source(s, "impulsio · operação de canais digitais.");
},
];

/* ═════════════════════ PROPOSTA ═════════════════════ */
const PROP = [

/* 01 · FECHO */
(pres, pg) => {
  const s = D.slide(pres, "O DIAGNÓSTICO VOCÊS JÁ VIRAM", pg, { blue: true });
  s.addText(CLIENTE, { x: L, y: 3.05, w: W, h: 0.7, isTextBox: true, margin: 0,
    fontFace: FM, fontSize: 22, color: AMBER, charSpacing: 1.6 });
  D.h1(s, "Agora, a execução\ne o retorno dela.", { y: 3.85, h: 2.4, size: 62 });
  D.sub(s, "Escopo, cronograma, investimento e a projeção de retorno,\ncom as premissas na mesa.", { y: 6.5, h: 1.2 });
  D.kicker(pres, s, "Proposta comercial · " + DATA, { y: 9.9 });
  D.source(s, "Este arquivo continua o diagnóstico de canal. Leia os dois juntos.");
},

/* 02 · ESCOPO */
(pres, pg) => {
  const s = D.slide(pres, "ESCOPO · O QUE A IMPULSIO EXECUTA", pg);
  D.h1(s, "Um canal, uma linha,\nfeitos direito.", { y: 1.55, h: 2.1 });
  rotulo(s, "PRIMEIRA ONDA", L, 4.2, 8.2);
  linhas(pres, s, [
    ["Canal", "Mercado Livre", T_H1],
    ["Linha", "areia de mandioca", T_H1],
    ["Produtos", "2 e 4 kg · fina e grossa"],
    ["Ofertas de teste", "kits e 8 kg"],
    ["Segundo canal", "Shopee, avaliada no mês 4", T_DIM],
  ], { x: L, w: 8.2, y: 4.8, size: 17, step: 0.58, split: 0.45 });
  rotulo(s, "A OPERAÇÃO, TODO MÊS", 10.55, 4.2, 8.2);
  linhas(pres, s, [
    ["Loja oficial e cadastro", "mês 1"],
    ["Conteúdo e análise de concorrência", "contínuo"],
    ["Precificação e promoções", "contínuo"],
    ["Planejamento de envio ao Full", "a partir do mês 3"],
    ["Reunião mensal de resultado", "mensal"],
  ], { x: 10.55, w: 8.2, y: 4.8, size: 17, step: 0.58, split: 0.6 });
  texto(s, "A operação acontece na conta da marca, faturando no CNPJ de vocês. O estoque e a expedição seguem com a fábrica.", L, 8.25, W, 0.6, { size: 16, color: T_DIM });
  D.kicker(pres, s, "Começar estreito e acertar é mais rápido do que começar largo e corrigir.");
  D.source(s, "Escopo conforme reunião de descoberta. Quantidade final de SKUs a confirmar.");
},

/* 03 · CRONOGRAMA */
(pres, pg) => {
  const s = D.slide(pres, "OS PRIMEIROS MESES", pg);
  D.h1(s, "Quatro tempos até\no canal andar sozinho.", { y: 1.55, h: 2.1 });
  const fases = [
    ["MÊS 1", "Setup", "Conta e loja oficial.\nCadastro e conteúdo.\nPrimeiras vendas, postadas na agência dos Correios."],
    ["MESES 2–3", "Reputação", "Preço de entrada para girar.\nMedalha e avaliações.\nColeta do Mercado Livre na fábrica."],
    ["MESES 3–6", "Full", "Envio programado ao CD de Ribeirão Preto.\nEstoque dimensionado pela venda."],
    ["MÊS 6+", "Escala", "Ofertas testadas viram linha.\nMídia paga.\nDecisão sobre a Shopee."],
  ];
  fases.forEach((f, i) => {
    const x = L + i * 4.45;
    D.card(pres, s, x, 4.2, 4.1, 4.4, { transparency: 94 });
    s.addText(f[0], { x: x + 0.36, y: 4.52, w: 3.4, h: 0.34, isTextBox: true, margin: 0,
      fontFace: FM, fontSize: 13, bold: true, color: BLUE_L, charSpacing: 1.3 });
    s.addText(f[1], { x: x + 0.36, y: 4.96, w: 3.4, h: 0.55, isTextBox: true, margin: 0,
      fontFace: FH, fontSize: 24, bold: true, color: T_H1 });
    texto(s, f[2], x + 0.36, 5.65, 3.4, 2.7, { size: 15 });
  });
  texto(s, "O Full é liberado pelo Mercado Livre depois que a conta ganha reputação. Não dá para começar por ele, e o cronograma já conta com isso.", L, 8.85, W, 0.6, { size: 16, color: T_DIM });
  D.kicker(pres, s, "Os primeiros meses são de construção. A projeção a seguir mostra esse custo.");
  D.source(s, "Prazos dependem da liberação do Mercado Livre e do envio dos insumos.");
},

/* 04 · INVESTIMENTO */
(pres, pg) => {
  const p = M.PREMISSAS;
  const s = D.slide(pres, "O INVESTIMENTO", pg, { blue: true });
  D.h1(s, "Um fixo que cobre o time,\num variável que acompanha a venda.", { y: 1.55, h: 2.1 });
  D.card(pres, s, L, 4.25, 8.5, 3.4, { transparency: 92 });
  rotulo(s, "OPERAÇÃO MENSAL", L + 0.5, 4.6, 7.5, { color: BLUE_PALE });
  s.addText(brl(p.fixo), { x: L + 0.5, y: 5.05, w: 7.5, h: 1.1, isTextBox: true, margin: 0,
    fontFace: FH, fontSize: 60, bold: true, color: WHITE });
  texto(s, "Por mês. Analista dedicado, estratégia e reunião mensal de resultado.", L + 0.5, 6.3, 7.5, 1.0, { size: 16 });
  D.card(pres, s, 10.25, 4.25, 8.5, 3.4, { transparency: 92 });
  rotulo(s, "VARIÁVEL", 10.75, 4.6, 7.5, { color: BLUE_PALE });
  s.addText("2%", { x: 10.75, y: 5.05, w: 7.5, h: 1.1, isTextBox: true, margin: 0,
    fontFace: FH, fontSize: 60, bold: true, color: WHITE });
  texto(s, "Só sobre o que passar de R$ 50 mil no mês, sem efeito retroativo. Medido na conta do Mercado Livre de vocês.", 10.75, 6.3, 7.5, 1.0, { size: 16 });
  linhas(pres, s, [
    ["Mês com R$ 40 mil de venda", brl(p.fixo)],
    ["Mês com R$ 100 mil de venda", brl(p.fixo + 0.02 * 50000)],
    ["Mês com R$ 150 mil de venda", brl(p.fixo + 0.02 * 100000) + " · 3,3% da venda", WHITE],
  ], { y: 7.95, size: 18, step: 0.56 });
  D.kicker(pres, s, "O variável existe porque a operação realiza a venda. Ganhamos mais quando vocês vendem mais.", { size: 21 });
  D.source(s, "Baseline zero: a marca não vende hoje com conta própria, então o variável incide sobre o faturamento do canal acima da isenção.");
},

/* 05 · PROJEÇÃO · CENÁRIOS */
(pres, pg) => {
  const s = D.slide(pres, "A PROJEÇÃO", pg);
  D.h1(s, "Três velocidades até\nR$ 150 mil por mês.", { y: 1.55, h: 2.1 });
  s.addChart(pres.charts.LINE, M.CENARIOS.map((c) => ({
    name: c.nome + " · mês " + c.T, labels, values: proj[c.id].meses.map((r) => Math.round(r.receita)),
  })), { ...chartBase, x: L, y: 3.85, w: 11.2, h: 5.3, valAxisLabelFormatCode: "#,##0" });
  rotulo(s, "COMO LER", 13.1, 4.2, 5.65);
  texto(s, "Faturamento mensal do canal, em reais. A diferença entre as curvas é só o tempo para chegar ao mesmo patamar.", 13.1, 4.7, 5.65, 1.8, { size: 16 });
  rotulo(s, "O CENÁRIO BASE", 13.1, 6.7, 5.65);
  linhas(pres, s, [
    ["mês 6", mil(base.meses[5].receita)],
    ["mês 9", mil(base.meses[8].receita)],
    ["mês 12", mil(base.meses[11].receita), WHITE],
  ], { x: 13.1, w: 5.65, y: 7.2, size: 17, step: 0.52, split: 0.45 });
  D.kicker(pres, s, "Isto é cenário, não meta. Faturamento depende de preço, estoque e decisões de vocês.");
  D.source(s, SRC_MODELO);
  s.addNotes("Os três cenários existem porque a velocidade é o que menos controlamos. O acelerado (6 meses) é possível, mas eu não apresentaria como expectativa. O base (12 meses) é a referência desta conversa.\n\nTeto de R$ 150 mil por mês foi o patamar que conversamos para a linha de mandioca. Não projetamos crescimento acima dele.");
},

/* 06 · O RETORNO */
(pres, pg) => {
  const s = D.slide(pres, "O RETORNO", pg);
  D.h1(s, "Quando o canal se paga.", { y: 1.55, h: 1.05 });
  D.sub(s, "Resultado acumulado: margem de contribuição do canal menos o investimento na impulsio.", { y: 2.75, h: 0.55, size: 20, color: T_DIM });
  s.addChart(pres.charts.LINE, M.CENARIOS.map((c) => ({
    name: c.nome, labels, values: proj[c.id].meses.map((r) => Math.round(r.acum)),
  })), { ...chartBase, x: L, y: 3.6, w: 11.2, h: 5.6, valAxisLabelFormatCode: "#,##0" });
  numero(pres, s, 13.1, 3.75, "mês " + base.payback, "RETORNO DO INVESTIMENTO · CENÁRIO BASE", { size: 64, w: 5.65 });
  numero(pres, s, 13.1, 6.15, mil(-base.piorCaixa), "PIOR MOMENTO DE CAIXA · CENÁRIO BASE", { size: 64, w: 5.65, color: AMBER });
  D.kicker(pres, s, "Nos primeiros meses só sai dinheiro. A pergunta certa é quanto, e até quando.");
  D.source(s, SRC_MODELO + " Margem de 15% (5% nos 3 meses de preço de entrada).");
  s.addNotes("Desembolso com a impulsio nos 6 primeiros meses, no cenário base: " + brl(fee6) + ". Mas a venda do período já devolve parte disso, então a exposição real de caixa é o 'pior momento' do slide.\n\nO que NÃO está nesta conta, e precisa ser dito: mídia paga, embalagem nova (clichê de cerca de R$ 6 mil), capital de giro do estoque no Full e a venda que hoje já acontece pelos distribuidores e pode migrar para o canal próprio.");
},

/* 07 · SENSIBILIDADE */
(pres, pg) => {
  const s = D.slide(pres, "A SENSIBILIDADE", pg);
  D.h1(s, "O número que mais pesa\nestá com vocês: a margem.", { y: 1.55, h: 2.1 });
  const cx = [L + 4.2, L + 8.7, L + 13.2];
  M.MARGENS.forEach((mg, j) => {
    s.addText("MARGEM " + Math.round(mg * 100) + "%", { x: cx[j], y: 4.2, w: 4.2, h: 0.4, isTextBox: true,
      margin: 0, align: "center", fontFace: FM, fontSize: 14, bold: true,
      color: mg === M.PREMISSAS.margemBase ? WHITE : BLUE_L, charSpacing: 1.4 });
  });
  M.CENARIOS.forEach((c, i) => {
    const y = 4.85 + i * 1.35;
    texto(s, c.nome, L, y + 0.15, 4.0, 0.5, { font: FH, size: 22, bold: true, color: T_H1 });
    texto(s, "R$ 150 mil no mês " + c.T, L, y + 0.65, 4.0, 0.4, { font: FM, size: 12, color: T_DIM });
    M.MARGENS.forEach((mg, j) => {
      const r = M.projetar(c.T, mg);
      const hl = c.id === "base" && mg === M.PREMISSAS.margemBase;
      D.card(pres, s, cx[j], y, 4.2, 1.15, { transparency: hl ? 85 : 95, line: hl ? BLUE : undefined });
      texto(s, "mês " + r.payback, cx[j], y + 0.12, 4.2, 0.55, { font: FH, size: 26, bold: true, color: hl ? WHITE : T_H1, align: "center" });
      texto(s, "caixa mínimo " + mil(r.piorCaixa), cx[j], y + 0.68, 4.2, 0.35, { font: FM, size: 12, color: T_DIM, align: "center" });
    });
  });
  D.kicker(pres, s, "Com a margem real de vocês na planilha, este quadro vira um número só.");
  D.source(s, SRC_MODELO + " Margem de contribuição = venda − produto − taxa do canal − frete − impostos.");
  s.addNotes("Pedir a margem de contribuição da linha de mandioca, depois de taxa do Mercado Livre (12% a 15%), frete e imposto. Com ela, a planilha fecha o cenário em tempo real.\n\nSe a margem for menor que 10%, a conversa muda: o canal ainda se paga, mas mais devagar, e vale olhar preço e formato de embalagem antes de abrir a loja.");
},

/* 08 · COMO SE MEDE */
(pres, pg) => {
  const s = D.slide(pres, "COMO O TRABALHO É MEDIDO", pg);
  D.h1(s, "Pelo que a operação\ncontrola.", { y: 1.55, h: 2.1 });
  rotulo(s, "OS INDICADORES DO CONTRATO", L, 4.2, 8.2);
  linhas(pres, s, [
    ["Loja oficial no ar", "mês 1"],
    ["Produtos no padrão de ficha", "100% da onda"],
    ["Reputação da conta", "verde"],
    ["Pedidos entregues via Full", "a partir do mês 3"],
    ["Posição na busca “areia de mandioca”", "mensal"],
  ], { x: L, w: 8.2, y: 4.8, size: 17, step: 0.58, split: 0.6 });
  rotulo(s, "PROJEÇÃO NÃO É META", 10.55, 4.2, 8.2, { color: AMBER });
  texto(s, "A projeção mostra o tamanho da aposta. Os indicadores mostram se a operação está fazendo a parte dela.", 10.55, 4.8, 8.2, 1.5, { font: FH, size: 21, bold: true, color: T_H1 });
  texto(s, "Faturamento depende também do preço que vocês aprovam, do estoque disponível e da concorrência. Por isso o contrato mede o que dá para conferir na tela.", 10.55, 6.45, 8.2, 1.6, { size: 17 });
  D.kicker(pres, s, "É mais fácil vender promessa de faturamento. É mais honesto vender o que dá para conferir.");
  D.source(s, "impulsio · operação de canais digitais.");
},

/* 09 · O QUE PRECISAMOS + PRÓXIMO PASSO */
(pres, pg) => {
  const s = D.slide(pres, "O PRÓXIMO PASSO", pg, { blue: true });
  D.h1(s, "O que precisamos\nde vocês para começar.", { y: 1.55, h: 2.1 });
  linhas(pres, s, [
    ["Margem de contribuição da linha", "fecha a projeção", WHITE],
    ["Decisão sobre a marca-mãe da loja", "semana 1"],
    ["Quem cuida da expedição no começo", "semana 1"],
    ["Fotos e ficha técnica dos produtos", "semana 1"],
    ["Contato com o responsável pelo conteúdo", "semana 1"],
  ], { x: L, w: 9.0, y: 4.25, size: 18, step: 0.62, split: 0.62 });
  D.card(pres, s, 11.1, 4.2, 7.65, 4.5, { transparency: 92 });
  rotulo(s, "PARADA DE RELÓGIO", 11.55, 4.55, 6.8, { color: BLUE_PALE });
  texto(s, "O prazo de cada entrega corre a partir do recebimento do insumo, não da data do contrato.", 11.55, 5.05, 6.8, 1.2, { font: FH, size: 21, bold: true, color: WHITE });
  texto(s, "Se um material atrasar, a entrega desloca o mesmo número de dias, com aviso por escrito no momento em que o atraso aparece.", 11.55, 6.45, 6.8, 1.5, { size: 16 });
  D.kicker(pres, s, "impulsio · operação de canais digitais para indústrias e distribuidores", { size: 20 });
  D.source(s, "Proposta válida por 30 dias · " + DATA);
},
];

/* ═════════════════════ ANEXO EUA ═════════════════════ */
const ANEXO = [
(pres, pg) => {
  const s = D.slide(pres, "ANEXO · MERCADO DOS EUA", pg);
  D.h1(s, "Areia biodegradável cresce\nmais rápido que a categoria.", { y: 1.55, h: 2.1 });
  linhas(pres, s, [
    ["Areia para gatos · EUA, mercado total", "US$ 3,8 a 5,7 bi"],
    ["Areia natural · EUA", "US$ 579,7 mi · 6,5% a.a."],
    ["Areia biodegradável · global", "US$ 1,57 bi · 7,9% a.a."],
    ["Areia para gatos · global", "US$ 5,91 bi"],
    ["Donos de gato nos EUA que compram online", "52%"],
  ], { y: 4.3, size: 19, step: 0.64, split: 0.55 });
  texto(s, "Mercado total de varejo, não GMV de marketplace: não se compara com os números do Brasil deste estudo. As consultorias divergem, por isso o total dos EUA aparece em faixa.", L, 7.75, W, 1.0, { size: 16, color: T_DIM });
  D.kicker(pres, s, "Referência de tendência, não plano de canal.");
  D.source(s, "MarkWide Research · Strategyh · Grand View Research · Fortune Business Insights · Global Growth Insights · estimativas 2026.");
},
];

/* ═════════════════════ MONTAGEM ═════════════════════ */
function montar(titulo, slides, arquivo) {
  const pres = D.novo(titulo);
  const n = slides.length;
  slides.forEach((f, i) => f(pres, String(i + 1).padStart(2, "0") + " / " + n));
  return pres.writeFile({ fileName: arquivo }).then((f) => console.log("ok:", f));
}

Promise.all([
  montar("Diagnóstico de canal — areia de mandioca", DIAG, "01-Diagnostico.pptx"),
  montar("Proposta comercial — areia de mandioca", PROP, "02-Proposta-Comercial.pptx"),
  montar("Diagnóstico e proposta — areia de mandioca", [...DIAG, ...PROP], "COMPLETO.pptx"),
  montar("Anexo — mercado dos EUA", ANEXO, "03-Anexo-EUA.pptx"),
]);
