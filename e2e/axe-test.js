const { chromium } = require('playwright');
const { injectAxe, checkA11y, getAxeResults } = require('axe-playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const url = process.env.URL || 'http://localhost:3000/trust';
  console.log('Scanning', url);
  await page.goto(url, { waitUntil: 'networkidle' });
  await injectAxe(page);
  // run a11y checks and output results
  const results = await page.accessibility.snapshot(); // basic snapshot
  try {
    await checkA11y(page, null, { detailedReport: true, detailedReportOptions: { html: true } });
    console.log('A11y checks passed (no violations found).');
  } catch (err) {
    console.error('Accessibility violations detected:');
    console.error(err);
    // write report file
    const fs = require('fs');
    fs.writeFileSync('e2e/axe-report.json', JSON.stringify(err, null, 2));
    process.exit(2);
  } finally {
    await browser.close();
  }
})().catch(e => { console.error(e); process.exit(1); });
