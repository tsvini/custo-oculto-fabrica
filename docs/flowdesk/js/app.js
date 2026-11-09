// FlowDesk: site de treino do curso Vida de QA.
// Cada aluno cria a própria conta. Tudo fica salvo só no navegador dele (localStorage).
// ?versao=14 ou ?versao=15 troca a versão do sistema (a 14 é a que está em homologação no curso, com os bugs da sprint).
'use strict';

// ---------- armazenamento ----------
const LS = {
  get(k, d) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* navegador sem armazenamento */ } },
  del(k) { try { localStorage.removeItem(k); } catch (e) { } },
};
const qs = new URLSearchParams(location.search);
if (qs.get('versao')) LS.set('fd:versao', qs.get('versao') === '15' ? 15 : 14);
const VERSAO = LS.get('fd:versao', 14);
// bugs plantados por versão
const BUG = {
  tituloSoEspacos: VERSAO < 15,  // aceita título só com espaços (não usa trim)
  anexo5mbExato: VERSAO < 15,    // recusa o arquivo de exatamente 5 MB (usa >= em vez de >)
};
const LIMITE_ANEXO = 5 * 1024 * 1024;
const FORMATOS = ['pdf', 'png', 'jpg', 'jpeg'];

const contas = () => LS.get('fd:contas', {});
const sessao = () => LS.get('fd:sessao', null);
const chaveDados = () => 'fd:dados:' + sessao();
let D = null;
const dados = () => D || (D = LS.get(chaveDados(), null));
const salvar = () => LS.set(chaveDados(), D);

// ---------- utilidades ----------
const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const agora = () => new Date().toISOString();
const dataBR = (iso) => { const d = new Date(iso); return d.toLocaleDateString('pt-BR') + ' ' + d.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }); };
const hora = (iso) => new Date(iso).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
const tamanho = (b) => b >= 1048576 ? (b / 1048576).toFixed(2).replace('.', ',') + ' MB' : Math.max(1, Math.round(b / 1024)) + ' KB';
const extensao = (n) => (n.split('.').pop() || '').toLowerCase();
function toast(msg, mal = false) {
  $$('.toast').forEach((t) => t.remove());
  const t = document.createElement('div');
  t.className = 'toast' + (mal ? ' mal' : ''); t.setAttribute('data-test', mal ? 'toast-erro' : 'toast-sucesso'); t.setAttribute('role', 'status');
  t.textContent = (mal ? '✕ ' : '✓ ') + msg; document.body.appendChild(t);
  setTimeout(() => t.remove(), 4000);
}
const recado = (msg) => sessionStorage.setItem('fd:toast', msg);
function mostraRecado() { const m = sessionStorage.getItem('fd:toast'); if (m) { sessionStorage.removeItem('fd:toast'); toast(m); } }

// ---------- dados iniciais de toda conta nova ----------
const PESSOAS = {
  beatriz: { nome: 'Beatriz', papel: 'PM' }, rafael: { nome: 'Rafael', papel: 'PO' },
  gabriela: { nome: 'Gabriela', papel: 'Dev' }, lucas: { nome: 'Lucas', papel: 'Tech lead' },
  vinicius: { nome: 'Vinícius', papel: 'QA sênior' }, voce: { nome: 'Você', papel: 'QA' },
};
const COLUNAS = [['afazer', 'A FAZER'], ['dev', 'EM DESENVOLVIMENTO'], ['qa', 'PRONTO PRA QA'], ['teste', 'EM TESTE'], ['concluido', 'CONCLUÍDO']];
const STATUS = ['Aberto', 'Em andamento', 'Resolvido', 'Fechado'];
const REGRAS = ['Título obrigatório', 'Descrição obrigatória', 'Título até 100 caracteres', 'Anexo opcional: PDF, PNG ou JPG até 5 MB', 'Mensagem de sucesso e tela do chamado', 'Status inicial: Aberto'];
const CLIENTES = [
  { nome: 'Padaria Pão Quente', contato: 'Marta Souza', plano: 'Básico' },
  { nome: 'Mercado Bom Preço', contato: 'Carlos Lima', plano: 'Profissional' },
  { nome: 'Clínica Vida', contato: 'Dra. Helena Rocha', plano: 'Profissional' },
  { nome: 'Auto Peças Silva', contato: 'Jorge Silva', plano: 'Básico' },
  { nome: 'Escola Aprender', contato: 'Paula Mendes', plano: 'Empresarial' },
  { nome: 'Studio Fit', contato: 'Renan Alves', plano: 'Básico' },
];
function semente() {
  const dia = (d, h) => { const x = new Date(); x.setDate(x.getDate() - d); x.setHours(h, 12, 0, 0); return x.toISOString(); };
  const ch = (id, titulo, descricao, cliente, status, d, h) => ({ id, titulo, descricao, cliente, status, criadoEm: dia(d, h), criadoPor: 'Cliente', anexo: null, historico: [{ quando: dia(d, h), tx: 'Chamado criado com status Aberto' }] });
  return {
    versaoDados: 1,
    proximoChamado: 1009, proximoBug: 1,
    chamados: [
      ch(1001, 'Não consigo acessar o painel', 'Desde ontem aparece "sessão expirada" logo depois do login.', 'Padaria Pão Quente', 'Resolvido', 9, 10),
      ch(1002, 'Erro ao emitir nota fiscal', 'Quando clico em emitir, a tela fica carregando e não termina.', 'Mercado Bom Preço', 'Em andamento', 6, 15),
      ch(1003, 'Como cadastrar um novo atendente?', 'Contratamos uma pessoa nova e não achei onde cadastrar.', 'Clínica Vida', 'Resolvido', 5, 9),
      ch(1004, 'Relatório mensal veio em branco', 'O relatório de outubro foi gerado sem nenhuma linha.', 'Auto Peças Silva', 'Aberto', 3, 11),
      ch(1005, 'Notificações por e-mail não chegam', 'Os clientes não recebem o aviso de chamado respondido.', 'Escola Aprender', 'Em andamento', 2, 14),
      ch(1006, 'Quero mudar o plano para o anual', 'Gostaria de passar do plano mensal para o anual.', 'Studio Fit', 'Fechado', 2, 16),
      ch(1007, 'Lentidão ao abrir a lista de chamados', 'A lista demora uns 20 segundos pra aparecer.', 'Mercado Bom Preço', 'Aberto', 1, 10),
      ch(1008, 'ajuda', '.', 'Padaria Pão Quente', 'Aberto', 0, 8),
    ],
    cards: [
      { id: 'FD-097', titulo: 'Tela de login', coluna: 'concluido', resp: 'gabriela', tipo: 'story', prioridade: 'Alta', descricao: 'Tela de login com e-mail e senha.', criterios: [], ok: [], comentarios: [] },
      { id: 'FD-101', titulo: 'Criar chamado', coluna: 'qa', resp: 'voce', tipo: 'story', prioridade: 'Normal', descricao: 'Clientes criam chamados sem informação, e depois ninguém sabe o que fazer com eles. Melhorar a tela de criar chamado.',
        criterios: ['Título é obrigatório', 'Descrição é obrigatória', 'Título aceita até 100 caracteres', 'Anexo é opcional: PDF, PNG ou JPG, até 5 MB', 'Depois de criar: mensagem de sucesso e ida pra tela do chamado', 'Chamado novo começa com status Aberto'], ok: [], comentarios: [] },
      { id: 'FD-102', titulo: 'Anexar arquivo ao chamado', coluna: 'dev', resp: 'gabriela', tipo: 'story', prioridade: 'Normal', descricao: 'Permitir anexar mais de um arquivo depois que o chamado já foi criado.', criterios: [], ok: [], comentarios: [] },
      { id: 'FD-104', titulo: 'Filtrar chamados por cliente', coluna: 'afazer', resp: 'rafael', tipo: 'story', prioridade: 'Baixa', descricao: 'Na lista de chamados, filtrar pelo nome do cliente.', criterios: [], ok: [], comentarios: [] },
      { id: 'FD-106', titulo: 'Exportar relatório em PDF', coluna: 'afazer', resp: 'rafael', tipo: 'story', prioridade: 'Baixa', descricao: 'Exportar o relatório mensal em PDF.', criterios: [], ok: [], comentarios: [] },
    ],
    planos: { 'FD-101': [] },
    chat: {
      'time-produto': [
        { de: 'beatriz', tx: 'Bem-vindo ao time! Eu cuido das prioridades e das releases 👋', quando: dia(1, 9) },
        { de: 'rafael', tx: 'E aí! Os cards que você vai testar saem de mim.', quando: dia(1, 9) },
        { de: 'gabriela', tx: 'Oi! Se achar bug, me chama primeiro 😅', quando: dia(1, 9) },
        { de: 'lucas', tx: 'Seja bem-vindo. Daily às 9h15.', quando: dia(1, 9) },
        { de: 'gabriela', tx: 'Bom dia! O FD-101 já está em homologação, pode testar quando quiser 🚀', quando: dia(0, 9) },
      ],
      geral: [{ de: 'beatriz', tx: 'Lembrete: review da sprint na sexta às 16h.', quando: dia(1, 11) }],
      releases: [{ de: 'lucas', tx: 'Release da Sprint 13 publicada. Próxima: sexta, depois da review.', quando: dia(4, 18) }],
      bugs: [{ de: 'vinicius', tx: 'Aqui a gente avisa quando abre bug. Sempre com o link do card 😉', quando: dia(1, 10) }],
    },
  };
}


// ---------- saves por episódio (pontos de continuação do curso) ----------
// Cada save deixa o FlowDesk do jeito que o curso espera naquele ponto. Novos episódios: acrescentar aqui.
const CENARIOS_EP03 = [
  ['Caminho feliz: tudo válido', 'P', '1. Abrir a tela Novo chamado\n2. Preencher título e descrição\n3. Clicar em Criar chamado', 'Mensagem de sucesso, abre a tela do chamado, status Aberto', [4, 5]],
  ['Criar sem título', 'N', '', 'Aparece "Título é obrigatório" e o chamado não é criado', [0]],
  ['Criar sem descrição', 'N', '', 'Aparece "Descrição é obrigatória" e o chamado não é criado', [1]],
  ['Título com 100 caracteres', 'L', '', 'Aceita e cria o chamado', [2]],
  ['Tentar digitar o 101º caractere', 'L', '', 'O campo para em 100 caracteres', [2]],
  ['Anexo PDF de exatamente 5 MB', 'L', '', 'Aceita o anexo e cria o chamado', [3]],
  ['Anexo de 5,1 MB', 'L', '', 'Recusa o arquivo e avisa o limite de 5 MB', [3]],
  ['Anexo em formato .exe', 'N', '', 'Recusa o arquivo: formato não aceito', [3]],
  ['Título só com espaços em branco', 'N', '', 'Nenhuma regra diz o que acontece', []],
].map(([nome, tipo, passos, esperado, regras]) => ({ nome, tipo, passos, esperado, regras, exec: 'nao' }));
const SAVES = [
  { id: 'inicio', nome: 'Começo do curso', quando: 'do EP00 até a prática do EP03', monta: () => semente() },
  { id: 'ep04', nome: 'Início do EP04', quando: 'Cenários em Gherkin', monta: () => { const d = semente(); d.planos['FD-101'] = CENARIOS_EP03.map((c) => ({ ...c })); d.conquistas = ['ep03']; return d; } },
];


// ---------- missões (conferidas pelo próprio site) ----------
// Uma missão por prática guiada. O site confere sozinho e libera a conquista. Novas práticas: acrescentar aqui.
const coberturaFD101 = (d) => new Set((d.planos['FD-101'] || []).flatMap((c) => c.regras)).size;
const MISSOES = [
  { id: 'ep03', titulo: 'Plano de testes do FD-101', aula: 'Prática do EP03', conquista: 'Plano de testes no FlowDesk', nivel: 'QA estagiário', link: 'plano.html', itens: [
    ['Escreva pelo menos 8 cenários', (d) => (d.planos['FD-101'] || []).length >= 8],
    ['Use os três tipos: positivo, negativo e valor limite', (d) => ['P', 'N', 'L'].every((t) => (d.planos['FD-101'] || []).some((c) => c.tipo === t))],
    ['Cubra as 6 regras do card', (d) => coberturaFD101(d) === 6],
    ['Encontre um cenário fora das regras', (d) => (d.planos['FD-101'] || []).some((c) => !c.regras.length)],
  ] },
];
const progresso = (m, d = dados()) => m.itens.map(([, f]) => !!f(d));
const missaoAtual = () => MISSOES.find((m) => !(dados().conquistas || []).includes(m.id)) || null;
function confereMissoes() {
  const d = dados(); d.conquistas = d.conquistas || [];
  MISSOES.forEach((m) => {
    if (d.conquistas.includes(m.id) || !progresso(m, d).every(Boolean)) return;
    d.conquistas.push(m.id); salvar(); conquista(m);
  });
  const el = $('#missaoSide'); if (el) el.outerHTML = cardMissao();
}
function conquista(m) {
  const o = document.createElement('div'); o.className = 'conq-fundo'; o.setAttribute('data-test', 'conquista');
  o.innerHTML = `<div class="conq"><div class="k">🏆 CONQUISTA DESBLOQUEADA</div><div class="v" data-test="conquista-nome">${m.conquista}</div><div class="s">Nível atual: <b>${m.nivel}</b></div><button class="btn" data-test="fechar-conquista">Continuar</button></div>`;
  document.body.appendChild(o); $('[data-test=fechar-conquista]', o).onclick = () => o.remove();
}
function cardMissao() {
  const m = missaoAtual();
  if (!m) return '<a class="missao-side feita" id="missaoSide" href="missoes.html" data-test="missao-atual"><div class="k">MISSÕES</div><div class="t">Tudo feito por agora</div><div class="p">A próxima chega na próxima prática</div></a>';
  const pr = progresso(m), n = pr.filter(Boolean).length;
  return `<a class="missao-side" id="missaoSide" href="missoes.html" data-test="missao-atual"><div class="k">MISSÃO · ${m.aula.toUpperCase()}</div><div class="t">${m.titulo}</div><div class="bar"><i style="width:${n / pr.length * 100}%"></i></div><div class="p" data-test="missao-progresso">${n}/${pr.length}</div><div class="pop" data-test="missao-lista"><div class="k">SUA MISSÃO</div>${m.itens.map(([t], i) => `<div class="pit ${pr[i] ? 'on' : ''}"><b>${pr[i] ? '✓' : i + 1}</b>${t}</div>`).join('')}</div></a>`;
}

// ---------- layout ----------
const avatar = (p) => p === 'voce' ? '<span class="vc">VC</span>' : `<img class="av" src="img/av_${p}.png" alt="">`;
const MARCA = '<span class="marca"><img src="img/icon.png" alt="">FlowDesk</span>';
const pillVersao = () => `<span class="versao" data-test="versao-sistema"><b>Sprint ${VERSAO}</b> · homologação</span>`;
function casca(pagina, conteudo) {
  const c = contas()[sessao()] || { nome: '' };
  const it = (h, n, k) => `<a href="${h}" data-test="menu-${k}" class="${pagina === k ? 'on' : ''}">${n}</a>`;
  document.body.innerHTML = `<div class="app"><aside class="side">${MARCA}<nav>
    ${it('dashboard.html', 'Dashboard', 'dashboard')}${it('chamados.html', 'Chamados', 'chamados')}${it('quadro.html', 'Quadro', 'quadro')}${it('clientes.html', 'Clientes', 'clientes')}
    <div class="grupo">QA</div>${it('plano.html', 'Plano de testes', 'plano')}${it('reportar-bug.html', 'Reportar bug', 'reportar-bug')}
    <div class="grupo">TIME</div>${it('missoes.html', 'Missões', 'missoes')}${it('chat.html', 'FlowChat', 'chat')}${it('configuracoes.html', 'Configurações', 'configuracoes')}</nav>
    ${cardMissao()}<div class="eu"><span class="vc">VC</span><div><b data-test="usuario-logado">${esc(c.nome)}</b><span>QA estagiário</span></div><button data-test="sair">Sair</button></div></aside>
    <main class="main">${conteudo}</main></div>`;
  $('[data-test=sair]').onclick = sair;
  mostraRecado(); setTimeout(confereMissoes, 300);
}
function sair() { LS.del('fd:sessao'); location.href = 'index.html'; }
const topo = (titulo, sub = '', crumb = '') => `<div class="topo"><div>${crumb ? `<div class="crumb">${crumb}</div>` : ''}<h2 data-test="titulo-pagina">${titulo}</h2>${sub ? `<div class="sub">${sub}</div>` : ''}</div>${pillVersao()}</div>`;
const stClasse = (s) => 'st st-' + ({ 'Aberto': 'aberto', 'Em andamento': 'andamento', 'Resolvido': 'resolvido', 'Fechado': 'fechado' }[s] || 'aberto');
const erroCampo = (id, msg) => { const e = $('#' + id); e.classList.add('erro'); const m = document.createElement('div'); m.className = 'msg-erro'; m.setAttribute('data-test', 'erro-' + id); m.textContent = msg; (e.closest('.arquivo') || e).after(m); };
const limpaErros = () => { $$('.msg-erro').forEach((m) => m.remove()); $$('.erro').forEach((e) => e.classList.remove('erro')); };

// ---------- páginas ----------
const PAGINAS = {};

PAGINAS.login = () => {
  if (sessao() && contas()[sessao()]) return location.replace('dashboard.html');
  document.body.innerHTML = `<div class="tela-login"><div class="login">${MARCA}
    <form id="fEntrar" novalidate><h1>Bem-vindo!</h1><p class="sub">Entre com a sua conta da empresa</p>
      <div class="campo"><label for="email">E-mail</label><input class="in" id="email" type="email" data-test="login-email" autocomplete="username"></div>
      <div class="campo"><label for="senha">Senha</label><input class="in" id="senha" type="password" data-test="login-senha" autocomplete="current-password"></div>
      <button class="btn cheio" data-test="login-entrar">Entrar</button>
      <div class="troca">Primeira vez aqui? <button type="button" data-test="ir-criar-conta">Criar minha conta</button></div></form>
    <form id="fCriar" novalidate hidden><h1>Criar conta</h1><p class="sub">Seu primeiro acesso ao FlowDesk</p>
      <div class="campo"><label for="nome">Seu nome</label><input class="in" id="nome" data-test="cadastro-nome" autocomplete="name"></div>
      <div class="campo"><label for="cemail">E-mail</label><input class="in" id="cemail" type="email" data-test="cadastro-email" autocomplete="username"></div>
      <div class="campo"><label for="csenha">Senha <small>(mínimo 6 caracteres)</small></label><input class="in" id="csenha" type="password" data-test="cadastro-senha" autocomplete="new-password"></div>
      <button class="btn cheio" data-test="cadastro-criar">Criar conta e entrar</button>
      <div class="troca">Já tem conta? <button type="button" data-test="ir-entrar">Entrar</button></div></form>
    <p class="aviso">Site de treino do curso <b>Vida de QA</b>. Use dados de mentira: a sua conta e tudo o que você fizer ficam salvos só neste navegador.</p>
  </div></div>`;
  const troca = (criar) => { $('#fEntrar').hidden = criar; $('#fCriar').hidden = !criar; limpaErros(); };
  $('[data-test=ir-criar-conta]').onclick = () => troca(true);
  $('[data-test=ir-entrar]').onclick = () => troca(false);
  const emailOk = (e) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e);
  $('#fEntrar').onsubmit = (ev) => {
    ev.preventDefault(); limpaErros();
    const e = $('#email').value.trim().toLowerCase(), s = $('#senha').value;
    if (!e) return erroCampo('email', 'Preencha o e-mail');
    if (!s) return erroCampo('senha', 'Preencha a senha');
    const c = contas()[e];
    if (!c || c.senha !== s) return erroCampo('senha', 'E-mail ou senha incorretos');
    LS.set('fd:sessao', e); location.href = 'dashboard.html';
  };
  $('#fCriar').onsubmit = (ev) => {
    ev.preventDefault(); limpaErros();
    const n = $('#nome').value.trim(), e = $('#cemail').value.trim().toLowerCase(), s = $('#csenha').value;
    let ok = true;
    if (!n) { erroCampo('nome', 'Preencha o seu nome'); ok = false; }
    if (!e) { erroCampo('cemail', 'Preencha o e-mail'); ok = false; } else if (!emailOk(e)) { erroCampo('cemail', 'E-mail inválido'); ok = false; } else if (contas()[e]) { erroCampo('cemail', 'Já existe uma conta com esse e-mail'); ok = false; }
    if (s.length < 6) { erroCampo('csenha', 'A senha precisa ter pelo menos 6 caracteres'); ok = false; }
    if (!ok) return;
    const cs = contas(); cs[e] = { nome: n, senha: s, criadaEm: agora() }; LS.set('fd:contas', cs);
    LS.set('fd:sessao', e); LS.set('fd:dados:' + e, semente());
    recado('Conta criada. Bem-vindo ao FlowDesk!'); location.href = 'dashboard.html';
  };
};

PAGINAS.dashboard = () => {
  const d = dados(), c = contas()[sessao()];
  const h = new Date().getHours(), oi = h < 12 ? 'Bom dia' : h < 18 ? 'Boa tarde' : 'Boa noite';
  const n = (s) => d.chamados.filter((x) => x.status === s).length;
  const meus = d.cards.filter((x) => x.resp === 'voce');
  const ult = [...d.chamados].sort((a, b) => b.criadoEm.localeCompare(a.criadoEm)).slice(0, 5);
  casca('dashboard', topo(`${oi}, ${esc(c.nome.split(' ')[0])}! 👋`, `Workspace FlowDesk · Sprint ${VERSAO}`) + `
    <div class="kpis"><div class="kpi"><div class="l">Chamados abertos</div><div class="n" data-test="kpi-abertos">${n('Aberto')}</div></div>
    <div class="kpi"><div class="l">Em andamento</div><div class="n" data-test="kpi-andamento">${n('Em andamento')}</div></div>
    <div class="kpi"><div class="l">Resolvidos</div><div class="n" data-test="kpi-resolvidos">${n('Resolvido')}</div></div></div>
    <div class="bloco"><h3>Seus cards</h3>${meus.length ? meus.map((k) => `<a class="tk meu" href="card.html?id=${k.id}" data-test="meu-card" style="max-width:420px;cursor:pointer"><div class="id">${k.id}</div><div class="t">${esc(k.titulo)}</div><div class="who">${COLUNAS.find((x) => x[0] === k.coluna)[1]}</div></a>`).join('') : '<div class="vazio">Nenhum card com você agora.</div>'}</div>
    <div class="bloco"><h3>Últimos chamados</h3><table class="tabela"><thead><tr><th>#</th><th>TÍTULO</th><th>CLIENTE</th><th>STATUS</th></tr></thead><tbody>
    ${ult.map((x) => `<tr><td class="num">${x.id}</td><td><a href="chamado.html?id=${x.id}">${esc(x.titulo)}</a></td><td>${esc(x.cliente)}</td><td><span class="${stClasse(x.status)}">${x.status}</span></td></tr>`).join('')}</tbody></table></div>`);
};

PAGINAS.chamados = () => {
  casca('chamados', topo('Chamados', 'Todas as solicitações de atendimento dos clientes') + `
    <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:16px">
      <input class="in" id="busca" placeholder="Buscar pelo título…" data-test="busca-chamado" style="max-width:320px">
      <select class="in" id="filtro" data-test="filtro-status" style="max-width:220px"><option value="">Todos os status</option>${STATUS.map((s) => `<option>${s}</option>`).join('')}</select>
      <a class="btn" href="novo-chamado.html" data-test="novo-chamado" style="margin-left:auto">+ Novo chamado</a></div>
    <table class="tabela"><thead><tr><th>#</th><th>TÍTULO</th><th>CLIENTE</th><th>STATUS</th><th>CRIADO EM</th></tr></thead><tbody id="linhas"></tbody></table>`);
  const pinta = () => {
    const b = $('#busca').value.trim().toLowerCase(), f = $('#filtro').value;
    const l = [...dados().chamados].sort((a, c) => c.id - a.id).filter((x) => (!f || x.status === f) && x.titulo.toLowerCase().includes(b));
    $('#linhas').innerHTML = l.length ? l.map((x) => `<tr data-test="linha-chamado"><td class="num">${x.id}</td><td><a href="chamado.html?id=${x.id}" data-test="link-chamado">${esc(x.titulo) || '<i style="color:#5b5f78">(sem título)</i>'}</a></td><td>${esc(x.cliente)}</td><td><span class="${stClasse(x.status)}" data-test="status">${x.status}</span></td><td>${dataBR(x.criadoEm)}</td></tr>`).join('')
      : '<tr><td colspan="5" class="vazio" data-test="lista-vazia">Nenhum chamado encontrado</td></tr>';
  };
  $('#busca').oninput = pinta; $('#filtro').onchange = pinta; pinta();
};

PAGINAS['novo-chamado'] = () => {
  casca('chamados', topo('Novo chamado', 'Registre uma nova solicitação de atendimento', '<a href="chamados.html">Chamados</a> / Novo') + `
    <form class="fcard" id="f" novalidate>
      <div class="campo"><label for="titulo">Título <i>*</i><span class="contador" data-test="contador-titulo" id="cont">0/100</span></label><input class="in" id="titulo" maxlength="100" data-test="titulo" placeholder="Resuma o problema em uma frase"></div>
      <div class="campo"><label for="descricao">Descrição <i>*</i></label><textarea class="in" id="descricao" data-test="descricao" placeholder="Descreva o problema…"></textarea></div>
      <div class="campo"><label for="cliente">Cliente</label><select class="in" id="cliente" data-test="cliente">${CLIENTES.map((c) => `<option>${c.nome}</option>`).join('')}</select></div>
      <div class="campo"><label>Anexo <small>(opcional · PDF, PNG ou JPG até 5 MB)</small></label>
        <label class="arquivo" for="anexo"><input type="file" id="anexo" data-test="anexo" accept=".pdf,.png,.jpg,.jpeg"><span class="btn sec peq">Escolher arquivo</span><span class="nome" id="nomeArq" data-test="nome-anexo">Nenhum arquivo escolhido</span><button type="button" class="icone" id="tiraArq" data-test="remover-anexo" hidden>Remover</button></label></div>
      <div class="fbtns"><a class="btn sec" href="chamados.html" data-test="cancelar">Cancelar</a><button class="btn" data-test="criar-chamado">Criar chamado</button></div>
    </form>`);
  let arquivo = null;
  $('#titulo').oninput = () => { $('#cont').textContent = $('#titulo').value.length + '/100'; };
  const validaArquivo = (f) => {
    if (!FORMATOS.includes(extensao(f.name))) return 'Formato não aceito. Envie PDF, PNG ou JPG';
    if (BUG.anexo5mbExato ? f.size >= LIMITE_ANEXO : f.size > LIMITE_ANEXO) return 'O arquivo passa do limite de 5 MB';
    return '';
  };
  $('#anexo').onchange = () => {
    limpaErros(); const f = $('#anexo').files[0]; if (!f) return;
    const e = validaArquivo(f);
    if (e) { arquivo = null; $('#anexo').value = ''; $('#nomeArq').textContent = 'Nenhum arquivo escolhido'; $('#tiraArq').hidden = true; return erroCampo('anexo', e); }
    arquivo = { nome: f.name, tamanho: f.size }; $('#nomeArq').textContent = `${f.name} (${tamanho(f.size)})`; $('#tiraArq').hidden = false;
  };
  $('#tiraArq').onclick = (ev) => { ev.preventDefault(); arquivo = null; $('#anexo').value = ''; $('#nomeArq').textContent = 'Nenhum arquivo escolhido'; $('#tiraArq').hidden = true; };
  $('#f').onsubmit = (ev) => {
    ev.preventDefault(); limpaErros();
    const t = $('#titulo').value, ds = $('#descricao').value;
    let ok = true;
    if (BUG.tituloSoEspacos ? t.length === 0 : t.trim().length === 0) { erroCampo('titulo', 'Título é obrigatório'); ok = false; }
    if (ds.trim().length === 0) { erroCampo('descricao', 'Descrição é obrigatória'); ok = false; }
    if (!ok) return;
    const d = dados(), id = d.proximoChamado++;
    d.chamados.push({ id, titulo: BUG.tituloSoEspacos ? t : t.trim(), descricao: ds.trim(), cliente: $('#cliente').value, status: 'Aberto', criadoEm: agora(), criadoPor: 'Você', anexo: arquivo, historico: [{ quando: agora(), tx: 'Chamado criado com status Aberto' }] });
    salvar(); recado('Chamado criado com sucesso'); location.href = 'chamado.html?id=' + id;
  };
};

PAGINAS.chamado = () => {
  const id = Number(qs.get('id')), x = dados().chamados.find((c) => c.id === id);
  if (!x) return casca('chamados', topo('Chamado não encontrado', `Não existe chamado com o número ${esc(qs.get('id'))}.`) + '<a class="btn sec" href="chamados.html">Voltar pra lista</a>');
  casca('chamados', topo(`<span>#${x.id}</span> · <span style="color:var(--txt)" data-test="chamado-titulo">${esc(x.titulo) || '<i style="color:#5b5f78">(sem título)</i>'}</span>`, '', '<a href="chamados.html">Chamados</a> / #' + x.id) + `
    <div class="meta"><div class="mi"><div class="k">STATUS</div><div class="v"><span class="${stClasse(x.status)}" data-test="chamado-status">${x.status}</span></div></div>
      <div class="mi"><div class="k">CLIENTE</div><div class="v" data-test="chamado-cliente">${esc(x.cliente)}</div></div>
      <div class="mi"><div class="k">CRIADO POR</div><div class="v">${x.criadoPor === 'Você' ? '<span class="vc">VC</span>Você' : esc(x.criadoPor)}</div></div>
      <div class="mi"><div class="k">CRIADO EM</div><div class="v">${dataBR(x.criadoEm)}</div></div></div>
    <div class="sec"><div class="k">Descrição</div><div class="v" data-test="chamado-descricao">${esc(x.descricao)}</div></div>
    <div class="sec"><div class="k">Anexo</div>${x.anexo ? `<div class="v" data-test="chamado-anexo">📎 ${esc(x.anexo.nome)} <span style="color:var(--mut)">(${tamanho(x.anexo.tamanho)})</span></div>` : '<div class="v nada" data-test="chamado-anexo">Nenhum anexo</div>'}</div>
    <div class="sec"><div class="k">Mudar status</div><div style="display:flex;gap:10px;flex-wrap:wrap"><select class="in" id="novoSt" data-test="mudar-status" style="max-width:240px">${STATUS.map((s) => `<option ${s === x.status ? 'selected' : ''}>${s}</option>`).join('')}</select><button class="btn" id="salvaSt" data-test="salvar-status">Salvar status</button></div></div>
    <div class="sec"><div class="k">Histórico</div><div class="hist" data-test="historico">${x.historico.map((h) => `<div>${dataBR(h.quando)} · ${esc(h.tx)}</div>`).join('')}</div></div>`);
  $('#salvaSt').onclick = () => {
    const s = $('#novoSt').value; if (s === x.status) return toast('O chamado já está com esse status', true);
    x.historico.push({ quando: agora(), tx: `Status mudou de ${x.status} para ${s}` }); x.status = s; salvar();
    recado('Status atualizado para ' + s); location.reload();
  };
};

PAGINAS.quadro = () => {
  casca('quadro', topo(`Sprint ${VERSAO}`, 'Objetivo: melhorar o fluxo de criar chamado') + `<div class="cols">${COLUNAS.map(([k, n]) => `<div class="col ${k === 'qa' ? 'qa' : ''}" data-col="${k}" data-test="coluna-${k}"><div class="h">${n}<span data-test="contagem-${k}"></span></div><div class="cards"></div></div>`).join('')}</div>
    <p class="dica" style="margin-top:10px">Arraste o card pra outra coluna, ou abra o card e use "Mover para".</p>`);
  const pinta = () => {
    COLUNAS.forEach(([k]) => {
      const l = dados().cards.filter((c) => c.coluna === k), col = $(`[data-col=${k}]`);
      $('.cards', col).innerHTML = l.map((c) => `<a class="tk ${c.resp === 'voce' ? 'meu' : ''} ${c.tipo === 'bug' ? 'e-bug' : ''}" href="card.html?id=${c.id}" draggable="true" data-id="${c.id}" data-test="card-${c.id}"><div class="id">${c.id}${c.tipo === 'bug' ? '<span class="bug">BUG</span>' : ''}</div><div class="t">${esc(c.titulo)}</div><div class="who">${avatar(c.resp)}${c.resp === 'voce' ? '<span style="color:#fff;font-weight:700">Você · QA</span>' : PESSOAS[c.resp].nome}</div></a>`).join('');
      $('[data-test=contagem-' + k + ']', col).textContent = l.length || '';
    });
    $$('.tk').forEach((t) => { t.ondragstart = (e) => e.dataTransfer.setData('text/plain', t.dataset.id); });
  };
  $$('.col').forEach((col) => {
    col.ondragover = (e) => { e.preventDefault(); col.classList.add('sobre'); };
    col.ondragleave = () => col.classList.remove('sobre');
    col.ondrop = (e) => { e.preventDefault(); col.classList.remove('sobre'); const c = dados().cards.find((x) => x.id === e.dataTransfer.getData('text/plain')); if (c && c.coluna !== col.dataset.col) { c.coluna = col.dataset.col; salvar(); pinta(); toast(`${c.id} movido para ${COLUNAS.find((x) => x[0] === c.coluna)[1]}`); } };
  });
  pinta();
};

PAGINAS.card = () => {
  const d = dados(), c = d.cards.find((x) => x.id === (qs.get('id') || '').toUpperCase());
  if (!c) return casca('quadro', topo('Card não encontrado') + '<a class="btn sec" href="quadro.html">Voltar pro quadro</a>');
  const bug = c.tipo === 'bug';
  const campo = (k, v) => `<div class="sec"><div class="k">${k}</div>${v ? `<div class="v">${esc(v)}</div>` : '<div class="v nada">Nada informado.</div>'}</div>`;
  casca('quadro', topo(`<span>${c.id}</span> · <span style="color:var(--txt)" data-test="card-titulo">${esc(c.titulo)}</span>`, '', `<a href="quadro.html">Quadro</a> / Sprint ${VERSAO} · ${bug ? 'Bug' : 'User story'}`) + `
    <div class="meta"><div class="mi"><div class="k">${bug ? 'SEVERIDADE' : 'PRIORIDADE'}</div><div class="v" data-test="card-prioridade">${esc(bug ? c.severidade : c.prioridade)}</div></div>
      <div class="mi"><div class="k">RESPONSÁVEL</div><div class="v">${avatar(c.resp)}${PESSOAS[c.resp].nome}</div></div>
      <div class="mi"><div class="k">MOVER PARA</div><div class="v"><select class="in" id="mover" data-test="mover-card" style="height:34px;font-size:14px;min-width:200px">${COLUNAS.map(([k, n]) => `<option value="${k}" ${k === c.coluna ? 'selected' : ''}>${n}</option>`).join('')}</select></div></div></div>
    ${bug ? `<div class="sec"><div class="k">Card relacionado</div><div class="v">${c.relacionado ? `<a href="card.html?id=${c.relacionado}">${c.relacionado}</a>` : '—'}</div></div>` + campo('Passos para reproduzir', c.passos) + campo('Resultado esperado', c.esperado) + campo('Resultado obtido', c.obtido) + campo('Evidência', c.evidencia ? '📎 ' + c.evidencia : '')
      : campo('Descrição', c.descricao) + `<div class="sec" id="sCrit"><div class="k">Critérios de aceite</div>${c.criterios.length ? c.criterios.map((k, i) => `<label class="cr"><input type="checkbox" data-i="${i}" data-test="criterio" ${c.ok.includes(i) ? 'checked' : ''}>${esc(k)}</label>`).join('') : '<div class="v nada">Nenhum critério definido.</div>'}</div>`}
    ${d.planos[c.id] ? `<div style="margin-top:16px"><a class="btn" href="plano.html?card=${c.id}" data-test="abrir-plano">Abrir plano de testes</a></div>` : ''}
    <div class="sec"><div class="k">Comentários</div><div id="coms">${c.comentarios.map((m) => `<div class="coment">${avatar('voce')}<div class="bx"><b>Você</b><small>${dataBR(m.quando)}</small><div>${esc(m.tx)}</div></div></div>`).join('') || '<div class="v nada" style="font-size:15px">Nenhum comentário ainda.</div>'}</div>
      <div style="display:flex;gap:10px;margin-top:12px"><input class="in" id="com" placeholder="Escreva um comentário…" data-test="comentario"><button class="btn" id="enviaCom" data-test="enviar-comentario">Comentar</button></div></div>`);
  $('#mover').onchange = () => { c.coluna = $('#mover').value; salvar(); toast(`${c.id} movido para ${COLUNAS.find((x) => x[0] === c.coluna)[1]}`); };
  $$('[data-test=criterio]').forEach((k) => { k.onchange = () => { const i = +k.dataset.i; c.ok = k.checked ? [...new Set([...c.ok, i])] : c.ok.filter((x) => x !== i); salvar(); }; });
  $('#enviaCom').onclick = () => { const t = $('#com').value.trim(); if (!t) return; c.comentarios.push({ tx: t, quando: agora() }); salvar(); location.reload(); };
};

PAGINAS.plano = () => {
  const d = dados(), id = (qs.get('card') || 'FD-101').toUpperCase();
  if (!d.planos[id]) return casca('plano', topo('Plano de testes') + '<div class="vazio">Esse card ainda não tem plano de testes.</div>');
  const card = d.cards.find((x) => x.id === id);
  const TIPOS = { P: ['POSITIVO', 'tP'], N: ['NEGATIVO', 'tN'], L: ['VALOR LIMITE', 'tL'] };
  casca('plano', topo(`<span>${id}</span> · Plano de testes`, 'Cada cenário: uma situação, os passos e o resultado esperado', `<a href="card.html?id=${id}">${id} · ${esc(card.titulo)}</a>`) + `
    <div class="plano"><div class="esq">
      <table class="tabela"><thead><tr><th style="width:44px">#</th><th>CENÁRIO</th><th>RESULTADO ESPERADO</th><th style="width:150px">EXECUÇÃO</th><th style="width:110px"></th></tr></thead><tbody id="linhas"></tbody></table>
      <form class="fcard" id="f" novalidate style="margin-top:18px;max-width:none"><h3 style="font-size:18px;margin-bottom:14px" id="fTit">Novo cenário</h3>
        <div style="display:flex;gap:14px;flex-wrap:wrap"><div class="campo" style="flex:2;min-width:240px"><label for="cNome">Cenário <i>*</i></label><input class="in" id="cNome" data-test="cenario-nome" placeholder="Ex.: Criar sem título"></div>
          <div class="campo" style="flex:1;min-width:170px"><label for="cTipo">Tipo</label><select class="in" id="cTipo" data-test="cenario-tipo"><option value="P">Positivo</option><option value="N">Negativo</option><option value="L">Valor limite</option></select></div></div>
        <div class="campo"><label for="cPassos">Passos</label><textarea class="in" id="cPassos" data-test="cenario-passos" placeholder="1. Abrir a tela Novo chamado&#10;2. …"></textarea></div>
        <div class="campo"><label for="cEsp">Resultado esperado <i>*</i></label><input class="in" id="cEsp" data-test="cenario-esperado" placeholder="Seja específico: o que aparece, onde, e o que acontece com o chamado"></div>
        <div class="campo"><label>Quais regras esse cenário cobre?</label><div class="regras-check">${REGRAS.map((r, i) => `<label class="cr"><input type="checkbox" value="${i}" data-test="cenario-regra">${r}</label>`).join('')}</div></div>
        <div class="fbtns"><button type="button" class="btn sec" id="cancela" hidden data-test="cancelar-edicao">Cancelar</button><button class="btn" data-test="salvar-cenario" id="salva">Adicionar cenário</button></div>
      </form></div>
      <aside><div class="cov" id="cov" data-test="cobertura"><div class="hd">Cobertura das regras<span class="cnt" id="cnt" data-test="cobertura-contagem">0/6</span></div><div class="bar"><i id="bar"></i></div>
        ${REGRAS.map((r, i) => `<div class="rl" id="u${i}" data-test="regra"><b>✓</b>${r}<span class="q" id="q${i}" hidden></span></div>`).join('')}<div class="ex" id="ex" hidden></div></div>
        <div class="bloco arqs"><h3>Arquivos de teste</h3><p class="dica" style="margin:-4px 0 8px">Gerados na hora, no tamanho exato, pra testar o anexo.</p>
          ${[['documento-5MB-exato.pdf', LIMITE_ANEXO], ['documento-5,1MB.pdf', Math.floor(5.1 * 1048576)], ['documento-1MB.pdf', 1048576], ['print-da-tela.png', 48 * 1024], ['foto.jpg', 220 * 1024], ['programa.exe', 12 * 1024]].map(([n, b]) => `<a href="#" data-arq="${n}" data-b="${b}" data-test="arquivo-teste">${n}<small>${tamanho(b)}</small></a>`).join('')}</div></aside></div>`);
  const lista = d.planos[id];
  let editando = null;
  const pinta = () => {
    $('#linhas').innerHTML = lista.length ? lista.map((c, i) => {
      const fora = !c.regras.length, t = TIPOS[c.tipo];
      return `<tr class="${fora ? 'fora' : ''}" data-test="linha-cenario"><td class="num">${i + 1}</td><td><div class="cn">${esc(c.nome)}</div><span class="tg ${fora ? 'tX' : t[1]}">${fora ? 'FORA DAS REGRAS' : t[0]}</span>${fora ? ` <span class="tg ${t[1]}">${t[0]}</span>` : ''}${c.passos ? `<div class="dica" style="white-space:pre-wrap">${esc(c.passos)}</div>` : ''}</td><td class="res">${esc(c.esperado)}</td>
        <td><select class="exec ${c.exec}" data-i="${i}" data-test="execucao"><option value="nao" ${c.exec === 'nao' ? 'selected' : ''}>Não executado</option><option value="passou" ${c.exec === 'passou' ? 'selected' : ''}>Passou</option><option value="falhou" ${c.exec === 'falhou' ? 'selected' : ''}>Falhou</option></select></td>
        <td><div class="acoes"><button class="icone" data-ed="${i}" data-test="editar-cenario">Editar</button><button class="icone" data-rm="${i}" data-test="excluir-cenario">✕</button></div></td></tr>`;
    }).join('') : '<tr><td colspan="5" class="vazio" data-test="plano-vazio">Nenhum cenário ainda</td></tr>';
    let n = 0;
    REGRAS.forEach((r, i) => { const quem = lista.map((c, j) => c.regras.includes(i) ? j + 1 : 0).filter(Boolean); const on = quem.length > 0; if (on) n++; $('#u' + i).classList.toggle('on', on); $('#q' + i).hidden = !on; $('#q' + i).textContent = quem.length === 1 ? 'CENÁRIO ' + quem[0] : quem.join(' · '); });
    setTimeout(confereMissoes, 400);
    $('#cnt').textContent = n + '/6'; $('#bar').style.width = (n / 6 * 100) + '%'; $('#cov').classList.toggle('done', n === 6);
    const fora = lista.map((c, j) => c.regras.length ? 0 : j + 1).filter(Boolean);
    $('#ex').hidden = !fora.length; $('#ex').textContent = `+ Cenário ${fora.join(', ')}: fora das regras`;
    $$('[data-test=execucao]').forEach((s) => { s.onchange = () => { lista[+s.dataset.i].exec = s.value; salvar(); s.className = 'exec ' + s.value; }; });
    $$('[data-ed]').forEach((b) => { b.onclick = () => edita(+b.dataset.ed); });
    $$('[data-rm]').forEach((b) => { b.onclick = () => { lista.splice(+b.dataset.rm, 1); salvar(); pinta(); toast('Cenário excluído'); }; });
  };
  const limpa = () => { editando = null; $('#f').reset(); $('#fTit').textContent = 'Novo cenário'; $('#salva').textContent = 'Adicionar cenário'; $('#cancela').hidden = true; limpaErros(); };
  const edita = (i) => {
    const c = lista[i]; editando = i; limpaErros();
    $('#cNome').value = c.nome; $('#cTipo').value = c.tipo; $('#cPassos').value = c.passos; $('#cEsp').value = c.esperado;
    $$('[data-test=cenario-regra]').forEach((k) => { k.checked = c.regras.includes(+k.value); });
    $('#fTit').textContent = `Editando o cenário ${i + 1}`; $('#salva').textContent = 'Salvar cenário'; $('#cancela').hidden = false; $('#f').scrollIntoView({ behavior: 'smooth' });
  };
  $('#cancela').onclick = limpa;
  $('#f').onsubmit = (ev) => {
    ev.preventDefault(); limpaErros();
    const nome = $('#cNome').value.trim(), esp = $('#cEsp').value.trim(); let ok = true;
    if (!nome) { erroCampo('cNome', 'Dê um nome pro cenário'); ok = false; }
    if (!esp) { erroCampo('cEsp', 'Escreva o resultado esperado'); ok = false; }
    if (!ok) return;
    const c = { nome, tipo: $('#cTipo').value, passos: $('#cPassos').value.trim(), esperado: esp, regras: $$('[data-test=cenario-regra]').filter((k) => k.checked).map((k) => +k.value), exec: 'nao' };
    if (editando !== null) { c.exec = lista[editando].exec; lista[editando] = c; toast('Cenário salvo'); } else { lista.push(c); toast('Cenário adicionado'); }
    salvar(); limpa(); pinta();
  };
  $$('[data-arq]').forEach((a) => {
    a.onclick = (ev) => {
      ev.preventDefault();
      const n = a.dataset.arq, b = +a.dataset.b, bytes = new Uint8Array(b), cab = { pdf: '%PDF-1.4\n', png: '\x89PNG\r\n\x1a\n', jpg: '\xff\xd8\xff\xe0', exe: 'MZ' }[extensao(n)] || '';
      for (let i = 0; i < cab.length; i++) bytes[i] = cab.charCodeAt(i) & 255;
      const url = URL.createObjectURL(new Blob([bytes])); const l = document.createElement('a'); l.href = url; l.download = n; document.body.appendChild(l); l.click(); l.remove(); setTimeout(() => URL.revokeObjectURL(url), 2000);
    };
  });
  pinta();
};

PAGINAS['reportar-bug'] = () => {
  const d = dados();
  casca('reportar-bug', topo('Reportar bug', 'Abra o card do bug que você encontrou. Ele vai pro quadro, com a Gabriela.') + `
    <form class="fcard" id="f" novalidate>
      <div class="campo"><label for="bTitulo">Título <i>*</i></label><input class="in" id="bTitulo" data-test="bug-titulo" placeholder="O que acontece, e onde"></div>
      <div style="display:flex;gap:14px;flex-wrap:wrap"><div class="campo" style="flex:1;min-width:200px"><label for="bCard">Card relacionado</label><select class="in" id="bCard" data-test="bug-card"><option value="">Nenhum</option>${d.cards.filter((c) => c.tipo !== 'bug').map((c) => `<option value="${c.id}" ${c.id === 'FD-101' ? 'selected' : ''}>${c.id} · ${esc(c.titulo)}</option>`).join('')}</select></div>
        <div class="campo" style="flex:1;min-width:200px"><label for="bSev">Severidade <i>*</i></label><select class="in" id="bSev" data-test="bug-severidade"><option value="">Escolha…</option><option>Baixa</option><option>Média</option><option>Alta</option><option>Crítica</option></select></div></div>
      <div class="campo"><label for="bPassos">Passos para reproduzir <i>*</i></label><textarea class="in" id="bPassos" data-test="bug-passos" placeholder="1. …&#10;2. …&#10;3. …"></textarea></div>
      <div class="campo"><label for="bEsp">Resultado esperado <i>*</i></label><input class="in" id="bEsp" data-test="bug-esperado"></div>
      <div class="campo"><label for="bObt">Resultado obtido <i>*</i></label><input class="in" id="bObt" data-test="bug-obtido"></div>
      <div class="campo"><label>Evidência <small>(print ou vídeo, opcional)</small></label><label class="arquivo" for="bEvid"><input type="file" id="bEvid" data-test="bug-evidencia"><span class="btn sec peq">Escolher arquivo</span><span class="nome" id="nomeEv">Nenhum arquivo escolhido</span></label></div>
      <div class="fbtns"><a class="btn sec" href="quadro.html">Cancelar</a><button class="btn" data-test="abrir-bug">Abrir bug</button></div></form>`);
  $('#bEvid').onchange = () => { const f = $('#bEvid').files[0]; $('#nomeEv').textContent = f ? f.name : 'Nenhum arquivo escolhido'; };
  $('#f').onsubmit = (ev) => {
    ev.preventDefault(); limpaErros(); let ok = true;
    const v = (i) => $('#' + i).value.trim();
    [['bTitulo', 'Dê um título pro bug'], ['bSev', 'Escolha a severidade'], ['bPassos', 'Escreva os passos pra reproduzir'], ['bEsp', 'Escreva o resultado esperado'], ['bObt', 'Escreva o resultado obtido']].forEach(([i, m]) => { if (!v(i)) { erroCampo(i, m); ok = false; } });
    if (!ok) return;
    const id = 'BUG-' + d.proximoBug++, f = $('#bEvid').files[0];
    d.cards.push({ id, titulo: v('bTitulo'), coluna: 'afazer', resp: 'gabriela', tipo: 'bug', severidade: v('bSev'), relacionado: v('bCard'), passos: v('bPassos'), esperado: v('bEsp'), obtido: v('bObt'), evidencia: f ? f.name : '', criterios: [], ok: [], comentarios: [], criadoEm: agora() });
    d.chat.bugs.push({ de: 'voce', tx: `Abri o ${id}: ${v('bTitulo')}`, quando: agora() });
    salvar(); recado(`${id} aberto e enviado pra Gabriela`); location.href = 'card.html?id=' + id;
  };
};


PAGINAS.missoes = () => {
  const d = dados(), feitas = d.conquistas || [];
  casca('missoes', topo('Missões', 'Cada prática do curso tem uma missão. O FlowDesk confere sozinho.') + MISSOES.map((m) => {
    const pr = progresso(m, d), ok = feitas.includes(m.id);
    return `<div class="missao ${ok ? 'ok' : ''}" data-test="missao-${m.id}"><div class="k">${ok ? '🏆 CONQUISTA DESBLOQUEADA' : 'MISSÃO'} · ${m.aula.toUpperCase()}</div><div class="v">${m.titulo}</div>
      ${m.itens.map(([t], i) => `<div class="mit ${pr[i] ? 'on' : ''}" data-test="missao-item"><b>✓</b>${t}</div>`).join('')}
      ${ok ? `<div class="s">Conquista: <b>${m.conquista}</b></div>` : `<a class="btn peq" href="${m.link}" style="margin-top:8px">Ir pra missão</a>`}</div>`;
  }).join('') + '<p class="dica" style="margin-top:14px">Novas missões aparecem aqui conforme o curso avança.</p>');
};

PAGINAS.clientes = () => {
  const d = dados();
  casca('clientes', topo('Clientes', 'Empresas que usam o FlowDesk') + `<table class="tabela"><thead><tr><th>CLIENTE</th><th>CONTATO</th><th>PLANO</th><th>CHAMADOS</th></tr></thead><tbody>
    ${CLIENTES.map((c) => `<tr data-test="linha-cliente"><td><b>${c.nome}</b></td><td>${c.contato}</td><td>${c.plano}</td><td>${d.chamados.filter((x) => x.cliente === c.nome).length}</td></tr>`).join('')}</tbody></table>`);
};

PAGINAS.chat = () => {
  const d = dados(), canal = d.chat[qs.get('canal')] ? qs.get('canal') : 'time-produto', l = d.chat[canal];
  document.body.innerHTML = `<div class="chat"><div class="chan"><span class="marca" style="font-size:18px"><img src="img/icon.png" alt="" style="height:28px">FlowChat</span>
      <div class="t">CANAIS</div>${Object.keys(d.chat).map((k) => `<a href="chat.html?canal=${k}" class="${k === canal ? 'on' : ''}" data-test="canal-${k}"># ${k}</a>`).join('')}
      <a href="dashboard.html" style="margin-top:auto;color:var(--mut);font-size:14px" data-test="voltar-flowdesk">← Voltar pro FlowDesk</a></div>
    <div class="msgs"><div class="chead"># ${canal}<span>6 membros</span></div><div class="lista" id="lista" data-test="mensagens">
      ${l.map((m) => `<div class="msg" data-test="mensagem">${m.de === 'voce' ? '<span class="vc">VC</span>' : `<img src="img/av_${m.de}.png" alt="">`}<div><div class="who">${PESSOAS[m.de].nome}<i>${PESSOAS[m.de].papel}</i><small>${hora(m.quando)}</small></div><div class="tx">${esc(m.tx)}</div></div></div>`).join('')}</div>
      <form class="composer" id="f"><input class="in" id="tx" placeholder="Escreva uma mensagem…" data-test="mensagem-texto" autocomplete="off"><button class="btn" data-test="enviar-mensagem">Enviar</button></form></div></div>`;
  $('#lista').scrollTop = 1e9;
  $('#f').onsubmit = (ev) => { ev.preventDefault(); const t = $('#tx').value.trim(); if (!t) return; l.push({ de: 'voce', tx: t, quando: agora() }); salvar(); location.reload(); };
};

PAGINAS.configuracoes = () => {
  const cs = contas(), c = cs[sessao()];
  casca('configuracoes', topo('Configurações') + `
    <div class="fcard"><div class="campo"><label for="cfNome">Seu nome</label><div style="display:flex;gap:10px"><input class="in" id="cfNome" value="${esc(c.nome)}" data-test="config-nome"><button class="btn" id="salvaNome" data-test="salvar-nome">Salvar</button></div></div>
      <div class="campo"><label>E-mail</label><input class="in" value="${esc(sessao())}" disabled></div>
      <div class="campo"><label for="cfVer">Versão do sistema</label><select class="in" id="cfVer" data-test="config-versao"><option value="14" ${VERSAO === 14 ? 'selected' : ''}>Sprint 14 · homologação</option><option value="15" ${VERSAO === 15 ? 'selected' : ''}>Sprint 15 · homologação</option></select><div class="dica">O curso diz quando trocar de versão.</div></div></div>
    <div class="fcard" style="margin-top:18px"><h3 style="font-size:17px;margin-bottom:6px">Carregar save do curso</h3><p class="dica" style="margin-bottom:12px">Perdeu o progresso, trocou de computador ou pulou uma aula? Carregue o ponto do curso em que você está. O FlowDesk fica do jeito que o vídeo espera. <b>Isso substitui o que você tem agora.</b></p>
      <div style="display:flex;gap:10px;flex-wrap:wrap"><select class="in" id="cfSave" data-test="save-episodio" style="max-width:420px">${SAVES.map((x) => `<option value="${x.id}">${x.nome} · ${x.quando}</option>`).join('')}</select><button class="btn" id="carregaSave" data-test="carregar-save">Carregar save</button></div>
      <div id="confSave" hidden style="margin-top:12px"><b>Tem certeza?</b> O que você fez até agora vai ser trocado pelo save. <button class="btn peq" id="saveSim" data-test="confirmar-save">Sim, carregar</button> <button class="btn sec peq" id="saveNao">Cancelar</button></div></div>
    <div class="fcard" style="margin-top:18px"><h3 style="font-size:17px;margin-bottom:6px">Levar o progresso pra outro computador</h3><p class="dica" style="margin-bottom:12px">Baixe um arquivo com tudo o que você fez. No outro computador, crie a conta e importe o arquivo.</p>
      <div style="display:flex;gap:10px;flex-wrap:wrap"><button class="btn sec" id="exporta" data-test="exportar-progresso">Exportar progresso</button><label class="btn sec" for="importa" style="cursor:pointer">Importar progresso<input type="file" id="importa" accept=".json,application/json" data-test="importar-progresso" hidden></label></div></div>
    <div class="fcard" style="margin-top:18px;border-color:#5b1d24"><h3 style="font-size:17px;margin-bottom:6px">Recomeçar do zero</h3><p class="dica" style="margin-bottom:12px">Apaga os chamados, cards, cenários e mensagens que você criou e volta tudo pro começo do curso. A sua conta continua.</p>
      <button class="btn perigo" id="zera" data-test="recomecar">Recomeçar do zero</button>
      <div id="conf" hidden style="margin-top:12px"><b>Tem certeza?</b> Isso não tem volta. <button class="btn perigo peq" id="zeraSim" data-test="confirmar-recomecar">Sim, apagar tudo</button> <button class="btn sec peq" id="zeraNao">Cancelar</button></div></div>`);
  $('#salvaNome').onclick = () => { const n = $('#cfNome').value.trim(); if (!n) return toast('O nome não pode ficar vazio', true); c.nome = n; LS.set('fd:contas', cs); recado('Nome salvo'); location.reload(); };
  $('#cfVer').onchange = () => { LS.set('fd:versao', +$('#cfVer').value); recado('Versão trocada para a Sprint ' + $('#cfVer').value); location.reload(); };
  $('#carregaSave').onclick = () => { $('#confSave').hidden = false; };
  $('#saveNao').onclick = () => { $('#confSave').hidden = true; };
  $('#saveSim').onclick = () => { const sv = SAVES.find((x) => x.id === $('#cfSave').value); LS.set(chaveDados(), sv.monta()); recado(`Save carregado: ${sv.nome}`); location.href = 'dashboard.html'; };
  $('#exporta').onclick = () => {
    const arq = { app: 'flowdesk', formato: 1, nome: c.nome, exportadoEm: agora(), dados: dados() };
    const url = URL.createObjectURL(new Blob([JSON.stringify(arq, null, 1)], { type: 'application/json' }));
    const l = document.createElement('a'); l.href = url; l.download = `flowdesk-progresso-${new Date().toISOString().slice(0, 10)}.json`; document.body.appendChild(l); l.click(); l.remove(); setTimeout(() => URL.revokeObjectURL(url), 2000);
    toast('Progresso exportado');
  };
  $('#importa').onchange = async () => {
    const f = $('#importa').files[0]; if (!f) return;
    try {
      const arq = JSON.parse(await f.text());
      if (arq.app !== 'flowdesk' || !arq.dados || !Array.isArray(arq.dados.chamados) || !Array.isArray(arq.dados.cards)) throw new Error();
      LS.set(chaveDados(), arq.dados); recado('Progresso importado'); location.href = 'dashboard.html';
    } catch (e) { $('#importa').value = ''; toast('Esse arquivo não é um progresso do FlowDesk', true); }
  };
  $('#zera').onclick = () => { $('#conf').hidden = false; };
  $('#zeraNao').onclick = () => { $('#conf').hidden = true; };
  $('#zeraSim').onclick = () => { LS.set(chaveDados(), semente()); recado('Tudo zerado. Bom recomeço!'); location.href = 'dashboard.html'; };
};

// ---------- início ----------
(function () {
  const p = document.body.dataset.page;
  if (p !== 'login') {
    if (!sessao() || !contas()[sessao()]) return location.replace('index.html');
    if (!dados()) { D = semente(); salvar(); }
  }
  PAGINAS[p]();
})();
