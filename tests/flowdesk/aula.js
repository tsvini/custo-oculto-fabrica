const { chromium } = require('playwright'); // Uso: node tests/flowdesk/aula.js [url-base]  · links por aula (aula.html?ep=N)
const U = process.argv[2] || 'http://localhost:8765/';
let f = 0; const ok = (c, m) => { console.log((c ? 'OK   ' : 'FALHA ') + m); if (!c) f++; };
(async () => { const b = await chromium.launch(); const p = await (await b.newContext()).newPage(); const err = []; p.on('pageerror', (e) => err.push(e.message));
  await p.goto(U + 'aula.html?ep=00'); await p.waitForURL(/index\.html\?volta=/); ok(true, 'sem conta: vai pro login guardando a aula');
  await p.click('[data-test=ir-criar-conta]'); await p.fill('[data-test=cadastro-nome]', 'Ana'); await p.fill('[data-test=cadastro-email]', 'a@a.com'); await p.fill('[data-test=cadastro-senha]', '123456'); await p.click('[data-test=cadastro-criar]');
  await p.waitForURL(/card\.html\?id=FD-101/); ok(true, 'depois do cadastro cai direto na prática do EP00');
  await p.goto(U + 'aula.html?ep=8'); await p.waitForSelector('[data-test=aula-pular]'); ok(/Prática do EP08/.test(await p.textContent('body')), 'aula à frente: oferece pular');
  await p.click('[data-test=aula-confirmar]'); await p.waitForURL(/aba=plano/); ok(true, 'pulou e abriu a prática do EP08');
  const cq = await p.evaluate(() => dados().conquistas); ok(cq.includes('ep06') && !cq.includes('ep08'), 'estado do começo do EP08: ' + cq.join(','));
  await p.goto(U + 'aula.html?ep=4'); await p.waitForURL(/card\.html/); ok(true, 'aula que já passou: vai direto, sem perguntar');
  await p.goto(U + 'configuracoes.html'); ok(await p.isVisible('[data-test=desfazer-pulo]'), 'Configurações oferece voltar pro progresso');
  await p.click('[data-test=desfazer-pulo]'); await p.waitForURL(/dashboard/); const cq2 = await p.evaluate(() => dados().conquistas || []); ok(!cq2.includes('ep06'), 'voltou pro progresso de antes: ' + cq2.join(','));
  await p.goto(U + 'aula.html?ep=d1'); ok(await p.isVisible('[data-test=aula-pular]'), 'link do Desafio 1 funciona');
  ok(err.length === 0, 'sem erro de JS ' + err.join('|')); await b.close(); console.log(f ? f + ' falha(s)' : 'tudo certo'); })();
