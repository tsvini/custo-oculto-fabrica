const { chromium } = require('playwright');
// Uso: node tests/flowdesk/incidente.js [url-base]
// Módulo 7: a página Incidente (log, investigação, relatório) e os testes do fork (API do GitHub simulada).
const U = process.argv[2] || 'http://localhost:8765/';
let falhas = 0; const ok = (c, m) => { console.log((c ? 'OK   ' : 'FALHA ') + m); if (!c) falhas++; };
const b64 = (s) => Buffer.from(s).toString('base64');
const FEAT = '# language: pt\nFuncionalidade: Sessão\n  Cenário: a\n    Então o token vale pelo menos 30 minutos\n  Cenário: b\n    Quando eu entro marcando lembrar de mim\n    Então o token vale pelo menos 30 dias\n';
const fork = {
  '': { fork: true, default_branch: 'main', parent: { full_name: 'tsvini/vida-de-qa-regressivo' } },
  '/actions/runs?per_page=100': { workflow_runs: [] },
  '/git/trees/main?recursive=1': { tree: [{ path: 'cypress/e2e/api/sessao.feature' }] },
  '/contents/cypress/e2e/api/sessao.feature?ref=main': { content: b64(FEAT) },
};
(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } }); const p = await ctx.newPage();
  const erros = []; p.on('pageerror', (e) => erros.push(e.message));
  await ctx.route('https://api.github.com/**', (r) => { const u = new URL(r.request().url()); const m = u.pathname.match(/^\/repos\/[^/]+\/[^/]+(.*)$/); const k = (m ? m[1] : '') + u.search;
    const v = fork[k]; return v === undefined ? r.fulfill({ status: 404, body: '{}' }) : r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(v) }); });
  const fecha = async () => { for (let i = 0; i < 8; i++) { if (await p.isVisible('[data-test=fechar-conquista]').catch(() => false)) { await p.click('[data-test=fechar-conquista]'); await p.waitForTimeout(300); } else break; } };
  await p.goto(U + 'index.html?save=m6ep44'); await p.waitForURL(/dashboard/);
  ok(!(await p.isVisible('[data-test=menu-incidente]')), 'menu Incidente escondido antes de fechar o módulo 6');
  await p.goto(U + 'index.html?save=m7ep47'); await p.waitForURL(/dashboard/); await p.waitForTimeout(300);
  ok(await p.isVisible('[data-test=menu-incidente]'), 'menu Incidente aparece no módulo 7');
  await p.goto(U + 'incidente.html'); await p.waitForTimeout(300);
  const info = await p.evaluate(() => { const L = logIncidente(); return { n: L.lin.length, primeiro: L.primeiro, antes: L.lin.filter((x) => x.st === 401 && x.hora < '22:41' && !x.rota.includes('entrar')).length }; });
  ok(info.n > 3500 && info.n < 5000, `log com cerca de 4 mil linhas (${info.n})`);
  ok(info.primeiro === '22:41' && info.antes === 0, 'primeiro 401 fora do comum às 22:41');
  await p.selectOption('[data-test=in-filtro-status]', '401'); await p.fill('[data-test=in-filtro-hora]', '22:41');
  ok(/linhas/.test(await p.textContent('[data-test=in-contagem]')), 'filtro do log responde');
  await p.fill('[data-test=in-resp-hora]', '22:50'); await p.selectOption('[data-test=in-resp-deploy]', 'pdf'); await p.selectOption('[data-test=in-resp-duracao]', '30min'); await p.click('[data-test=in-responder]'); await p.waitForTimeout(400);
  ok(!(await p.evaluate(() => Object.keys((dados().m7 || {}).ok || {}).length)), 'respostas erradas não contam');
  await p.fill('[data-test=in-resp-hora]', '22:41'); await p.selectOption('[data-test=in-resp-deploy]', 'sessao'); await p.selectOption('[data-test=in-resp-duracao]', '30s'); await p.click('[data-test=in-responder]'); await p.waitForTimeout(1500); await fecha();
  await p.goto(U + 'incidente.html'); await p.waitForTimeout(300);
  ok(await p.isVisible('[data-test=in-ep47].feito'), 'conquista do EP47');
  await p.fill('[data-test=in-fork]', 'aluno/vida-de-qa-regressivo'); await p.click('[data-test=in-conferir]'); await p.waitForTimeout(1500); await fecha();
  await p.goto(U + 'incidente.html'); await p.waitForTimeout(300);
  ok(await p.isVisible('[data-test=in-ep48].feito') && await p.isVisible('[data-test=in-ep50].feito'), 'conquistas do EP48 e EP50 vindas do fork');
  await p.check('[data-test=in-acao-smoke]'); await p.check('[data-test=in-acao-horario]'); await p.check('[data-test=in-acao-alerta]'); await p.check('[data-test=in-acao-lucas]'); await p.click('[data-test=in-relatorio]'); await p.waitForTimeout(400);
  ok(!(await p.evaluate(() => (dados().m7.ok || {}).acoes)), 'aprovação do Lucas não fecha o relatório');
  await p.uncheck('[data-test=in-acao-lucas]'); await p.click('[data-test=in-relatorio]'); await p.waitForTimeout(1500); await fecha();
  await p.goto(U + 'incidente.html'); await p.waitForTimeout(300);
  ok(await p.isVisible('[data-test=in-ep51].feito'), 'conquista do EP51');
  const xp = await p.evaluate(() => xpDe()); ok(xp <= 5960, 'pleno só no Desafio 2 (' + xp + ')');
  ok(erros.length === 0, 'sem erro de JavaScript' + (erros.length ? ': ' + erros[0] : ''));
  await b.close(); console.log(falhas ? `\n${falhas} FALHA(S)` : '\nTUDO OK'); process.exit(falhas ? 1 : 0);
})();
