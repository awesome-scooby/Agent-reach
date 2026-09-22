const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch({ } }).catch(()=>chromium.launch());
  const p = await b.newPage();
  await p.goto('file://' + __dirname + '/Pregnancy-Optimisation-Plan.html', { waitUntil: 'load' });
  await p.pdf({ path: __dirname + '/Pregnancy-Optimisation-Plan-Perth.pdf', format: 'A4', printBackground: true,
    displayHeaderFooter: true, headerTemplate: '<div></div>',
    footerTemplate: '<div style="font-size:7px;width:100%;text-align:center;color:#777;">Pregnancy Optimisation Plan · Perth WA · Sept 2026 · page <span class="pageNumber"></span> of <span class="totalPages"></span></div>',
    margin: { top: '16mm', bottom: '18mm', left: '14mm', right: '14mm' } });
  await b.close();
})();
