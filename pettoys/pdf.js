// Exporta a proposta para PDF, um slide por página (16:9). Uso: node pdf.js <index.html> <dir_png>
const { chromium } = require('playwright');
(async()=>{
  const b=await chromium.launch();
  const p=await b.newPage({viewport:{width:1600,height:900},deviceScaleFactor:1.5});
  await p.goto('file://'+process.argv[2]);
  await p.addStyleTag({content:`.rail,.topbar{display:none!important}
    .slide.on > *{animation:none!important}
    .tbl{overflow:visible} .tbl td{padding:2px 10px} .tbl th{padding:4px 10px}`});
  const n=await p.evaluate(()=>document.querySelectorAll('.slide').length);
  for(let i=0;i<n;i++){
    await p.waitForTimeout(150);
    await p.screenshot({path:`${process.argv[3]}/p${String(i+1).padStart(2,'0')}.png`});
    await p.keyboard.press('ArrowRight');
  }
  await b.close();
})();
