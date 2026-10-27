/* Modelo de projeção — fonte única dos números do deck e da planilha.
 * Tudo aqui é premissa editável. Nada disso é meta: é cenário. */

const PREMISSAS = {
  alvo: 150000,          // faturamento mensal do canal citado na call (R$)
  fixo: 2900,            // fee mensal citado na call (R$)
  variavel: 0.02,        // 2% sobre o que passar da isenção
  isencao: 50000,        // até R$ 50 mil/mês não há variável
  mesesPenetracao: 3,    // meses com preço de entrada para ganhar reputação
  margemPenetracao: 0.05,// margem de contribuição nesses meses
  margemBase: 0.15,      // margem de contribuição depois (A CONFIRMAR com o cliente)
  curva: 1.6,            // formato da rampa: f(m) = (m / T) ^ curva
  horizonte: 24,
};

/* Cenários: mês em que o canal atinge o faturamento-alvo */
const CENARIOS = [
  { id: "conservador", nome: "Conservador", T: 18 },
  { id: "base", nome: "Base", T: 12 },
  { id: "acelerado", nome: "Acelerado", T: 6 },
];

const MARGENS = [0.10, 0.15, 0.20];

function projetar(T, margem = PREMISSAS.margemBase, p = PREMISSAS) {
  let acum = 0, payback = null, piorCaixa = 0, feeAcum = 0;
  const meses = [];
  for (let m = 1; m <= p.horizonte; m++) {
    const receita = p.alvo * Math.min(1, Math.pow(m / T, p.curva));
    const mc = receita * (m <= p.mesesPenetracao ? p.margemPenetracao : margem);
    const fee = p.fixo + p.variavel * Math.max(0, receita - p.isencao);
    acum += mc - fee;
    feeAcum += fee;
    piorCaixa = Math.min(piorCaixa, acum);
    if (payback === null && acum >= 0) payback = m;
    meses.push({ m, receita, mc, fee, acum });
  }
  return { meses, payback, piorCaixa, feeAcum, acum };
}

module.exports = { PREMISSAS, CENARIOS, MARGENS, projetar };

if (require.main === module) {
  for (const c of CENARIOS) for (const mg of MARGENS) {
    const r = projetar(c.T, mg);
    console.log(c.nome.padEnd(12), (mg * 100) + "%", "payback mês", r.payback,
      "pior caixa", Math.round(r.piorCaixa), "acum 24m", Math.round(r.acum));
  }
}
