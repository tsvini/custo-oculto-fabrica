const { chromium } = require('playwright'); // Uso: node tests/flowdesk/ajustes.js [url-base] · ajustes de nov/2026 (dica do tipo, mensagens, voltar, cronômetro, execução, carreira)
const U = process.argv[2] || 'http://localhost:8765/';
let f = 0; const ok = (c, m) => { console.log((c ? 'OK   ' : 'FALHA ') + m); if (!c) f++; };
const muda = (p, fn) => p.evaluate(fn);
(async () => {
  const b = await chromium.launch(); const p = await (await b.newContext({ viewport: { width: 1280, height: 800 } })).newPage(); const err = []; p.on('pageerror', (e) => err.push(e.message));
  // ---- plano de testes: dica do campo Tipo, evidência em todo cenário, Passou/Falhou neutros
  await p.goto(U + 'index.html?save=ep04'); await p.waitForURL(/dashboard/);
  await p.goto(U + 'card.html?id=FD-101&aba=plano'); await p.waitForSelector('#linhas tr');
  if (await p.isHidden('#f')) await p.click('[data-test=novo-cenario]');
  ok(await p.isHidden('.dica-box'), 'dica do tipo fica escondida até pedir');
  await p.hover('[data-test=dica-tipo]'); ok(await p.isVisible('.dica-box'), 'passar o mouse no ? mostra a dica do tipo');
  const dica = await p.textContent('.dica-box'); ok(/Positivo/.test(dica) && /Negativo/.test(dica) && /Valor limite/.test(dica) && /101/.test(dica), 'dica explica os três tipos com exemplo');
  const nLin = await p.locator('#linhas tr').count(), nEv = await p.locator('#linhas [data-test=evidencia-cenario]').count();
  ok(nLin > 0 && nEv === nLin, `todo cenário tem anexar evidência (${nEv}/${nLin}), executado ou não`);
  const corNeutra = await p.locator('#linhas tr:first-child [data-test=marcar-passou]').evaluate((e) => getComputedStyle(e).backgroundColor);
  ok(!/rgb\(22, 163, 74\)|rgb\(220, 38, 38\)/.test(corNeutra), 'Passou sem marcar não fica colorido: ' + corNeutra);
  await p.locator('#linhas tr:first-child [data-test=marcar-passou]').click();
  const corOn = await p.locator('#linhas tr:first-child [data-test=marcar-passou]').evaluate((e) => getComputedStyle(e).backgroundColor);
  ok(/rgb\(22, 163, 74\)/.test(corOn), 'Passou marcado fica verde');
  await p.locator('#linhas tr:nth-child(2) [data-test=marcar-falhou]').click(); await p.click('#linhas tr:nth-child(2) [data-test=reportar-bug]');
  ok((await p.inputValue('[data-test=bug-passos]')).includes('Novo chamado') && (await p.inputValue('[data-test=bug-esperado]')).length > 5, 'reportar bug pelo plano já traz os passos e o esperado do cenário');
  await p.click('[data-test=fechar-modal]');
  // ---- mensagens ficam tempo pra ler e dá pra fechar
  await muda(p, () => toast('Teste de mensagem'));
  await p.waitForTimeout(5000); ok(await p.isVisible('[data-test=toast-sucesso]'), 'mensagem de sucesso continua na tela depois de 5 s');
  await p.click('[data-test=fechar-toast]'); ok(await p.isHidden('[data-test=toast-sucesso]'), 'mensagem fecha no ×');
  await muda(p, () => toast('Erro de teste', true)); await p.waitForTimeout(7500); ok(await p.isVisible('[data-test=toast-erro]'), 'mensagem de erro fica mais tempo (7,5 s)');
  // ---- criar chamado: a confirmação aparece na tela do chamado e tem como voltar pra lista
  await p.goto(U + 'novo-chamado.html'); ok(await p.isVisible('[data-test=voltar]'), 'novo chamado tem botão de voltar');
  await p.fill('#titulo', 'Teste do voltar'); await p.fill('#descricao', 'Conferindo o botão de voltar.');
  await p.click('[data-test=criar-chamado], button[type=submit]'); await p.waitForURL(/chamado\.html\?id=/);
  ok(await p.isVisible('[data-test=toast-sucesso]'), 'depois de criar, a mensagem aparece na tela do chamado');
  await p.waitForTimeout(4000); ok(await p.isVisible('[data-test=toast-sucesso]'), 'e ainda está lá 4 s depois');
  ok(await p.isVisible('[data-test=voltar]'), 'tela do chamado tem a seta de voltar'); await p.click('[data-test=voltar]'); await p.waitForURL(/chamados\.html/); ok(true, 'a seta volta pra lista de chamados');
  await p.goto(U + 'card.html?id=FD-101'); await p.click('[data-test=voltar]'); await p.waitForURL(/quadro\.html/); ok(true, 'no card, a seta volta pro quadro');
  // ---- desafio 1: cronômetro para em 00:00 e entrega sozinho
  await p.goto(U + 'index.html?save=d1'); await p.waitForURL(/dashboard/);
  await p.goto(U + 'card.html?id=FD-118'); await p.click('[data-test=comecar-desafio]'); await p.waitForSelector('[data-test=tempo-desafio]');
  ok((await p.textContent('[data-test=tempo-desafio]')).trim() === '40:00', 'desafio começa com 40:00');
  await muda(p, () => { const d = dados(); d.desafio.inicio = new Date(Date.now() - (40 * 60 - 2) * 1000).toISOString(); d.desafio.pausas = 0; salvar(); });
  await p.goto(U + 'chamados.html'); await p.waitForTimeout(4500);
  ok(/FD-118/.test(p.url()) && await p.isVisible('[data-test=desafio-resultado]'), 'em 00:00 o desafio é entregue e o aluno vê o resultado');
  ok(await p.isVisible('[data-test=desafio-tempo-esgotado]'), 'o resultado avisa que o tempo acabou');
  ok(!/-\d\d:\d\d/.test(await p.textContent('body')), 'nenhum tempo negativo na tela');
  ok(await p.isHidden('[data-test=relogio-desafio]'), 'o relógio do canto some depois da entrega');
  await p.click('#d1De'); await p.waitForSelector('[data-test=tempo-desafio]'); ok((await p.textContent('[data-test=tempo-desafio]')).trim() === '40:00', 'dá pra reiniciar o desafio do zero');
  // pausado não encerra
  await p.click('[data-test=pausar-desafio]'); await muda(p, () => { const d = dados(); d.desafio.inicio = new Date(Date.now() - 50 * 60000).toISOString(); d.desafio.pausadoDesde = new Date(Date.now() - 20 * 60000).toISOString(); salvar(); });
  await p.reload(); await p.waitForTimeout(2500); ok(await p.isHidden('[data-test=desafio-resultado]'), 'com o desafio pausado o tempo não acaba');
  // ---- carreira: comemora só quando acabou de subir
  await p.goto(U + 'index.html?save=ep16'); await p.waitForURL(/dashboard/); await p.waitForTimeout(600);
  ok(await p.isHidden('[data-test=festa-carreira]'), 'carregar um save de júnior não dispara a comemoração');
  await muda(p, () => { const d = dados(); d.festaPendente = 'junior'; salvar(); }); await p.reload(); await p.waitForTimeout(600);
  ok(await p.isVisible('[data-test=festa-carreira]') && /LinkedIn/.test(await p.textContent('[data-test=festa-carreira]')), 'ao subir pra júnior, a trilha comemora e lembra do cartão pro LinkedIn');
  await p.reload(); await p.waitForTimeout(500); ok(await p.isHidden('[data-test=festa-carreira]'), 'a comemoração aparece uma vez só');
  const gap = await p.locator('[data-test=carreira]').evaluate((e) => getComputedStyle(e).columnGap); ok(gap === '0px' || gap === 'normal', 'níveis da trilha colados na linha (gap ' + gap + ')');
  ok(err.length === 0, 'sem erro de JS ' + err.join('|'));
  await b.close(); console.log(f ? f + ' falha(s)' : 'tudo certo'); process.exitCode = f ? 1 : 0;
})();
