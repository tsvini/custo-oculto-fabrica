const { chromium } = require('playwright');
// Uso: node tests/flowdesk/modulo4.js [url-base]   (padrão: http://localhost:8765/)
// Ganchos do módulo 4: ?save=, ?api=rede, ?regressao= (duplicado, rascunho, periodo, layout)
const U = process.argv[2] || 'http://localhost:8765/';
let falhas = 0; const ok = (c, m) => { console.log((c ? 'OK   ' : 'FALHA ') + m); if (!c) falhas++; };
(async () => {
  const b = await chromium.launch();
  const nova = async (vp) => { const ctx = await b.newContext({ viewport: vp || { width: 1280, height: 800 } }); const p = await ctx.newPage(); const erros = []; p.on('pageerror', (e) => erros.push(e.message)); p.erros = erros; return { ctx, p }; };
  // 1) save pela URL
  let { ctx, p } = await nova();
  await p.goto(U + 'index.html?save=m4'); await p.waitForURL(/dashboard/);
  ok(/Aluno Teste/.test(await p.textContent('[data-test=usuario-logado]')), 'save pela URL entra com a conta de teste');
  ok(!/save=/.test(p.url()), 'parâmetro save sai da URL');
  const v = await p.evaluate(() => VERSAO); ok(v === 18, 'Sprint 18 depois do EP20 (VERSAO=' + v + ')');
  // 2) duplicado corrigido: clique duplo com rede lenta manda um pedido só
  const criaDuplo = async (url) => {
    let n = 0; await p.route('**/servidor/chamados', async (r) => { n++; await new Promise((s) => setTimeout(s, 1200)); await r.fulfill({ status: 201, contentType: 'application/json', body: JSON.stringify({ id: 9000 + n }) }); });
    await p.goto(url); await p.fill('[data-test=titulo]', 'Clique duplo ' + Date.now()); await p.fill('[data-test=descricao]', 'Teste do módulo 4');
    await p.click('[data-test=criar-chamado]'); await p.click('[data-test=criar-chamado]', { force: true }).catch(() => {});
    await p.waitForTimeout(3000); await p.unroute('**/servidor/chamados'); return n;
  };
  ok(await criaDuplo(U + 'novo-chamado.html?api=rede') === 1, 'sem regressão: clique duplo = 1 pedido');
  ok(await p.isVisible('[data-test=modo-regressao]'), 'selo aparece no modo api=rede');
  ok(await criaDuplo(U + 'novo-chamado.html?api=rede&regressao=duplicado') === 2, 'regressao=duplicado: clique duplo = 2 pedidos');
  const nDup = await p.evaluate(() => dados().chamados.filter((c) => /^Clique duplo/.test(c.titulo)).length); ok(nDup === 3, 'chamados criados pelas respostas (' + nDup + ')');
  // 3) sem stub, o servidor de treino não existe: erro amigável
  await p.goto(U + 'novo-chamado.html?api=rede&regressao='); await p.fill('[data-test=titulo]', 'Sem stub'); await p.fill('[data-test=descricao]', 'x'); await p.click('[data-test=criar-chamado]'); await p.waitForTimeout(1500);
  ok(/servidor respondeu|Não deu/.test(await p.textContent('body')), 'sem stub mostra erro do servidor');
  // 4) caminho normal (service worker) continua funcionando
  await p.goto(U + 'novo-chamado.html?api='); await p.fill('[data-test=titulo]', 'Pelo service worker'); await p.fill('[data-test=descricao]', 'x'); await p.click('[data-test=criar-chamado]'); await p.waitForTimeout(2500);
  ok(/criado com sucesso/.test(await p.textContent('body')), 'service worker ainda cria chamado');
  // 5) período: 7 dias inclui hoje; com regressão, não
  const hoje = async (url) => { await p.goto(url); await p.selectOption('[data-test=filtro-periodo]', '7'); await p.waitForTimeout(300); return p.evaluate(() => [...document.querySelectorAll('[data-test=linha-chamado]')].filter((e) => /min|agora|há [0-9]+ h$/.test(e.querySelector('.quando').textContent.trim())).length); };
  const h1 = await hoje(U + 'chamados.html?regressao='); ok(h1 > 0, 'últimos 7 dias mostra os de hoje (' + h1 + ')');
  const h2 = await hoje(U + 'chamados.html?regressao=periodo'); ok(h2 === 0, 'regressao=periodo some com os de hoje (' + h2 + ')');
  // 6) rascunho: corrigido não vaza pra outra conta; com regressão vaza
  const vaza = async (regr) => {
    await p.goto(U + 'novo-chamado.html?regressao=' + regr); await p.fill('[data-test=titulo]', 'Contrato secreto'); await p.waitForTimeout(200);
    await p.click('[data-test=sair]'); await p.waitForURL(/index/);
    await p.click('[data-test=ir-criar-conta]'); await p.fill('[data-test=cadastro-nome]', 'Outra Pessoa'); await p.fill('[data-test=cadastro-email]', 'outra' + Date.now() + '@t.com'); await p.fill('[data-test=cadastro-senha]', '123456'); await p.click('[data-test=cadastro-criar]'); await p.waitForURL(/dashboard/);
    await p.goto(U + 'index.html?save=m4'); // volta pra Sprint 18 na conta nova
    await p.waitForURL(/dashboard/); await p.goto(U + 'novo-chamado.html'); await p.waitForTimeout(300);
    const t = await p.inputValue('[data-test=titulo]');
    // volta pra conta de teste
    await p.click('[data-test=sair]'); await p.waitForURL(/index/); await p.fill('[data-test=email]', 'aluno@teste.com').catch(() => {}); return t;
  };
  ok(await vaza('') === '', 'sem regressão: rascunho não vaza');
  await p.evaluate(() => { localStorage.setItem('fd:sessao', JSON.stringify('aluno@teste.com')); });
  ok(await vaza('rascunho') === 'Contrato secreto', 'regressao=rascunho: rascunho vaza');
  ok(p.erros.length === 0, 'sem erro de JS: ' + p.erros.join(' | '));
  await ctx.close();
  // 7) layout no celular
  ({ ctx, p } = await nova({ width: 390, height: 844 }));
  await p.goto(U + 'index.html?save=m4'); await p.waitForURL(/dashboard/);
  await p.goto(U + 'chamados.html?regressao='); ok(await p.isVisible('[data-test=novo-chamado]'), 'celular: botão Novo chamado aparece');
  await p.goto(U + 'chamados.html?regressao=layout'); ok(!(await p.isVisible('[data-test=novo-chamado]')), 'regressao=layout: botão some no celular');
  await p.setViewportSize({ width: 1280, height: 800 }); await p.goto(U + 'chamados.html'); ok(await p.isVisible('[data-test=novo-chamado]'), 'regressao=layout: no desktop continua');
  await b.close(); console.log(falhas ? falhas + ' falha(s)' : 'tudo certo'); process.exit(falhas ? 1 : 0);
})();
