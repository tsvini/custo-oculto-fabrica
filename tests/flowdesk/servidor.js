const { chromium } = require('playwright');
// Uso: node tests/flowdesk/servidor.js [url-base]
// Missões do módulo 6: o FlowDesk lê os testes de API do fork pela API pública do GitHub (aqui, simulada).
const U = process.argv[2] || 'http://localhost:8765/';
let falhas = 0; const ok = (c, m) => { console.log((c ? 'OK   ' : 'FALHA ') + m); if (!c) falhas++; };
const b64 = (s) => Buffer.from(s).toString('base64');
const F1 = '# language: pt\n@api\nFuncionalidade: x\n  Cenário: a\n    Quando eu peço o chamado 1\n    E o título é "Forno não liga"\n    E o cliente é "Panificadora Sol"\n  Cenário: b\n    Quando eu crio pelo servidor um chamado da "Panificadora Sol" com prioridade "urgente"\n    Então a prioridade guardada é "alta"\n  Esquema do Cenário: c\n    Então o servidor responde 400\n    Exemplos:\n      | a |\n';
const F2 = '# language: pt\nFuncionalidade: r\n  Cenário: a\n    Então o servidor responde 401\n  Cenário: b\n    Então o servidor responde 403\n';
const F3 = '# language: pt\nFuncionalidade: s\n  Cenário: a\n    E que existem estes chamados:\n';
const WF = 'name: Smoke\non: pull_request\njobs:\n  s:\n    steps:\n      - uses: cypress-io/github-action@v6\n        with:\n          start: npm run api\n';
const fork = (completo) => ({
  '': { fork: true, default_branch: 'main', parent: { full_name: 'tsvini/vida-de-qa-regressivo' } },
  '/actions/runs?per_page=100': { workflow_runs: completo ? [{ id: 1, name: 'Smoke', path: '.github/workflows/smoke.yml', event: 'pull_request', conclusion: 'success', head_branch: 'api' }] : [] },
  '/git/trees/main?recursive=1': { tree: [{ path: 'cypress/e2e/fumaca.feature' }] },
  '/contents/cypress/e2e/fumaca.feature?ref=main': { content: b64('# language: pt\nFuncionalidade: f\n') },
  '/git/trees/api?recursive=1': completo ? { tree: ['cypress/e2e/api/chamados.feature', 'cypress/e2e/api/rascunho.feature', 'cypress/e2e/chamados/semana.feature', 'cypress/fixtures/contrato-chamado.json', '.github/workflows/smoke.yml'].map((path) => ({ path })) } : null,
  '/contents/cypress/e2e/api/chamados.feature?ref=api': { content: b64(F1) },
  '/contents/cypress/e2e/api/rascunho.feature?ref=api': { content: b64(F2) },
  '/contents/cypress/e2e/chamados/semana.feature?ref=api': { content: b64(F3) },
  '/contents/.github/workflows/smoke.yml?ref=api': { content: b64(WF) },
});
(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } }); const p = await ctx.newPage();
  const erros = []; p.on('pageerror', (e) => erros.push(e.message));
  let base = fork(false);
  await ctx.route('https://api.github.com/**', (r) => { const u = new URL(r.request().url()); const m = u.pathname.match(/^\/repos\/[^/]+\/[^/]+(.*)$/); const k = (m ? m[1] : '') + u.search;
    const v = base[k]; return v === undefined || v === null ? r.fulfill({ status: 404, body: '{}' }) : r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(v) }); });
  await p.goto(U + 'index.html?save=m5ep36'); await p.waitForURL(/dashboard/);
  ok(!(await p.isVisible('[data-test=menu-servidor]')), 'menu Servidor escondido antes de fechar o módulo 5');
  await p.goto(U + 'servidor.html'); ok(await p.isVisible('[data-test=sv-fechado]'), 'Servidor fechado antes do módulo 6');
  await p.goto(U + 'index.html?save=m6ep39'); await p.waitForURL(/dashboard/); await p.waitForTimeout(400);
  ok(await p.isVisible('[data-test=menu-servidor]'), 'menu Servidor aparece no módulo 6');
  ok(/EP39/.test(await p.textContent('[data-test=missao-atual]')), 'missão do EP39 no lado');
  await p.goto(U + 'servidor.html');
  await p.fill('[data-test=sv-fork]', 'aluno/vida-de-qa-regressivo'); await p.click('[data-test=sv-conferir]'); await p.waitForTimeout(1200);
  ok(!(await p.isVisible('[data-test=sv-ep39] .rg-cx.ok')), 'fork sem testes de API: nada conferido');
  base = fork(true);
  await p.click('[data-test=sv-conferir]'); await p.waitForTimeout(1500);
  for (let i = 0; i < 10; i++) { if (await p.isVisible('[data-test=fechar-conquista]').catch(() => false)) { await p.click('[data-test=fechar-conquista]'); await p.waitForTimeout(350); } else break; }
  await p.goto(U + 'servidor.html');
  for (const k of ['lista', 'urgente', 'erros', 'token', 'semana', 'contrato', 'apiPipeline']) ok(await p.isVisible(`[data-test=sv-item-${k}].ok`), `item ${k} conferido`);
  for (const ep of [39, 40, 41, 42, 43, 44]) ok(await p.isVisible(`[data-test=sv-ep${ep}].feito`), `conquista do EP${ep}`);
  const xp = await p.evaluate(() => xpDe()); ok(xp < 6000, 'XP ainda abaixo de pleno (' + xp + ')');
  await p.goto(U + 'aula.html?ep=42'); await p.waitForTimeout(300);
  ok(erros.length === 0, 'sem erro de JavaScript' + (erros.length ? ': ' + erros[0] : ''));
  await b.close(); console.log(falhas ? `\n${falhas} FALHA(S)` : '\nTUDO OK'); process.exit(falhas ? 1 : 0);
})();
