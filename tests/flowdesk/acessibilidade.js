const { chromium } = require('playwright');
// Uso: node tests/flowdesk/acessibilidade.js [url-base]
// Módulo 8: tela nova do novo chamado, bugs de acessibilidade e de tempo, e a página Acessibilidade (fork simulado).
const U = process.argv[2] || 'http://localhost:8765/';
let falhas = 0; const ok = (c, m) => { console.log((c ? 'OK   ' : 'FALHA ') + m); if (!c) falhas++; };
const b64 = (s) => Buffer.from(s).toString('base64');
const fork = {
  '': { fork: true, default_branch: 'main', parent: { full_name: 'tsvini/vida-de-qa-regressivo' } },
  '/actions/runs?per_page=100': { workflow_runs: [] },
  '/git/trees/main?recursive=1': { tree: ['cypress/e2e/a/teclado.feature', 'cypress/e2e/a/lista.feature', 'cypress/support/e2e.js', 'cypress/fixtures/orcamento.json'].map((path) => ({ path })) },
  '/contents/cypress/e2e/a/teclado.feature?ref=main': { content: b64('Quando eu aperto Tab\nEntão o foco está no cliente\n') },
  '/contents/cypress/e2e/a/lista.feature?ref=main': { content: b64('Quando eu abro a lista com 2000 chamados\nEntão a lista aparece em menos de 2000 milissegundos\n') },
  '/contents/cypress/support/e2e.js?ref=main': { content: b64("cy.findByRole('button')\nCypress.Commands.add('injectAxe')\ncy.checkA11y()\n") },
};
(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 1280, height: 800 } }); const p = await ctx.newPage();
  const erros = []; p.on('pageerror', (e) => erros.push(e.message));
  await ctx.route('https://api.github.com/**', (r) => { const u = new URL(r.request().url()); const m = u.pathname.match(/^\/repos\/[^/]+\/[^/]+(.*)$/); const k = (m ? m[1] : '') + u.search;
    const v = fork[k]; return v === undefined ? r.fulfill({ status: 404, body: '{}' }) : r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(v) }); });
  await p.goto(U + 'index.html?save=m4'); await p.waitForURL(/dashboard/);
  await p.goto(U + 'novo-chamado.html'); ok(/Criar chamado/.test(await p.textContent('[data-test=criar-chamado]')), 'antes do módulo 8: botão com texto');
  await p.goto(U + 'index.html?save=m8ep54'); await p.waitForURL(/dashboard/); await p.waitForTimeout(300);
  ok(await p.isVisible('[data-test=menu-acessibilidade]'), 'menu Acessibilidade no módulo 8');
  await p.goto(U + 'novo-chamado.html?regressao='); ok((await p.getAttribute('[data-test=criar-chamado]', 'aria-label')) === 'Enviar chamado', 'botão de ícone com nome Enviar chamado');
  await p.focus('#titulo'); const seq = []; for (let i = 0; i < 3; i++) { await p.keyboard.press('Tab'); seq.push(await p.evaluate(() => document.activeElement.dataset.test)); }
  ok(seq.join() === 'descricao,cliente,criar-chamado', 'ordem do Tab: descrição, cliente, enviar');
  await p.goto(U + 'novo-chamado.html?regressao=rotulo'); ok((await p.getAttribute('[data-test=criar-chamado]', 'aria-label')) === null, 'regressao=rotulo tira o nome do botão');
  await p.goto(U + 'novo-chamado.html?regressao=ordem'); await p.focus('#titulo'); await p.keyboard.press('Tab'); await p.keyboard.press('Tab');
  ok(await p.evaluate(() => document.activeElement.tagName === 'A'), 'regressao=ordem desvia o foco pro link');
  await p.goto(U + 'chamados.html?regressao=&massa=2000'); ok((await p.locator('[data-test=linha-chamado]').count()) === 20 && await p.isVisible('[data-test=mostrar-mais]'), 'lista grande mostra 20 por vez');
  await p.click('[data-test=mostrar-mais]'); ok((await p.locator('[data-test=linha-chamado]').count()) === 40, 'mostrar mais traz mais 20');
  await p.goto(U + 'chamados.html?regressao=cor'); ok(!(await p.isVisible('.stx')), 'regressao=cor deixa só a bolinha');
  await p.goto(U + 'acessibilidade.html?regressao='); await p.fill('[data-test=ac-fork]', 'aluno/vida-de-qa-regressivo'); await p.click('[data-test=ac-conferir]'); await p.waitForTimeout(1500);
  for (let i = 0; i < 8; i++) { if (await p.isVisible('[data-test=fechar-conquista]').catch(() => false)) { await p.click('[data-test=fechar-conquista]'); await p.waitForTimeout(300); } else break; }
  await p.goto(U + 'acessibilidade.html'); await p.waitForTimeout(300);
  for (const k of [54, 55, 56, 58, 59]) ok(await p.isVisible(`[data-test=ac-ep${k}].feito`), `conquista do EP${k}`);
  ok(erros.length === 0, 'sem erro de JavaScript' + (erros.length ? ': ' + erros[0] : ''));
  await b.close(); console.log(falhas ? `\n${falhas} FALHA(S)` : '\nTUDO OK'); process.exit(falhas ? 1 : 0);
})();
