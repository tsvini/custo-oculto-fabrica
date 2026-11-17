const { chromium } = require('playwright');
// Uso: node tests/flowdesk/ia.js [url-base]
// Módulo 9: a página IA (revisar casos, o teste da IA, hipótese e prova) e o teste consertado conferido no fork (simulado).
const U = process.argv[2] || 'http://localhost:8765/';
let falhas = 0; const ok = (c, m) => { console.log((c ? 'OK   ' : 'FALHA ') + m); if (!c) falhas++; };
const b64 = (s) => Buffer.from(s).toString('base64');
const fork = {
  '': { fork: true, default_branch: 'main', parent: { full_name: 'tsvini/vida-de-qa-regressivo' } },
  '/actions/runs?per_page=100': { workflow_runs: [] },
  '/git/trees/main?recursive=1': { tree: ['cypress/e2e/ia/duplicado.feature', 'cypress/support/step_definitions/ia.steps.js'].map((path) => ({ path })) },
  '/contents/cypress/e2e/ia/duplicado.feature?ref=main': { content: b64('Funcionalidade: Chamado em dobro\n  Então só um chamado novo aparece na lista\n') },
  '/contents/cypress/support/step_definitions/ia.steps.js?ref=main': { content: b64("cy.findByRole('button', { name: nome }).dblclick();\n") },
};
const fecha = async (p) => { for (let i = 0; i < 6; i++) { if (await p.isVisible('[data-test=fechar-conquista]').catch(() => false)) { await p.click('[data-test=fechar-conquista]'); await p.waitForTimeout(250); } else break; } };
(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } }); const p = await ctx.newPage();
  const erros = []; p.on('pageerror', (e) => erros.push(e.message));
  await ctx.route('https://api.github.com/**', (r) => { const u = new URL(r.request().url()); const m = u.pathname.match(/^\/repos\/[^/]+\/[^/]+(.*)$/); const k = (m ? m[1] : '') + u.search;
    const v = fork[k]; return v === undefined ? r.fulfill({ status: 404, body: '{}' }) : r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(v) }); });
  await p.goto(U + 'index.html?save=m8ep59'); await p.waitForURL(/dashboard/); await p.waitForTimeout(300);
  ok(!(await p.isVisible('[data-test=menu-ia]')), 'sem o menu IA antes de fechar o módulo 8');
  await p.goto(U + 'index.html?save=m9ep61'); await p.waitForURL(/dashboard/); await p.waitForTimeout(300); await fecha(p);
  ok(await p.isVisible('[data-test=menu-ia]'), 'menu IA no módulo 9');
  await p.goto(U + 'ia.html'); ok((await p.locator('[data-test^=ia-caso-]').count()) === 12, 'os 12 casos da IA');
  await p.check('[data-test=ia-caso-7]'); await p.check('[data-test=ia-caso-3]'); await p.click('[data-test=ia-conferir-62]'); await p.waitForTimeout(400);
  ok(await p.isVisible('[data-test=toast-erro]'), 'marcar caso do card como inventado não passa');
  await p.goto(U + 'ia.html'); await p.check('[data-test=ia-caso-7]'); await p.check('[data-test=ia-caso-10]'); await p.fill('[data-test=ia-faltou]', 'no máximo 3 fotos por chamado'); await p.click('[data-test=ia-conferir-62]');
  await p.waitForTimeout(1200); await fecha(p); await p.goto(U + 'ia.html'); await p.waitForTimeout(300); await fecha(p);
  ok(await p.isVisible('[data-test=ia-ep62].feito'), 'conquista do EP62');
  for (const k of ['espera', 'classe', 'gherkin']) await p.check(`[data-test=ia-problema-${k}]`); await p.click('[data-test=ia-conferir-63]'); await p.waitForTimeout(400);
  ok(await p.isVisible('[data-test=toast-erro]'), 'problema errado no teste da IA não passa');
  await p.goto(U + 'ia.html'); for (const k of ['espera', 'classe', 'mensagem']) await p.check(`[data-test=ia-problema-${k}]`); await p.click('[data-test=ia-conferir-63]'); await p.waitForTimeout(1200); await fecha(p);
  await p.goto(U + 'ia.html'); await p.waitForTimeout(300); await fecha(p);
  ok(await p.isVisible('[data-test=ia-item-problemas].ok') && !(await p.isVisible('[data-test=ia-ep63].feito')), 'EP63 espera o teste do fork');
  await p.fill('[data-test=ia-fork]', 'aluno/vida-de-qa-regressivo'); await p.click('[data-test=ia-conferir-fork]'); await p.waitForTimeout(1500); await fecha(p);
  await p.goto(U + 'ia.html'); await p.waitForTimeout(300); await fecha(p);
  ok(await p.isVisible('[data-test=ia-ep63].feito'), 'conquista do EP63 com o fork');
  await p.check('[data-test=ia-hipotese-codigo]'); await p.check('[data-test=ia-prova-volume]'); await p.click('[data-test=ia-conferir-65]'); await p.waitForTimeout(400);
  ok(await p.isVisible('[data-test=toast-erro]'), 'hipótese errada não passa');
  await p.goto(U + 'ia.html'); await p.check('[data-test=ia-hipotese-trafego]'); await p.check('[data-test=ia-prova-usuario]'); await p.click('[data-test=ia-conferir-65]'); await p.waitForTimeout(1200); await fecha(p);
  await p.goto(U + 'ia.html'); await p.waitForTimeout(300); await fecha(p);
  ok(await p.isVisible('[data-test=ia-ep65].feito'), 'conquista do EP65');
  ok(/ 5960 /.test(' ' + (await p.textContent('[data-test=xp]')).split('/')[0] + ' ') || /5960/.test(await p.textContent('[data-test=xp]')), 'XP segura antes do pleno: ' + (await p.textContent('[data-test=xp]')));
  ok(erros.length === 0, 'sem erro de JavaScript' + (erros.length ? ': ' + erros[0] : ''));
  await b.close(); console.log(falhas ? `\n${falhas} FALHA(S)` : '\nTUDO OK'); process.exit(falhas ? 1 : 0);
})();
