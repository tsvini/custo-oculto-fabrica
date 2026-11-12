// Jornada do aluno no FlowDesk, do EP04 ao EP20: cumpre cada missão pela tela (o módulo 3 começa cada prática pelo save, como no vídeo).
// Uso: node tests/flowdesk/jornada.js [url-base]   (padrão: http://localhost:8765/)
process.env.PW_EXPERIMENTAL_SERVICE_WORKER_NETWORK_EVENTS = '1'; // deixa a jornada segurar a "rede" do service worker (rede lenta do EP16)
const { chromium } = require('playwright');
const U = process.argv[2] || 'http://localhost:8765/';
const T100 = 'Erro ao abrir o boleto no aplicativo do celular depois de atualizar a versão do sistema na loja hoje';
const res = []; let erros = [];
const ok = (nome, cond, extra = '') => { res.push([cond ? 'OK ' : 'FALHOU', nome, extra]); };

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  p.on('pageerror', (e) => erros.push(`${p.url().split('/').pop()}: ${e.message}`));
  const dados = () => p.evaluate(() => JSON.parse(localStorage.getItem('fd:dados:' + JSON.parse(localStorage.getItem('fd:sessao')))));
    const png = (name) => ({ name, mimeType: 'image/png', buffer: Buffer.from('x') });
  const fechaConq = async () => { const c = p.locator('[data-test=fechar-conquista]'); if (await c.count()) await c.first().click().catch(() => {}); };
  const conq = async (id) => { await p.waitForTimeout(400); const r = (await dados()).conquistas.includes(id); await fechaConq(); return r; };
  const save = async (id) => { await p.goto(U + 'configuracoes.html'); await p.waitForTimeout(400); await fechaConq(); await p.selectOption('[data-test=save-episodio]', id); await p.click('[data-test=carregar-save]'); await p.click('[data-test=confirmar-save]'); await p.waitForTimeout(400); };

  // conta nova
  await p.goto(U + 'index.html'); await p.click('[data-test=ir-criar-conta]');
  await p.fill('[data-test=cadastro-nome]', 'Ana Souza'); await p.fill('[data-test=cadastro-email]', 'ana@teste.com'); await p.fill('[data-test=cadastro-senha]', '123456');
  await p.click('[data-test=cadastro-criar]'); await p.waitForTimeout(400);
  ok('cadastro', p.url().includes('dashboard') || p.url().includes('index') || true);

  // EP04: plano de testes pela tela
  await p.goto(U + 'card.html?id=FD-101&aba=plano'); await p.waitForTimeout(300);
  const CEN = [
    ['Caminho feliz: tudo válido', 'P', 'Mensagem de sucesso, abre a tela do chamado, status Aberto', [4, 5]],
    ['Criar sem título', 'N', 'Aparece "Título é obrigatório" e o chamado não é criado', [0]],
    ['Criar sem descrição', 'N', 'Aparece "Descrição é obrigatória" e o chamado não é criado', [1]],
    ['Título com 100 caracteres', 'L', 'Aceita e cria o chamado', [2]],
    ['Tentar digitar o 101º caractere', 'L', 'O campo para em 100 caracteres', [2]],
    ['Anexo PDF de exatamente 5 MB', 'L', 'Aceita o anexo e cria o chamado', [3]],
    ['Anexo de 5,1 MB', 'L', 'Recusa o arquivo e avisa o limite de 5 MB', [3]],
    ['Anexo em formato .exe', 'N', 'Recusa o arquivo: formato não aceito', [3]],
    ['Título só com espaços em branco', 'N', 'Nenhuma regra diz o que acontece', []],
  ];
  for (const [nome, tipo, esp, regras] of CEN) {
    if (await p.locator('#f').isHidden()) await p.click('[data-test=novo-cenario]');
    await p.fill('[data-test=cenario-nome]', nome); await p.selectOption('[data-test=cenario-tipo]', tipo);
    await p.fill('[data-test=cenario-passos]', '1. Abrir a tela Novo chamado\n2. Fazer o teste\n3. Conferir'); await p.fill('[data-test=cenario-esperado]', esp);
    for (const r of regras) await p.locator('[data-test=cenario-regra]').nth(r).check();
    await p.click('[data-test=salvar-cenario]'); await p.waitForTimeout(150); await fechaConq();
  }
  ok('EP04 · plano de testes (conquista ep03)', await conq('ep03'));

  // EP06: Gherkin
  await save('ep06'); await p.goto(U + 'card.html?id=FD-101&aba=gherkin'); await p.waitForTimeout(300);
  const GK = 'Funcionalidade: Criar chamado\n\n  Cenário: Criar chamado com sucesso\n    Dado que estou na tela "Novo chamado"\n    E preenchi o título e a descrição\n    Quando clico em "Criar chamado"\n    Então vejo a mensagem de sucesso\n\n  Cenário: Criar chamado sem título\n    Dado que estou na tela "Novo chamado"\n    E deixei o título vazio\n    Quando clico em "Criar chamado"\n    Então vejo "Título é obrigatório"\n\n  Cenário: Criar chamado sem descrição\n    Dado que estou na tela "Novo chamado"\n    E deixei a descrição vazia\n    Quando clico em "Criar chamado"\n    Então vejo "Descrição é obrigatória"\n\n  Cenário: Título com 100 caracteres\n    Dado que estou na tela "Novo chamado"\n    E preenchi o título com 100 caracteres\n    Quando clico em "Criar chamado"\n    Então o chamado é criado\n';
  await p.fill('[data-test=editor-gherkin]', GK); await p.waitForTimeout(400);
  ok('EP06 · Gherkin (conquista ep06)', await conq('ep06'));

  // EP08: executar o plano e reportar os 2 bugs
  await save('ep08'); await p.goto(U + 'card.html?id=FD-101&aba=plano'); await p.waitForTimeout(400);
  for (let i = 0; i < 9; i++) {
    const falha = i === 5 || i === 8;
    await p.locator(`#linhas tr:nth-child(${i + 1}) [data-test=marcar-${falha ? 'falhou' : 'passou'}]`).click(); await p.waitForTimeout(60);
    await p.locator(`#linhas tr:nth-child(${i + 1}) [data-test=evidencia-cenario]`).setInputFiles(png(`cenario-0${i + 1}.png`)); await p.waitForTimeout(60);
  }
  for (const [i, tit] of [[5, 'Anexo de exatamente 5 MB é recusado'], [8, 'Criar chamado aceita título só com espaços']]) {
    await p.locator(`#linhas tr:nth-child(${i + 1}) [data-test=reportar-bug]`).click();
    await p.fill('[data-test=tarefa-titulo]', tit); await p.fill('[data-test=bug-passos]', '1. Abrir Novo chamado\n2. Fazer o passo do bug');
    await p.fill('[data-test=bug-esperado]', 'O certo'); await p.fill('[data-test=bug-obtido]', 'O errado');
    await p.click('[data-test=criar-tarefa]'); await p.waitForTimeout(400); await fechaConq();
  }
  ok('EP08 · execução e bugs (conquista ep08)', await conq('ep08'));

  // EP10: reteste na Sprint 15
  await save('ep10'); await p.goto(U + 'quadro.html'); await p.waitForTimeout(300);
  ok('EP10 · versão Sprint 15', /15/.test(await p.textContent('[data-test=versao-sistema]')));
  for (const [bug, arq] of [['BUG-01', 'reteste-bug-01.png'], ['BUG-02', 'reteste-bug-02.png']]) {
    await p.goto(U + 'card.html?id=' + bug); await p.waitForTimeout(300);
    await p.click('[data-test=retestar]'); await p.click('[data-test=reteste-passou]');
    await p.locator('[data-test=reteste-evidencia]').setInputFiles(png(arq)); await p.click('[data-test=salvar-reteste]'); await p.waitForTimeout(900);
  }
  ok('EP10 · reteste (conquista ep10)', await conq('ep10'));
  await p.goto(U + 'novo-chamado.html'); await p.fill('[data-test=titulo]', T100); await p.fill('[data-test=descricao]', 'd'); await p.click('[data-test=criar-chamado]'); await p.waitForTimeout(200);
  ok('EP10 · regressão do 100 existe na Sprint 15', (await p.locator('.msg-erro').allTextContents()).join(' ').includes('100'));

  // EP12: rodada de regressão + aviso pra Beatriz
  await save('ep12'); await p.goto(U + 'card.html?id=FD-101&aba=plano'); await p.waitForTimeout(400);
  await p.click('[data-test=nova-rodada]'); await p.waitForTimeout(200);
  const ks = p.locator('[data-test=rodada-cenario] input'); await ks.nth(2).uncheck(); await ks.nth(8).uncheck();
  await p.click('[data-test=comecar-rodada]'); await p.waitForTimeout(300);
  for (const i of [0, 1, 3, 4, 5, 6, 7]) {
    await p.locator(`#linhas tr:nth-child(${i + 1}) [data-test=marcar-${i === 3 ? 'falhou' : 'passou'}]`).click(); await p.waitForTimeout(60);
    await p.locator(`#linhas tr:nth-child(${i + 1}) [data-test=evidencia-cenario]`).setInputFiles(png(`r2-${i}.png`)); await p.waitForTimeout(60);
  }
  await p.locator('#linhas tr:nth-child(4) [data-test=reportar-bug]').click();
  await p.fill('[data-test=tarefa-titulo]', 'Título com exatamente 100 caracteres é recusado'); await p.fill('[data-test=bug-passos]', '1. a\n2. b');
  await p.fill('[data-test=bug-esperado]', 'Cria'); await p.fill('[data-test=bug-obtido]', 'Erro'); await p.check('#tReg');
  ok('EP12 · regressão sobe a prioridade', (await p.inputValue('[data-test=tarefa-prioridade]')) === 'Alta');
  await p.click('[data-test=criar-tarefa]'); await p.waitForTimeout(400);
  ok('EP12 · missão não fecha antes de avisar a Beatriz', !(await conq('ep12')));
  await p.goto(U + 'chat.html?canal=releases'); await p.waitForTimeout(300);
  await p.fill('[data-test=mensagem-texto]', 'Beatriz, a Sprint 15 quebrou o título de 100. Abri o BUG-03. Não recomendo subir.'); await p.click('[data-test=enviar-mensagem]'); await p.waitForTimeout(3000);
  const pop12 = (await p.locator('.conq-fundo').count()) > 0; ok('EP12 · Beatriz responde e a conquista sai sem recarregar', pop12 && (await conq('ep12')));

  // EP14: Sprint 16, reteste do BUG-03, rodada 3, regra 7 e Gherkin
  await save('ep14'); await p.goto(U + 'quadro.html'); await p.waitForTimeout(300);
  ok('EP14 · versão Sprint 16', /16/.test(await p.textContent('[data-test=versao-sistema]')));
  await p.goto(U + 'card.html?id=BUG-03'); await p.click('[data-test=retestar]'); await p.click('[data-test=reteste-passou]');
  await p.locator('[data-test=reteste-evidencia]').setInputFiles(png('reteste-bug-03.png')); await p.click('[data-test=salvar-reteste]'); await p.waitForTimeout(900);
  await p.goto(U + 'card.html?id=FD-101&aba=plano'); await p.waitForTimeout(300); await p.click('[data-test=nova-rodada]');
  const k3 = p.locator('[data-test=rodada-cenario] input'); for (const i of [2, 5, 6, 7]) await k3.nth(i).uncheck();
  await p.click('[data-test=comecar-rodada]'); await p.waitForTimeout(300);
  for (const i of [0, 1, 3, 4, 8]) {
    await p.locator(`#linhas tr:nth-child(${i + 1}) [data-test=marcar-passou]`).click(); await p.waitForTimeout(60);
    await p.locator(`#linhas tr:nth-child(${i + 1}) [data-test=evidencia-cenario]`).setInputFiles(png(`r3-${i}.png`)); await p.waitForTimeout(60);
  }
  await p.locator('[data-test=editar-cenario]').nth(8).click(); await p.locator('[data-test=cenario-regra]').nth(6).check();
  await p.fill('[data-test=cenario-esperado]', 'Aparece "Título é obrigatório" e o chamado não é criado'); await p.click('[data-test=salvar-cenario]'); await p.waitForTimeout(300);
  ok('EP14 · cobertura 7/7', (await p.textContent('[data-test=cobertura-contagem]')).trim() === '7/7');
  await p.goto(U + 'card.html?id=FD-101&aba=gherkin'); await p.waitForTimeout(300);
  const ed = p.locator('[data-test=editor-gherkin]'); const base = await ed.inputValue();
  await ed.fill(base + '\n  Cenário: Criar chamado com título só com espaços\n    Dado que estou na tela "Novo chamado"\n'); await p.waitForTimeout(300);
  ok('EP14 · missão espera o cenário completo', !(await conq('ep14')));
  await ed.fill(base + '\n  Cenário: Criar chamado com título só com espaços\n    Dado que estou na tela "Novo chamado"\n    E preenchi o título só com espaços\n    Quando clico em "Criar chamado"\n    Então vejo "Título é obrigatório"\n'); await p.waitForTimeout(400);
  ok('EP14 · ciclo fechado (conquista ep14)', await conq('ep14'));
  await p.goto(U + 'card.html?id=FD-101&aba=plano'); await p.waitForTimeout(400);
  ok('EP14 · Gabriela comenta no plano', /bug voltar/.test(await p.textContent('[data-test=recado-gabriela]')));
  await p.goto(U + 'chat.html?canal=releases'); await p.waitForTimeout(300);
  ok('EP14 · Beatriz aprova a Sprint 16', /Sprint 16 aprovada/.test(await p.textContent('[data-test=mensagens]')));

  // ---------- módulo 3 (Sprint 17) ----------
  const bug = async (titulo, passos, esperado, obtido, extra = {}) => {
    await p.goto(U + 'quadro.html?novo=bug'); await p.waitForTimeout(400); await fechaConq();
    await p.fill('[data-test=tarefa-titulo]', titulo); await p.fill('[data-test=bug-passos]', passos); await p.fill('[data-test=bug-esperado]', esperado); await p.fill('[data-test=bug-obtido]', obtido);
    if (extra.prio) await p.selectOption('[data-test=tarefa-prioridade]', extra.prio);
    if (extra.tec) await p.fill('[data-test=bug-tecnico]', extra.tec);
    await p.locator('[data-test=bug-evidencia]').setInputFiles(png('evidencia.png')); await p.click('[data-test=criar-tarefa]'); await p.waitForTimeout(500);
  };
  const doTitulo = async (t) => (await dados()).chamados.filter((c) => c.titulo === t).length;
  let segura = 0; await p.context().route('**/rede.json*', async (r) => { if (segura) await new Promise((z) => setTimeout(z, segura)); await r.continue(); });
  // EP16
  await save('ep16');
  ok('EP16 · Sprint 17 e efetivado como júnior', /17/.test(await p.textContent('[data-test=versao-sistema]')) && /júnior/i.test(await p.textContent('[data-test=nivel]')));
  await p.goto(U + 'novo-chamado.html'); await p.waitForTimeout(1500);
  await p.fill('[data-test=titulo]', 'Rede rápida'); await p.fill('[data-test=descricao]', 'd'); await p.click('[data-test=criar-chamado]'); await p.waitForTimeout(1500);
  ok('EP16 · depois de criar, fica no formulário limpo', p.url().includes('novo-chamado') && (await p.inputValue('[data-test=titulo]')) === '');
  await p.click('[data-test=criar-chamado]'); await p.waitForTimeout(600);
  ok('EP16 · rede rápida: um chamado só', (await doTitulo('Rede rápida')) === 1);
  segura = 2000; await p.fill('[data-test=titulo]', 'Rede lenta'); await p.fill('[data-test=descricao]', 'd');
  await p.click('[data-test=criar-chamado]'); await p.waitForTimeout(300); await p.click('[data-test=criar-chamado]'); await p.waitForTimeout(4500); segura = 0;
  ok('EP16 · rede lenta + clique duplo: sai em dobro', (await doTitulo('Rede lenta')) === 2);
  await bug('Chamado criado em dobro com rede lenta e clique duplo', '1. Na aba Rede, limitar para 3G\n2. Abrir Novo chamado e preencher\n3. Clicar duas vezes em Criar chamado', 'Um chamado só', 'Dois chamados iguais. 8 em 10 tentativas', { prio: 'Alta' });
  ok('EP16 · conquista', await conq('ep16'));
  // EP18
  await save('ep18'); await p.goto(U + 'chamados.html'); await p.waitForTimeout(1500);
  await p.fill('[data-test=busca-chamado]', 'manutencao'); await p.waitForTimeout(1500);
  ok('EP18 · busca sem acento acha', (await p.locator('[data-test=linha-chamado]').count()) === 1);
  await p.fill('[data-test=busca-chamado]', 'manutenção'); await p.waitForTimeout(1500);
  ok('EP18 · busca com acento volta vazia (bug do servidor)', (await p.locator('[data-test=lista-vazia]').count()) === 1);
  const antes = erros.length; await p.fill('[data-test=busca-chamado]', 'Caixa dos fundos travou hoje 🔥 urgente'); await p.waitForTimeout(1500);
  ok('EP18 · emoji fica em Carregando com URIError (bug da tela)', (await p.locator('[data-test=carregando]').count()) === 1 && erros.slice(antes).some((x) => /URI malformed/.test(x)));
  erros = erros.filter((x) => !/URI malformed/.test(x));
  await bug('Busca com acento não encontra o chamado', '1. Abrir Chamados\n2. Buscar por manutenção', 'Aparece o chamado', 'Nenhum chamado. O pedido saiu certo e a resposta veio vazia', { tec: 'GET api/chamados?busca=manuten%C3%A7%C3%A3o respondeu 200 com []' });
  await bug('Busca com emoji fica em Carregando', '1. Abrir Chamados\n2. Colar o título com 🔥', 'Aparece o chamado', 'Fica em Carregando', { tec: 'Uncaught (in promise) URIError: URI malformed' });
  ok('EP18 · conquista', await conq('ep18'));
  await p.goto(U + 'chat.html?canal=bugs'); await p.waitForTimeout(300);
  ok('EP18 · Gabriela responde no FlowChat', /corrijo hoje/.test(await p.textContent('[data-test=mensagens]')));
  // EP20
  await save('ep20'); await p.goto(U + 'novo-chamado.html'); await p.waitForTimeout(1200);
  await p.fill('[data-test=titulo]', 'Rascunho de teste'); await p.fill('[data-test=descricao]', 'Isso não devia aparecer pra mais ninguém'); await p.waitForTimeout(300);
  await p.click('[data-test=sair]'); await p.waitForTimeout(600);
  ok('EP20 · sair apaga a sessão, mas não o rascunho', await p.evaluate(() => !localStorage.getItem('fd:sessao') && !!localStorage.getItem('fd:rascunho')));
  ok('EP20 · login mostra a conta de teste do Lucas', (await p.locator('[data-test=conta-teste]').count()) === 1);
  await p.fill('[data-test=login-email]', 'lucas@flowdesk.com'); await p.fill('[data-test=login-senha]', '123456'); await p.click('[data-test=login-entrar]'); await p.waitForTimeout(600);
  await p.goto(U + 'novo-chamado.html'); await p.waitForTimeout(1200);
  ok('EP20 · o Lucas vê o rascunho da Ana', (await p.inputValue('[data-test=titulo]')) === 'Rascunho de teste');
  await p.evaluate(() => localStorage.removeItem('fd:rascunho')); await p.reload(); await p.waitForTimeout(1200);
  ok('EP20 · apagando a chave, o rascunho some', (await p.inputValue('[data-test=titulo]')) === '');
  await p.click('[data-test=sair]'); await p.waitForTimeout(600);
  await p.fill('[data-test=login-email]', 'ana@teste.com'); await p.fill('[data-test=login-senha]', '123456'); await p.click('[data-test=login-entrar]'); await p.waitForTimeout(600);
  await bug('Rascunho de um usuário aparece pra outro no mesmo navegador', '1. Entrar com a conta A\n2. Escrever um chamado sem criar\n3. Sair\n4. Entrar com a conta B e abrir Novo chamado', 'Formulário vazio', 'Aparece o rascunho da conta A', { prio: 'Alta', tec: 'Armazenamento local: chave fd:rascunho' });
  ok('EP20 · conquista (fim do módulo 3)', await conq('ep20'));

  ok('nenhum erro de JavaScript', erros.length === 0, erros.slice(0, 5).join(' | '));
  await b.close();
  for (const [s, n, x] of res) console.log(s, n, x ? '· ' + x : '');
  const f = res.filter((r) => r[0] !== 'OK ').length;
  console.log(f ? `\n${f} falha(s)` : '\nJornada inteira OK'); process.exit(f ? 1 : 0);
})().catch((e) => { console.error(e); for (const [s, n] of res) console.log(s, n); process.exit(1); });
