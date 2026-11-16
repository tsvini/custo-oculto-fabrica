// Uso: node tests/flowdesk/diploma.js [url-base]  · pular aula não dá cartão de efetivação
const { chromium } = require('playwright'); const U = process.argv[2] || 'http://localhost:8765/';
let f = 0; const ok = (c, m) => { console.log((c ? 'OK   ' : 'FALHA ') + m); if (!c) f++; };
(async () => { const b = await chromium.launch(); const p = await (await b.newContext()).newPage(); const err = []; p.on('pageerror', (e) => err.push(e.message));
  await p.goto(U + 'aula.html?ep=20'); await p.click('[data-test=ir-criar-conta]'); await p.fill('[data-test=cadastro-nome]', 'Pula Tudo'); await p.fill('[data-test=cadastro-email]', 'pula@t.com'); await p.fill('[data-test=cadastro-senha]', '123456'); await p.click('[data-test=cadastro-criar]');
  await p.waitForSelector('[data-test=aula-confirmar]'); await p.click('[data-test=aula-confirmar]'); await p.waitForURL(/novo-chamado/);
  await p.goto(U + 'efetivacao.html'); ok(await p.isVisible('[data-test=cartao-bloqueado]'), 'pulou pro EP20: cartão continua bloqueado');
  ok(!(await p.isVisible('[data-test=cartao]')), 'nenhum cartão pra baixar');
  ok(/Falta fazer o Desafio 1/.test(await p.textContent('body')), 'explica que falta o desafio');
  ok(await p.isVisible('[data-test=menu-efetivacao] .tranca'), 'Carreira continua com cadeado no menu');
  await p.goto(U + 'configuracoes.html?save=m4'); await p.waitForURL(/configuracoes/); await p.goto(U + 'efetivacao.html'); ok(await p.isVisible('[data-test=cartao-bloqueado]'), 'save pela URL também não dá cartão');
  await p.click('[data-test=fazer-desafio]'); await p.waitForURL(/FD-118/); ok(await p.isVisible('[data-test=comecar-desafio]'), '"Fazer o Desafio 1 agora" abre o desafio');
  ok(err.length === 0, 'sem erro de JS ' + err.join('|')); await b.close(); console.log(f ? f + ' falha(s)' : 'tudo certo'); process.exit(f ? 1 : 0); })();
