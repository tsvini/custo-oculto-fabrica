const { chromium } = require('playwright');
// Uso: node tests/flowdesk/desafio2.js [url-base]
// Desafio 2: card FD-130, fotos no novo chamado (regras e os 2 bugs de tela), nota e promoção pra pleno.
const U = process.argv[2] || 'http://localhost:8765/';
const F = require('fs').mkdtempSync(require('path').join(require('os').tmpdir(), 'fotos-'));
// arquivos com o tamanho de foto de celular (a tela confere extensão e tamanho)
for (const [n, mb] of [['forno_4mb.jpg', 4.4], ['caixa_4mb.jpg', 4.4], ['tela_4mb.jpg', 4.4], ['grande_6mb.png', 6.2], ['pequena.jpg', 0.1], ['doc.pdf', 0.01]]) require('fs').writeFileSync(require('path').join(F, n), require('crypto').randomBytes(Math.round(mb * 1048576)));
let falhas = 0; const ok = (c, m) => { console.log((c ? 'OK   ' : 'FALHA ') + m); if (!c) falhas++; };
const fecha = async (p) => { for (let i = 0; i < 6; i++) { if (await p.isVisible('[data-test=fechar-conquista]').catch(() => false)) { await p.click('[data-test=fechar-conquista]'); await p.waitForTimeout(250); } else break; } };
(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } }); const p = await ctx.newPage();
  const erros = []; p.on('pageerror', (e) => erros.push(e.message));
  await p.goto(U + 'index.html?save=m9ep64'); await p.waitForURL(/dashboard/); await p.waitForTimeout(300);
  await p.goto(U + 'novo-chamado.html'); ok(!(await p.isVisible('[data-test=adicionar-foto]')), 'sem fotos antes do Desafio 2');
  await p.goto(U + 'index.html?save=d2'); await p.waitForURL(/dashboard/); await p.waitForTimeout(400); await fecha(p);
  ok(/D2/.test(await p.textContent('[data-test=menu-missoes]')), 'missão atual: D2');
  await p.goto(U + 'card.html?id=FD-130'); ok(await p.isVisible('[data-test=desafio2]'), 'card FD-130 com o Desafio 2');
  await p.click('[data-test=comecar-desafio2]'); await p.waitForTimeout(400);
  ok((await p.locator('[data-test^=d2-plano-]').count()) === 8, 'o plano da IA com 8 linhas');
  await p.goto(U + 'novo-chamado.html?regressao='); ok((await p.textContent('[data-test=adicionar-foto]')).includes('Adicionar foto'), 'botão Adicionar foto no computador');
  await p.setInputFiles('[data-test=fotos]', F + '/doc.pdf'); ok(/Só fotos/.test(await p.textContent('[data-test=erro-fotos]')), 'PDF recusado');
  await p.setInputFiles('[data-test=fotos]', F + '/grande_6mb.png'); ok(/passa de 5 MB/.test(await p.textContent('[data-test=erro-fotos]')), 'foto de 6 MB recusada na tela');
  await p.setInputFiles('[data-test=fotos]', [F + '/forno_4mb.jpg', F + '/caixa_4mb.jpg', F + '/tela_4mb.jpg', F + '/pequena.jpg']); await p.waitForTimeout(800);
  ok((await p.locator('[data-test=foto]').count()) === 3 && /No máximo 3/.test(await p.textContent('[data-test=erro-fotos]')), 'quarta foto recusada');
  await p.fill('[data-test=titulo]', 'Forno não liga'); await p.fill('[data-test=descricao]', 'Foto do painel.'); await p.click('[data-test=criar-chamado]'); await p.waitForTimeout(1200);
  const id = await p.evaluate(() => { const d = JSON.parse(localStorage.getItem(Object.keys(localStorage).find((k) => k.startsWith('fd:dados:')))); return d.chamados[d.chamados.length - 1].id; });
  const t0 = Date.now(); await p.goto(U + 'chamado.html?id=' + id); await p.waitForSelector('[data-test=chamado-fotos]'); const ms = Date.now() - t0;
  ok(ms > 4500, 'tela do chamado com 3 fotos grandes demora: ' + ms + ' ms');
  const m = await ctx.newPage(); await m.setViewportSize({ width: 390, height: 844 }); await m.goto(U + 'novo-chamado.html?regressao=');
  ok(!(await m.isVisible('.foto-tx')) && (await m.evaluate(() => { const b = document.querySelector('[data-test=adicionar-foto]'); return (b.getAttribute('aria-label') || b.innerText.trim()); })) === '', 'no celular o botão de foto fica sem nome');
  await m.close();
  await p.goto(U + 'card.html?id=FD-130'); await p.selectOption('[data-test=d2-plano-2]', 'inventado'); await p.selectOption('[data-test=d2-plano-4]', 'lugar'); await p.fill('[data-test=d2-falta]', 'A quarta foto ser recusada');
  const onde = ['smoke', 'smoke', 'regressivo', 'regressivo', 'manual', 'regressivo']; for (let i = 0; i < 6; i++) await p.selectOption(`[data-test=d2-onde-${i + 1}]`, onde[i]);
  await p.evaluate(() => { const k = Object.keys(localStorage).find((x) => x.startsWith('fd:dados:')); const d = JSON.parse(localStorage.getItem(k));
    const bug = (id, titulo, obtido) => d.cards.push({ id, titulo, coluna: 'afazer', resp: 'gabriela', tipo: 'bug', prioridade: 'Alta', relacionado: 'FD-130', cenario: '', passos: '', esperado: '', obtido, evidencia: '', criterios: [], ok: [], comentarios: [] });
    bug('BUG-90', 'Servidor aceita foto de 6 MB pela API', 'POST /api/chamados/1/fotos com 6 MB responde 201'); bug('BUG-91', 'No celular o botão de câmera não tem nome', 'O leitor de tela fala só botão'); localStorage.setItem(k, JSON.stringify(d)); });
  await p.goto(U + 'card.html?id=FD-130'); await p.click('[data-test=entregar-desafio2]'); await p.click('[data-test=confirmar-entrega2]'); await p.waitForTimeout(800);
  ok(/Promovido/.test(await p.textContent('[data-test=desafio2-resultado]')), 'promovido com plano certo e 2 bugs: ' + (await p.textContent('[data-test=nota-desafio2]')));
  await fecha(p); await p.goto(U + 'dashboard.html'); await p.waitForTimeout(400); await fecha(p);
  ok(!/D2/.test(await p.textContent('[data-test=menu-missoes]')), 'depois da promoção a missão D2 sai');
  ok(/pleno/i.test(await p.textContent('[data-test=nivel]')), 'nível: ' + (await p.textContent('[data-test=nivel]')));
  ok(parseInt(await p.textContent('[data-test=xp]')) >= 6000, 'XP chega no pleno: ' + (await p.textContent('[data-test=xp]')));
  await p.goto(U + 'efetivacao.html?nivel=pleno'); ok(!(await p.isVisible('[data-test=cartao-bloqueado]')), 'cartão de promoção liberado');
  ok(erros.length === 0, 'sem erro de JavaScript' + (erros.length ? ': ' + erros[0] : ''));
  await b.close(); console.log(falhas ? `\n${falhas} FALHA(S)` : '\nTUDO OK'); process.exit(falhas ? 1 : 0);
})();
