const { chromium } = require('playwright');
// Uso: node tests/flowdesk/pipeline.js [url-base]
// Missões do módulo 5: o FlowDesk consulta a API pública do GitHub. Aqui a API é simulada com um fork completo e um incompleto.
const U = process.argv[2] || 'http://localhost:8765/';
let falhas = 0; const ok = (c, m) => { console.log((c ? 'OK   ' : 'FALHA ') + m); if (!c) falhas++; };
const b64 = (s) => Buffer.from(s).toString('base64');
const WF = "name: Smoke\non:\n  pull_request:\nenv:\n  TZ: America/Sao_Paulo\njobs:\n  smoke:\n    runs-on: ubuntu-latest\n";
const fork = (completo) => ({
  '': { fork: true, default_branch: 'main', parent: { full_name: 'tsvini/vida-de-qa-regressivo' } },
  '/actions/runs?per_page=100': { workflow_runs: completo ? [
    { id: 1, name: 'Regressivo', path: '.github/workflows/regressivo.yml', event: 'pull_request', conclusion: 'success', head_branch: 'gatilho' },
    { id: 2, name: 'Smoke', path: '.github/workflows/smoke.yml', event: 'pull_request', conclusion: 'success', head_branch: 'fuso' },
    { id: 3, name: 'Regressivo', path: '.github/workflows/regressivo.yml', event: 'workflow_dispatch', conclusion: 'success', head_branch: 'main' },
    { id: 4, name: 'Smoke', path: '.github/workflows/smoke.yml', event: 'pull_request', conclusion: 'failure', head_branch: 'quebra' },
  ] : [{ id: 1, name: 'Regressivo', path: '.github/workflows/regressivo.yml', event: 'push', conclusion: 'success', head_branch: 'main' }] },
  '/actions/runs/4/artifacts': { total_count: 1 },
  '/contents/cypress/e2e/painel.feature?ref=fuso': completo ? { name: 'painel.feature' } : null,
  '/contents/.github/workflows?ref=fuso': [{ name: 'smoke.yml', path: '.github/workflows/smoke.yml' }],
  '/contents/.github/workflows/smoke.yml?ref=fuso': { content: b64(WF) },
  '/branches/main': { protected: completo },
  '/issues?labels=regressivo&state=all&per_page=30': completo ? [{ user: { login: 'github-actions[bot]' }, comments: 2 }] : [],
});
(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } }); const p = await ctx.newPage();
  const erros = []; p.on('pageerror', (e) => erros.push(e.message));
  let base = fork(true), consultas = 0;
  await ctx.route('https://api.github.com/**', (r) => { consultas++; const u = new URL(r.request().url()); const m = u.pathname.match(/^\/repos\/[^/]+\/[^/]+(.*)$/); const k = (m ? m[1] : '') + u.search;
    const v = base[k]; return v === undefined || v === null ? r.fulfill({ status: 404, body: '{}' }) : r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(v) }); });
  const fecha = async () => { for (let i = 0; i < 8; i++) { if (await p.isVisible('[data-test=fechar-conquista]').catch(() => false)) { await p.click('[data-test=fechar-conquista]'); await p.waitForTimeout(350); } else break; } };
  await p.goto(U + 'index.html?save=m4'); await p.waitForURL(/dashboard/);
  ok(!(await p.isVisible('[data-test=menu-pipeline]')), 'menu Pipeline escondido antes de fechar o módulo 4');
  await p.goto(U + 'pipeline.html'); ok(await p.isVisible('[data-test=pp-fechado]'), 'pipeline fechado antes do módulo 5');
  await p.goto(U + 'index.html?save=m5ep31'); await p.waitForURL(/dashboard/); await p.waitForTimeout(400);
  ok(await p.isVisible('[data-test=menu-pipeline]'), 'menu Pipeline aparece no módulo 5');
  ok(/EP31/.test(await p.textContent('[data-test=missao-atual]')), 'missão do EP31 no lado');
  await p.goto(U + 'pipeline.html');
  await p.fill('[data-test=pp-fork]', 'qualquer coisa'); await p.click('[data-test=pp-conferir]'); await p.waitForTimeout(300);
  ok(consultas === 0, 'nome inválido nem consulta o GitHub');
  base = { '': { fork: false, default_branch: 'main' } };
  await p.fill('[data-test=pp-fork]', 'aluno/outro-repo'); await p.click('[data-test=pp-conferir]'); await p.waitForTimeout(800);
  ok(!(await p.evaluate(() => (dados().m5 || {}).fork)), 'repositório que não é fork é recusado');
  base = fork(false);
  await p.fill('[data-test=pp-fork]', 'https://github.com/aluno/vida-de-qa-regressivo'); await p.click('[data-test=pp-conferir]'); await p.waitForURL(/pipeline/); await p.waitForTimeout(900); await fecha();
  ok(await p.evaluate(() => dados().m5.fork === 'aluno/vida-de-qa-regressivo'), 'aceita o link do GitHub e guarda o fork');
  ok(await p.evaluate(() => !Object.keys(dados().m5.ok || {}).length), 'fork sem nada feito: nenhuma etapa conferida');
  base = fork(true);
  await p.click('[data-test=pp-conferir]'); await p.waitForTimeout(1500); await fecha(); await p.goto(U + 'dashboard.html'); await p.waitForTimeout(900); await fecha();
  const m5 = await p.evaluate(() => dados().m5.ok);
  for (const k of ['prVerde', 'smoke', 'completo', 'evidencia', 'painel', 'fuso', 'protegida', 'card', 'comentario']) ok(!!m5[k], 'etapa ' + k);
  const cq = await p.evaluate(() => dados().conquistas); ok(['ep31', 'ep32', 'ep33', 'ep34', 'ep35', 'ep36'].every((k) => cq.includes(k)), 'as 6 conquistas do módulo 5');
  const xp = await p.evaluate(() => xpDe()); ok(xp < 6000, 'XP ainda abaixo de pleno (' + xp + ')');
  ok(/EP37/.test(await p.textContent('[data-test=missao-atual]')), 'próximo passo vira o EP37');
  await p.goto(U + 'aula.html?ep=33'); ok(/pipeline|aula/.test(p.url()), 'link da aula do módulo 5 responde');
  ok(!erros.length, 'sem erro de JavaScript' + (erros.length ? ': ' + erros[0] : ''));
  await b.close(); console.log(falhas ? `\n${falhas} falha(s)` : '\nTudo certo'); process.exit(falhas ? 1 : 0);
})();
