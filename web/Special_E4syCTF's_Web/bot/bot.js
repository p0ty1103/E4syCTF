const puppeteer = require('puppeteer');

const APP_URL = 'http://localhost:2943';
const ADMIN_PASSWORD = 'SuPeRsEcReTaDmInPaSsWoRd1234';
const VISIT_INTERVAL = 30000;

const visitAdminPage = async () => {
  console.log('[BOT] Starting visit...');
  let browser;
  try {
    browser = await puppeteer.launch({
      headless: 'new', 
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-gpu',
        '--js-flags=--noexpose_wasm'
      ],
    });

    const context = await browser.createIncognitoBrowserContext();
    const page = await context.newPage();

    await page.goto(`${APP_URL}/login`, { waitUntil: 'networkidle2' });
    console.log('[BOT] On login page.');

    await page.type('input[name="username"]', 'admin');
    await page.type('input[name="password"]', ADMIN_PASSWORD);
    
    await Promise.all([
      page.click('button[type="submit"]'),
      page.waitForNavigation({ waitUntil: 'networkidle2' })
    ]);

    if (page.url() !== `${APP_URL}/admin`) {
      throw new Error('Login failed or redirect was incorrect.');
    }
    console.log('[BOT] Login successful. On admin page. Flag cookie is set.');
    
    await new Promise(resolve => setTimeout(resolve, 3000));

    console.log('[BOT] Visit finished successfully.');

  } catch (e) {
    console.error('[BOT] An error occurred:', e.message);
  } finally {
    if (browser) {
      await browser.close();
    }
  }
};

console.log(`[BOT] Bot started. Visiting admin page every ${VISIT_INTERVAL / 1000} seconds.`);
setInterval(visitAdminPage, VISIT_INTERVAL);
visitAdminPage();
