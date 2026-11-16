const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
// Uso: node tests/flowdesk/regressivo.js [url-base]
// Missões do módulo 4: o aluno cola a saída real do `npx cypress run` e o FlowDesk confere (saidas-cypress/ são execuções de verdade)
const U = process.argv[2] || 'http://localhost:8765/';
const S = (n) => fs.readFileSync(path.join(__dirname, 'saidas-cypress', n + '.txt'), 'utf8');
let falhas = 0; const ok = (c, m) => { console.log((c ? 'OK   ' : 'FALHA ') + m); if (!c) falhas++; };
(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } }); const p = await ctx.newPage();
  const erros = []; p.on('pageerror', (e) => erros.push(e.message));
  const fecha = async () => { if (await p.isVisible('[data-test=fechar-conquista]').catch(() => false)) await p.click('[data-test=fechar-conquista]'); };
  // antes do EP20 a página fica fechada e o menu não mostra
  await p.goto(U + 'index.html?save=ep18'); await p.waitForURL(/dashboard/);
  ok(!(await p.isVisible('[data-test=menu-regressivo]')), 'menu Regressivo escondido antes do módulo 4');
  await p.goto(U + 'regressivo.html'); ok(await p.isVisible('[data-test=rg-fechado]'), 'regressivo fechado antes do EP20');
  // módulo 4
  await p.goto(U + 'index.html?save=m4'); await p.waitForURL(/dashboard/); await p.waitForTimeout(400);
  ok(await p.isVisible('[data-test=menu-regressivo]'), 'menu Regressivo aparece no módulo 4');
  ok(/EP22/.test(await p.textContent('[data-test=missao-atual]')), 'missão do EP22 no lado');
  const cola = async (id, k, txt) => { await p.goto(U + 'regressivo.html#' + id); await p.fill(`[data-test=rg-${id}-${k}]`, txt); await p.click(`[data-test=rg-conferir-${id}-${k}]`); await p.waitForTimeout(700); await fecha(); };
  const tem = (id, k) => p.evaluate(([i, kk]) => !!((dados().m4 || {})[i] || {})[kk], [id, k]);
  // recusas
  await cola('ep23', 'verde', 'qualquer texto'); ok(!(await tem('ep23', 'verde')), 'texto sem resumo do Cypress é recusado');
  await cola('ep23', 'bug', S('ep23_verde')); ok(!(await tem('ep23', 'bug')), 'execução verde não vale como prova do bug');
  await cola('ep24', 'bug', S('ep23_bug')); ok(!(await tem('ep24', 'bug')), 'vermelho de outro spec não vale');
  await cola('ep27', 'tres', S('ep27_verde') + S('ep27_mente') + S('ep27_verde')); ok(!(await tem('ep27', 'tres')), 'três execuções com uma vermelha é recusado');
  // aceites, com as saídas reais
  const passos = [['ep22', 'verde'], ['ep23', 'verde'], ['ep23', 'bug'], ['ep24', 'verde'], ['ep24', 'bug'], ['ep25', 'verde'], ['ep25', 'bug'], ['ep26', 'verde'], ['ep26', 'bug'], ['ep27', 'verde'], ['ep27', 'tres'], ['ep28', 'verde']];
  for (const [id, k] of passos) { await cola(id, k, S(id + '_' + k)); ok(await tem(id, k), `${id} ${k} aceito`); }
  // revisão do PR: errado e certo
  await p.goto(U + 'regressivo.html#ep28');
  for (const k of ['pos', 'tres', 'wait', 'dep', 'shot']) await p.check(`[data-test=rev-${k}]`);
  await p.click('[data-test=rg-revisar]'); await p.waitForTimeout(400); ok(!(await tem('ep28', 'revisao')), 'revisão com item a mais é recusada');
  await p.uncheck('[data-test=rev-shot]'); await p.click('[data-test=rg-revisar]'); await p.waitForTimeout(900); await fecha();
  ok(await tem('ep28', 'revisao'), 'revisão com os 4 problemas aceita');
  await p.goto(U + 'dashboard.html'); await p.waitForTimeout(900); await fecha(); await p.waitForTimeout(300);
  const cq = await p.evaluate(() => dados().conquistas);
  ok(['ep22', 'ep23', 'ep24', 'ep25', 'ep26', 'ep27', 'ep28'].every((k) => cq.includes(k)), 'as 7 conquistas do módulo 4');
  const xp = await p.evaluate(() => xpDe()); ok(xp > 3660 && xp < 6000, 'XP sobe rumo a pleno sem chegar lá (' + xp + ')');
  ok(/EP29|EP31/.test(await p.textContent('[data-test=missao-atual]')), 'depois do módulo 4, o lado aponta pra frente (EP29 ou a missão do EP31)');
  // link da aula pula pro meio do módulo 4 com as missões de antes feitas
  await p.goto(U + 'index.html?save=m4'); await p.waitForURL(/dashboard/);
  await p.goto(U + 'aula.html?ep=25'); await p.click('[data-test=aula-confirmar]'); await p.waitForURL(/regressivo/); await p.waitForTimeout(500);
  const c2 = await p.evaluate(() => dados().conquistas); ok(c2.includes('ep24') && !c2.includes('ep25'), 'aula.html?ep=25 monta o começo do EP25');
  ok(!(await p.evaluate(() => !!DIPLOMAS().pleno)), 'pular aula não dá diploma');
  ok(!erros.length, 'sem erro de JavaScript' + (erros.length ? ': ' + erros[0] : ''));
  await b.close(); console.log(falhas ? `\n${falhas} falha(s)` : '\nTudo certo'); process.exit(falhas ? 1 : 0);
})();
