// Gravações com o Chromium de verdade (janela com abas), numa tela virtual: o alerta, a aba nova e o mouse aparecem no vídeo.
// Uso: DISPLAY=:99 node nivel2_gravar.js  (o nivel2.sh liga o Xvfb e o ffmpeg)
const { chromium } = require('@playwright/test');
const { execSync, spawn } = require('child_process');
const S = 'https://the-internet.herokuapp.com';
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
let ff;
const gravar = (n) => { ff = spawn('ffmpeg', ['-loglevel', 'error', '-y', '-f', 'x11grab', '-framerate', '30', '-video_size', '1920x1080', '-i', ':99', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-g', '1', `cg_saida/${n}.mp4`]); return espera(800); };
const parar = async () => { await espera(700); ff.kill('SIGINT'); await new Promise((r) => ff.on('exit', r)); };
const mouse = (x, y) => execSync(`xdotool mousemove --sync ${Math.round(x)} ${Math.round(y)}`);
async function mover(page, sel, passos = 30) {  // o cursor de verdade (xdotool) vai até o elemento
  const b = await page.locator(sel).first().boundingBox(); const o = await page.evaluate(() => [window.screenX + (window.outerWidth - window.innerWidth), window.screenY + (window.outerHeight - window.innerHeight)]);
  const z = 1.5, x = o[0] + (b.x + b.width / 2) * z, y = o[1] + (b.y + b.height / 2) * z;
  const atual = execSync('xdotool getmouselocation --shell').toString(); const X0 = +/X=(\d+)/.exec(atual)[1], Y0 = +/Y=(\d+)/.exec(atual)[1];
  for (let i = 1; i <= passos; i++) { mouse(X0 + (x - X0) * i / passos, Y0 + (y - Y0) * i / passos); await espera(18); }
}
(async () => {
  const b = await chromium.launch({ headless: false, args: ['--window-position=0,0', '--window-size=1920,1080', '--force-device-scale-factor=1.5', '--lang=pt-BR'] });
  const ctx = await b.newContext({ viewport: null }); const page = await ctx.newPage();
  mouse(1700, 900);
  // ---- aula 58: o alerta aparece e trava a página
  await page.goto(`${S}/javascript_alerts`); await espera(1500);
  page.once('dialog', async (d) => { await espera(2600); await d.accept(); });
  await gravar('n58_alerta'); await mover(page, 'text=Click for JS Alert'); await espera(300);
  await page.getByRole('button', { name: 'Click for JS Alert' }).click(); await espera(1800); await parar();
  // ---- aula 59: o link abre outra aba
  await page.goto(`${S}/windows`); await espera(1500);
  await gravar('n59_aba'); await mover(page, 'text=Click Here'); await espera(300);
  const pop = page.waitForEvent('popup'); await page.getByRole('link', { name: 'Click Here' }).click(); const nova = await pop; await nova.waitForLoadState(); await espera(2200);
  await page.bringToFront(); await espera(1500); await nova.bringToFront(); await espera(1200); await parar(); await nova.close();
  // ---- aula 61: o nome só aparece com o mouse em cima
  await page.goto(`${S}/hovers`); await espera(1500); mouse(1700, 900);
  await gravar('n61_hover'); await mover(page, '.figure >> nth=0'); await espera(1800); await mover(page, '.figure >> nth=1', 20); await espera(1500); await mover(page, '.figure >> nth=0', 20); await espera(1200); await parar();
  // ---- aula 63: a tabela muda de ordem quando clica no cabeçalho
  await page.goto(`${S}/tables`); await espera(1500); mouse(1700, 900);
  await gravar('n63_ordem'); await mover(page, '#table1 th:has-text("Due")'); await espera(400); await page.locator('#table1 th:has-text("Due")').click(); await espera(1500);
  await page.locator('#table1 th:has-text("Due")').click(); await espera(1500); await parar();
  await b.close();
})();
