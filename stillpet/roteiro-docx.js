const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
        BorderStyle, PageBreak, Table, TableRow, TableCell, WidthType,
        ShadingType, convertInchesToTwip } = require('docx');
const fs = require('fs');

const INK = "1A1512", BODY = "3D362F", MUTE = "7A7066", HOT = "B23410", AMBER = "8A5C08";
const SERIF = "Georgia", SANS = "Arial";

const gap = (n = 120) => new Paragraph({ spacing: { after: n }, children: [] });

// rótulo pequeno em caixa alta
const label = (txt, color = HOT) => new Paragraph({
  spacing: { before: 260, after: 60 },
  children: [new TextRun({ text: txt.toUpperCase(), bold: true, size: 15,
    font: SANS, color, characterSpacing: 40 })],
});

// número + nome do slide
const slideHead = (num, name) => new Paragraph({
  spacing: { before: 460, after: 100 },
  border: { top: { style: BorderStyle.SINGLE, size: 6, color: "DDD5CB", space: 14 } },
  children: [
    new TextRun({ text: `SLIDE ${num}`, bold: true, size: 17, font: SANS, color: HOT, characterSpacing: 50 }),
    new TextRun({ text: `   ${name}`, bold: true, size: 17, font: SANS, color: MUTE, characterSpacing: 50 }),
  ],
});

// a fala — recuada, com barra à esquerda
const fala = (txt) => new Paragraph({
  spacing: { after: 130, line: 300 },
  indent: { left: convertInchesToTwip(0.28) },
  border: { left: { style: BorderStyle.SINGLE, size: 14, color: HOT, space: 12 } },
  children: [new TextRun({ text: txt, size: 23, font: SERIF, color: INK })],
});

// insight
const insight = (txt) => new Paragraph({
  spacing: { before: 60, after: 160, line: 276 },
  shading: { type: ShadingType.CLEAR, fill: "F7F4F0" },
  indent: { left: convertInchesToTwip(0.16), right: convertInchesToTwip(0.16) },
  children: [new TextRun({ text: txt, size: 19, font: SANS, color: BODY })],
});

const nota = (txt, color = MUTE) => new Paragraph({
  spacing: { after: 140, line: 276 },
  children: [new TextRun({ text: txt, size: 19, font: SANS, color, italics: true })],
});

const pausa = (txt) => new Paragraph({
  spacing: { before: 60, after: 160 },
  children: [new TextRun({ text: "⏸   " + txt, bold: true, size: 19, font: SANS, color: HOT })],
});

// tabela de bifurcação
const bifurcacao = (linhas) => new Table({
  columnWidths: [5400, 3400],
  width: { size: 8800, type: WidthType.DXA },
  borders: {
    top:    { style: BorderStyle.SINGLE, size: 4, color: "DDD5CB" },
    bottom: { style: BorderStyle.SINGLE, size: 4, color: "DDD5CB" },
    left:   { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE },
    insideHorizontal: { style: BorderStyle.SINGLE, size: 2, color: "EDE7DF" },
    insideVertical:   { style: BorderStyle.NONE },
  },
  rows: [
    new TableRow({
      tableHeader: true,
      children: [
        new TableCell({ width: { size: 5400, type: WidthType.DXA },
          margins: { top: 90, bottom: 90, right: 140 },
          children: [new Paragraph({ children: [new TextRun({ text: "SE ELE DISSER",
            bold: true, size: 15, font: SANS, color: MUTE, characterSpacing: 40 })] })] }),
        new TableCell({ width: { size: 3400, type: WidthType.DXA },
          margins: { top: 90, bottom: 90 },
          children: [new Paragraph({ alignment: AlignmentType.RIGHT,
            children: [new TextRun({ text: "CLIQUE EM", bold: true, size: 15,
              font: SANS, color: MUTE, characterSpacing: 40 })] })] }),
      ],
    }),
    ...linhas.map(([a, b]) => new TableRow({ children: [
      new TableCell({ width: { size: 5400, type: WidthType.DXA },
        margins: { top: 110, bottom: 110, right: 140 },
        children: [new Paragraph({ children: [new TextRun({ text: a, size: 19, font: SANS, color: BODY })] })] }),
      new TableCell({ width: { size: 3400, type: WidthType.DXA },
        margins: { top: 110, bottom: 110 },
        children: [new Paragraph({ alignment: AlignmentType.RIGHT,
          children: [new TextRun({ text: b, bold: true, size: 19, font: SANS, color: INK })] })] }),
    ] })),
  ],
});

const doc = new Document({
  creator: "impulsio",
  title: "Roteiro de fala — call StillPet",
  description: "Falas completas, slide a slide, com o insight estratégico de cada momento",
  styles: {
    default: { document: { run: { font: SERIF, size: 21, color: BODY } } },
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: SANS, size: 48, bold: true, color: INK },
        paragraph: { spacing: { after: 140 } } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: SANS, size: 30, bold: true, color: INK },
        paragraph: { spacing: { before: 420, after: 160 } } },
    ],
  },
  sections: [{
    properties: { page: { margin: { top: 1100, right: 1200, bottom: 1000, left: 1200 } } },
    children: [

      new Paragraph({ spacing: { after: 100 }, children: [new TextRun({
        text: "BRIEFING INTERNO  ·  NÃO ENVIAR AO CLIENTE", bold: true, size: 16,
        font: SANS, color: HOT, characterSpacing: 60 })] }),
      new Paragraph({ style: "Title", text: "Roteiro de fala" }),
      new Paragraph({ spacing: { after: 200 }, children: [new TextRun({
        text: "Diagnóstico StillPet  ·  Amazon Brasil  ·  18 slides", size: 24, font: SANS, color: MUTE })] }),
      new Paragraph({
        spacing: { after: 240, line: 300 },
        border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "DDD5CB", space: 14 } },
        children: [new TextRun({ text: "As falas abaixo estão escritas do jeito que se fala, não do jeito que se escreve. Não são para decorar: são para você ler duas vezes antes da reunião e depois improvisar em cima. Abaixo de cada uma está por que ela funciona — é isso que te permite sair do roteiro sem perder o argumento.",
          size: 21, font: SERIF, color: BODY })] }),

      label("A regra que vale mais que todas"),
      fala("Os números estão na tela. Não leia os números."),
      insight("Se o slide mostra 151 e você diz “cento e cinquenta e um produtos”, você virou legenda do seu próprio deck. Diga o que o número significa — ele lê sozinho, e mais rápido que você."),

      // ───────── 00
      slideHead("00", "CAPA"),
      fala("Antes de qualquer coisa, isso aqui não é proposta. É o que eu consegui ver da marca de vocês na Amazon olhando de fora, do jeito que qualquer cliente de vocês veria. Levantei ontem. São trinta capturas de tela, e cada número que eu mostrar hoje tem print com data. Se em algum momento vocês quiserem conferir, a gente abre a Amazon aqui na frente e confere junto."),
      insight("Você estabeleceu a regra do jogo antes de mostrar o primeiro dado. Quem abre dizendo “confere comigo” não precisa defender número nenhum depois — e o Carlos, que conhece o mercado dele melhor que você, acabou de ser convidado para o lado de dentro em vez de ficar na posição de quem vai ser corrigido."),

      // ───────── 01
      slideHead("01", "O MÉTODO"),
      fala("Eu não usei nada de vocês. Nenhum login, nenhuma planilha, nenhum dado interno. Foram quatro buscas na Amazon, trinta prints, vinte e oito fichas de produto abertas uma a uma e trinta e um concorrentes medidos. Um dia de trabalho. E onde eu não consegui confirmar alguma coisa, está escrito que eu não consegui — vocês vão ver isso em dois ou três momentos."),
      insight("Admitir o que você não sabe, logo no começo, é o que faz o resto ser acreditado. É também o que separa você de consultoria que chega com apresentação genérica e número redondo. E é barato: ninguém nunca perdeu uma conta por dizer que não verificou uma coisa."),

      // ───────── 02
      slideHead("02", "O CATÁLOGO"),
      fala("Vocês nunca saíram da Amazon. Esse cadastro que vocês fizeram em dois mil e dezenove continua no ar até hoje. São cento e cinquenta e um produtos, que subiram todos de uma vez e nunca mais foram revisados. E eles seguiram vendendo sozinhos esse tempo todo. Isso não é um catálogo abandonado — é um ativo que ninguém administrou."),
      pausa("Pausa aqui. Deixa o número na tela trabalhar."),
      insight("A escolha da palavra “ativo” em vez de “bagunça” é deliberada. Você está dizendo que existe patrimônio, não que existe erro. Quem ouve “vocês fizeram errado” se defende; quem ouve “vocês têm algo parado” pergunta como destrava."),

      // ───────── 03
      slideHead("03", "O PATRIMÔNIO"),
      fala("Avaliação na Amazon só existe depois que alguém comprou. Então isso aqui é histórico de venda real. Uma coleira de gato de vocês tem oitocentas e quarenta e duas avaliações. Um comedouro tem duzentas e dez. E tem dois produtos com o selo Escolha da Amazon, que a plataforma dá sozinha, para o item que ela decide recomendar naquela busca. Ninguém pediu, ninguém pagou. O problema não é o produto de vocês."),
      insight("Esse slide compra o direito de dizer as coisas difíceis que vêm depois. Você elogiou com dado, não com adjetivo — e a partir daqui, quando você apontar um problema, ele sabe que não é vendedor procurando defeito para vender serviço."),

      // ───────── 04
      slideHead("04", "⑃  OS CINCO VENDEDORES"),
      fala("Hoje tem cinco vendedores anunciando esse catálogo na Amazon. Um é a própria Amazon, que compra de vocês. Os outros quatro são a Cobasi, o Empório Animal, uma loja chamada Only Fish, que é especialista em aquarismo, e outra chamada Paraíso dos Pássaros, especialista em aves. Repara que os dois últimos pegaram justamente as duas linhas de nicho da fábrica de vocês. Isso não é bagunça, é organização. A minha pergunta é de quem."),
      pausa("Faz a pergunta e cala a boca. Espera ele responder."),
      bifurcacao([
        ["“temos política”, “são nossos parceiros”, “a gente aprova”", "Foi decisão nossa"],
        ["“não sabia”, “como assim?”, hesitação, olhar para a filha", "Não sabíamos"],
      ]),
      nota("Na dúvida entre os dois, clique em “Não sabíamos”. Esse caminho abre conversa; o outro assume um conhecimento que ele pode não ter e te deixa sem saída se ele estiver blefando.", MUTE),
      insight("“A pergunta é de quem” é a frase que faz o trabalho. Você não acusou ninguém de nada e mesmo assim colocou a questão do controle na mesa. E note que você elogiou os revendedores antes: chamar a organização deles de organização tira qualquer tom de reclamação."),

      // ───────── 05
      slideHead("05", "A BUY BOX  ·  O SLIDE"),
      fala("Esse produto aqui, a Bica Pedra, tem o selo Escolha da Amazon. Quer dizer que a Amazon escolheu, sozinha, esse produto de vocês para recomendar a quem procura. E quem vende e entrega ele é a Cobasi. A buy box é aquele botão de comprar em um clique — quem está nela leva a maior parte das vendas do produto. As outras ofertas ficam atrás de um link que quase ninguém abre."),
      pausa("Pausa longa. Esse é o slide da reunião. Não preencha o silêncio."),
      label("Se ele defender a Cobasi — e ele provavelmente vai", AMBER),
      fala("Faz todo sentido, ela é cliente de vocês e está fazendo o trabalho dela. A minha pergunta não é se a Cobasi deveria estar vendendo. É se vocês escolheram que fosse ela, nesse produto, a esse preço."),
      insight("Essa é a réplica mais importante do documento inteiro. Se você tratar a Cobasi como vilã, o Carlos te corrige e você perde a mesa — ela é cliente dele. Ao concordar primeiro e só então deslocar a pergunta para controle, você transforma uma objeção em confirmação da sua tese."),

      // ───────── 06
      slideHead("06", "A DISPERSÃO DE PREÇO"),
      fala("Mesmo produto, mesma página. A Amazon vende por dezoito e trinta e dois. Logo abaixo, na mesma ficha, um revendedor oferece o mesmo item por onze e vinte e cinco, com envio feito pela própria Amazon. O revendedor não está atacando a marca de vocês. Ele está fazendo o óbvio com o preço que recebeu. E quem monta os dois preços de origem, um para a Amazon e outro para a distribuição, é a fábrica."),
      nota("Nunca diga que vamos obrigar revendedor a subir preço. Impor preço de revenda com punição é infração à ordem econômica, Lei 12.529/2011, e pode haver advogado na sala.", HOT),
      insight("Você acabou de tirar a culpa do revendedor e devolver o controle para quem está na sua frente. Isso parece contraintuitivo num diagnóstico, mas é o movimento mais forte: cliente que se enxerga como vítima não contrata: espera. Cliente que enxerga a alavanca dentro de casa decide."),

      // ───────── 07
      slideHead("07", "⑃  AS TRÊS MARCAS"),
      fala("Olha esse produto. O selo Still Pet está gravado no molde, no plástico. Agora olha o campo Marca na ficha da Amazon: diz Tudo Pet. E em um terceiro produto a embalagem traz Quick Pet. São três identidades circulando no mesmo catálogo. Para o algoritmo da Amazon isso são três marcas desconhecidas disputando as mesmas buscas — e não uma fábrica com quarenta anos."),
      pausa("Pergunta: “Isso foi decisão de vocês?” e espera."),
      bifurcacao([
        ["“sim, a gente separa por causa da rede”", "Foi escolha"],
        ["“isso foi do jeito que subiu”, “nem lembro”", "Foi como saiu"],
      ]),
      insight("“Quarenta anos” é a única vez que você menciona o tempo de fábrica, e ela cai exatamente onde dói: o patrimônio existe e não está sendo creditado a ninguém. Não é elogio de cortesia — é a medida do que está sendo perdido."),

      // ───────── 08
      slideHead("08", "A BUSCA GENÉRICA"),
      fala("Agora tira o nome de vocês da busca. Quem procura comedouro bebedouro cachorro plástico não digita marca nenhuma — é a busca que traz comprador novo, gente que ainda não conhece vocês. São mais de dois mil resultados. Eu analisei os quarenta e oito primeiros e não achei nenhum produto de vocês. E a Amazon destaca sete marcas no filtro dessa categoria. Nenhuma das três de vocês está lá."),
      insight("Aqui você mudou o eixo: até agora falou de quem vende o produto deles, agora fala de quem nunca vai encontrar o produto deles. É a passagem de “estamos perdendo margem” para “estamos perdendo mercado”, e é o que faz o Carlos parar de pensar em distribuidor e começar a pensar em canal."),

      // ───────── 09
      slideHead("09", "QUEM APARECE NO LUGAR"),
      fala("Olha quem está ocupando os quatro primeiros lugares da busca de comedouro para roedor. Produto importado, marca genérica, entrega em três semanas. Cento e quatro reais. Duzentos e cinquenta e quatro. Mil e cinquenta e cinco. O comparável de vocês custa nove e trinta e seis e chega amanhã. E dois desses importados estão até em categoria errada, e mesmo assim aparecem antes. Vocês não estão perdendo para um produto melhor. Estão perdendo para um cadastro melhor."),
      insight("Esse é o slide que derruba a tese do preço, que foi o que o Carlos verbalizou na primeira call. Ele acha que perde porque o concorrente é mais barato. Os dados mostram o contrário, e o contraste entre nove reais e mil reais faz o argumento sem você precisar defendê-lo."),

      // ───────── 10
      slideHead("10", "O DISTRIBUIDOR"),
      fala("E esse aqui, que aparece na mesma busca com marca própria e com selo de Marca em Destaque da Amazon, é distribuidor de vocês. Noventa e três por cento de avaliações positivas, mais de dez mil pedidos recentes, vendido pela própria Amazon. Mesma prateleira que a de vocês, mesma modalidade de venda. Um construiu marca no canal, o outro não."),
      insight("Isso encerra de vez o argumento “a Amazon não funciona para o nosso tipo de produto”, e encerra sem você precisar dizer a frase. Quem encerra é o próprio distribuidor dele, o que torna a conclusão inatacável."),

      // ───────── 11
      slideHead("11", "A FICHA  ·  VISTA EXPLODIDA"),
      fala("Esse é o comedouro de vocês, aberto peça por peça. Cada peça dessa existe no produto e não existe no cadastro. O selo que está gravado no molde aponta para um campo Marca que diz outra coisa. A capacidade em mililitros está em branco. O material está declarado como, entre aspas, madeira ou plástico. E o anel antiderrapante, que é uma característica real do produto, tem o campo vazio. Vocês fabricam comedouro à prova de formigas. Quem marca esse filtro na Amazon não vê o produto de vocês, porque o campo nunca foi preenchido."),
      insight("Vista explodida é a linguagem nativa de quem vive de injeção plástica — o Carlos lê isso há quarenta anos. E repare que o produto aparece inteiro, nunca quebrado: a mensagem é “o produto está certo, a informação sumiu”. Se você estilhaçasse o produto na tela, estaria usando o patrimônio da família como imagem de fracasso na frente da família."),

      // ───────── 12
      slideHead("12", "⑃  A POSTURA  ·  DECIDE A PROPOSTA"),
      fala("A partir daqui o caminho muda de verdade, e a decisão é de vocês, não minha. Pelo que vocês me contaram, parece que o caminho é organizar quem já vende. Só que eu quero confirmar, porque isso muda tudo que vem depois."),
      pausa("Deixa os dois cartões na tela e fica quieto. Essa decisão é deles."),
      bifurcacao([
        ["“não quero brigar com quem me compra”, “meu medo é o distribuidor”", "Organizar quem já vende"],
        ["“eu também quero vender”, “se não for eu vai ser outro”", "Vender direto também"],
      ]),
      label("A provocação para soltar aqui"),
      fala("Vocês me falaram uma coisa na primeira conversa que eu não esqueci: que tem muito produto de fábrica que não vende porque o distribuidor não quer, ou porque ele compra do concorrente. Aqueles produtos — quantos são?"),
      fala("Porque esses não queimam ninguém. A rede já disse não a eles. É uma terceira lista, que não pertence a nenhum dos dois caminhos, e é por onde dá para começar a testar venda direta sem conflito nenhum."),
      nota("Ressalva que precisa ser dita junto, senão desmonta no terceiro mês: produto que o distribuidor recusa pode ser produto que ninguém quer. A lista tem que ser filtrada contra demanda real de marketplace, não só contra “o distribuidor disse não”.", AMBER),
      label("Se alguém levantar o terceiro CNPJ"),
      fala("Eu não acho que precise. A distribuidora de vocês já vende essa marca, e marketplace é distribuição — não é canal novo, é mais uma modalidade do que ela já faz. E se o medo é a Cobasi perceber, ela percebe em uma semana: a marca é a mesma, o produto é o mesmo, a foto é a mesma. CNPJ novo não esconde nada de quem conhece o mercado. O que separa canal é sortimento, não razão social."),
      insight("Você acabou de tirar da mesa um projeto de meses — abertura de empresa, contador, responsável legal — que não resolveria o problema que ele foi inventado para resolver. Consultoria média venderia esse projeto. Recusar trabalho que não serve é a credencial mais cara que existe, e é de graça."),

      // ───────── 13
      slideHead("13", "O QUE ESTÁ PARADO"),
      fala("Eu não tenho acesso ao faturamento de vocês, então eu não vou inventar quanto isso custa. O que eu posso mostrar é o que dá para ver na tela. Tem um produto de vocês com quatro vírgula oito estrelas e cento e oitenta e duas avaliações que está sem buy box — quer dizer, com venda perto de zero, não reduzida. Treze dos vinte e oito produtos que eu documentei estão em ruptura ou sob encomenda. E tem dezenove erros de cadastro mapeados, dois deles críticos."),
      insight("Você acabou de recusar o número fácil. Toda agência nesse slide chuta um valor de perda mensal, e o dono sabe que é chute. Ao dizer “não vou inventar”, tudo que você falar depois vale mais — inclusive o preço, daqui a duas semanas."),

      // ───────── 14
      slideHead("14", "A CALCULADORA"),
      fala("Esse número aqui quem coloca são vocês. Vocês me contaram que teve um produto que chegou a ser sessenta, setenta por cento da venda de vocês na Amazon, e que depois caiu. Qual era o faturamento mensal dele no melhor momento?"),
      pausa("Digita o que ele falar. Deixa a tela calcular. Não comente o resultado — ele vai comentar."),
      insight("Esse é o único número emocional da apresentação, e é ele quem diz, não você. Número que o cliente digita ele não contesta. E o silêncio depois do resultado é o momento de maior poder da reunião inteira: quem fala primeiro perde."),

      // ───────── 15
      slideHead("15", "O QUE FAZEMOS"),
      fala("A ordem aqui importa mais que a lista. Primeiro governança de marca, que é resolver a arquitetura dessas três marcas, Brand Registry, buy box. Depois catálogo e conteúdo, que é ficha técnica, atributo de filtro, categoria certa. Aí sim arquitetura de canais, que é o papel de cada canal, sortimento, credenciamento. E mídia paga entra por último. Tráfego pago para uma ficha incompleta, com doze ofertas concorrendo na mesma página, vira desconto. Não vira venda."),
      insight("Colocar mídia por último contraria o que a maior parte do mercado vende, e é exatamente por isso que funciona. Você está dizendo que não vai cobrar por acelerador enquanto o carro não anda — e quem escuta entende que você está protegendo o dinheiro dele, não o seu."),

      // ───────── 16
      slideHead("16", "PELO QUE RESPONDEMOS"),
      fala("E aqui está o que a gente não promete. Eu não prometo meta de faturamento. Faturamento depende de preço, de estoque e de decisão de vocês, e essas três coisas eu não controlo. O que eu controlo e vou responder por isso é buy box, ficha no padrão, vendedor com critério, ruptura, erro de cadastro. Tudo isso dá para medir na tela, e a linha de partida foi medida no dia vinte e três de setembro."),
      insight("Essa é a segunda recusa da apresentação, e duas recusas fazem tudo que você afirma valer mais. Agência promete crescimento e entrega explicação no terceiro mês; operadora se compromete com o que dá para auditar. É a frase que define o que a impulsio é, e ela é mais forte dita como limite do que dita como proposta."),

      // ───────── 17
      slideHead("17", "FECHO"),
      fala("Três coisas eu não consegui descobrir sozinho, e são elas que mudam o desenho do trabalho. Primeira: qual era o produto que representava sessenta, setenta por cento da venda de vocês na Amazon. Segunda: se essa separação entre as três marcas foi decisão comercial de vocês. E terceira: qual preço a fábrica pratica com a Amazon e qual pratica com a distribuição."),
      pausa("Faz as três perguntas e para. Não emenda no fecho."),
      fala("Esse diagnóstico é de vocês, decidindo trabalhar comigo ou não. A planilha com as vinte e oito fichas, os dezenove erros e os trinta e um concorrentes vai junto."),
      insight("Terminar entregando em vez de pedindo é o fecho mais difícil de recusar. E a terceira pergunta é a que mais destrava: sem ela você leva um diagnóstico de sintomas, com ela leva a causa — que é a diferença entre uma reunião boa e um contrato."),

      new Paragraph({ children: [new PageBreak()] }),

      new Paragraph({ style: "Heading1", text: "O que nunca dizer" }),
      new Paragraph({ spacing: { after: 130, line: 288 }, children: [new TextRun({
        text: "Qualquer valor de proposta.  ", bold: true, size: 21, font: SANS, color: INK }),
        new TextRun({ text: "Preço é a segunda reunião, em arquivo separado. Os valores citados na call de descoberta foram cotados para 3P, e o que eles pediram foi 1P na Amazon, que não foi precificado.", size: 21, font: SERIF, color: BODY })] }),
      new Paragraph({ spacing: { after: 130, line: 288 }, children: [new TextRun({
        text: "Que vamos controlar ou impor preço de revendedor.  ", bold: true, size: 21, font: SANS, color: INK }),
        new TextRun({ text: "Lei 12.529/2011. Monitorar e orientar posicionamento: pode. Impor com punição: não.", size: 21, font: SERIF, color: BODY })] }),
      new Paragraph({ spacing: { after: 130, line: 288 }, children: [new TextRun({
        text: "Qualquer número que não esteja na tela com print.  ", bold: true, size: 21, font: SANS, color: INK }),
        new TextRun({ text: "É a regra que sustenta os outros trinta números da apresentação.", size: 21, font: SERIF, color: BODY })] }),

      new Paragraph({ style: "Heading1", text: "Os três momentos de calar a boca" }),
      new Paragraph({ spacing: { after: 110 }, children: [new TextRun({ text: "1.  Depois da buy box da Cobasi, no slide 05.", size: 21, font: SERIF, color: BODY })] }),
      new Paragraph({ spacing: { after: 110 }, children: [new TextRun({ text: "2.  Depois de cada pergunta de bifurcação: slides 04, 07 e 12.", size: 21, font: SERIF, color: BODY })] }),
      new Paragraph({ spacing: { after: 160 }, children: [new TextRun({ text: "3.  Depois que a calculadora mostra o número, no slide 14.", size: 21, font: SERIF, color: BODY })] }),
      insight("Quem fala primeiro depois do silêncio perde a mesa. O impulso vai ser preencher o vazio — não preencha. O desconforto é do outro lado, e é ele que faz a pergunta seguinte aparecer."),

      new Paragraph({ style: "Heading1", text: "Se travar" }),
      new Paragraph({ spacing: { after: 140, line: 288 }, children: [new TextRun({
        text: "Aperta a seta para a direita. O deck anda inteiro sem nenhuma escolha, as bifurcações não bloqueiam nada, e a tecla F entra em tela cheia. O link não vai antes da reunião: se ela abrir antes, lê os dois caminhos de cada pergunta e a mecânica perde o sentido.",
        size: 21, font: SERIF, color: BODY })] }),

      new Paragraph({
        spacing: { before: 400 },
        border: { top: { style: BorderStyle.SINGLE, size: 6, color: "DDD5CB", space: 14 } },
        children: [new TextRun({ text: "impulsio  ·  Diagnóstico de canal StillPet  ·  Amazon Brasil  ·  23 de setembro de 2026",
          size: 17, font: SANS, color: MUTE })] }),
    ],
  }],
});

Packer.toBuffer(doc).then(b => {
  fs.writeFileSync("Roteiro-de-fala-StillPet.docx", b);
  console.log("ok", b.length, "bytes");
});
