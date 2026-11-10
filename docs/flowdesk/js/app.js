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
  { id: 'inicio', nome: 'Começo do curso', quando: 'do EP00 ao EP04', monta: () => semente() },
  { id: 'ep04', nome: 'Início do EP05', quando: 'Cenários em Gherkin', monta: () => { const d = semente(); d.planos['FD-101'] = CENARIOS_EP03.map((c) => ({ ...c })); d.conquistas = ['ep03']; return d; } },
  { id: 'ep06', nome: 'Início do EP06', quando: 'Prática do Gherkin', monta: () => { const d = semente(); d.planos['FD-101'] = CENARIOS_EP03.map((c) => ({ ...c })); d.conquistas = ['ep03']; return d; } },
  { id: 'ep07', nome: 'Início do EP07', quando: 'Primeiro bug', monta: () => { const d = semente(); d.planos['FD-101'] = CENARIOS_EP03.map((c) => ({ ...c })); d.gherkin = { 'FD-101': GK_EP06 }; d.conquistas = ['ep03', 'ep06']; return d; } },
  { id: 'ep08', nome: 'Início do EP08', quando: 'Executar o plano', monta: () => { const d = semente(); d.planos['FD-101'] = CENARIOS_EP03.map((c) => ({ ...c })); d.gherkin = { 'FD-101': GK_EP06 }; d.conquistas = ['ep03', 'ep06']; return d; } },
];


// ---------- missões (conferidas pelo próprio site) ----------
// Uma missão por prática guiada. O site confere sozinho e libera a conquista. Novas práticas: acrescentar aqui.
const coberturaFD101 = (d) => new Set((d.planos['FD-101'] || []).flatMap((c) => c.regras)).size;
const MISSOES = [
  { id: 'ep03', titulo: 'Plano de testes do FD-101', aula: 'EP04', conquista: 'Plano de testes no FlowDesk', nivel: 'QA estagiário', link: 'card.html?id=FD-101&aba=plano', itens: [
    ['Escreva pelo menos 8 cenários', (d) => (d.planos['FD-101'] || []).length >= 8],
    ['Use os três tipos: positivo, negativo e valor limite', (d) => ['P', 'N', 'L'].every((t) => (d.planos['FD-101'] || []).some((c) => c.tipo === t))],
    ['Cubra as 6 regras do card', (d) => coberturaFD101(d) === 6],
    ['Encontre um cenário fora das regras', (d) => (d.planos['FD-101'] || []).some((c) => !c.regras.length)],
  ] },
  { id: 'ep06', titulo: 'Cenários do FD-101 em Gherkin', aula: 'EP06', conquista: 'Feature do FD-101 no FlowDesk', nivel: 'QA estagiário', link: 'card.html?id=FD-101&aba=gherkin', itens: [
    ['Comece pela Funcionalidade', (d) => revisaGherkin(gherkinDe(d)).funcionalidade],
    ['Escreva pelo menos 4 cenários', (d) => revisaGherkin(gherkinDe(d)).cenarios.length >= 4],
    ['Todo cenário com Dado, Quando e Então', (d) => { const r = revisaGherkin(gherkinDe(d)); return r.cenarios.length > 0 && r.cenarios.every((c) => c.dado && c.quando && c.entao && !c.ordem); }],
    ['Um Quando por cenário: uma ação só', (d) => { const r = revisaGherkin(gherkinDe(d)); return r.cenarios.length > 0 && r.cenarios.every((c) => c.acoes <= 1); }],
    ['Nenhum Então vago', (d) => { const r = revisaGherkin(gherkinDe(d)); return r.cenarios.length > 0 && r.cenarios.every((c) => !c.vago.length); }],
  ] },
  { id: 'ep08', titulo: 'Executar o plano do FD-101', aula: 'EP08', conquista: 'Primeiros bugs achados', nivel: 'QA júnior', link: 'card.html?id=FD-101&aba=plano', itens: [
    ['Execute todos os cenários do plano', (d) => { const l = d.planos['FD-101'] || []; return l.length >= 8 && l.every((c) => c.exec && c.exec !== 'nao'); }],
    ['Reporte o bug do título só com espaços', (d) => bugsDe(d).some((b) => /espa[çc]o/i.test(textoBug(b)))],
    ['Ache e reporte o bug do anexo', (d) => bugsDe(d).some((b) => /anexo|5\s?mb|arquivo/i.test(textoBug(b)))],
    ['Todo cenário que falhou tem um bug ligado', (d) => { const f = (d.planos['FD-101'] || []).filter((c) => c.exec === 'falhou'); return f.length > 0 && f.every((c) => c.bug); }],
  ] },
];
const bugsDe = (d) => d.cards.filter((c) => c.tipo === 'bug');
const textoBug = (b) => [b.titulo, b.passos, b.esperado, b.obtido, b.cenario].join(' ');

// ---------- Gherkin (EP06): leitura e revisão do arquivo .feature ----------
const GK_INICIO = 'Funcionalidade: Criar chamado\n\n';
const GK_EP06 = "Funcionalidade: Criar chamado\n\n  Cenário: Criar chamado com sucesso\n    Dado que estou na tela \"Novo chamado\"\n    E preenchi o título e a descrição\n    Quando clico em \"Criar chamado\"\n    Então vejo a mensagem de sucesso\n    E o chamado aparece com o status \"Aberto\"\n\n  Cenário: Criar chamado sem título\n    Dado que estou na tela \"Novo chamado\"\n    E preenchi a descrição\n    E deixei o título vazio\n    Quando clico em \"Criar chamado\"\n    Então vejo \"Título é obrigatório\"\n    E o chamado não é criado\n\n  Cenário: Criar chamado sem descrição\n    Dado que estou na tela \"Novo chamado\"\n    E preenchi o título\n    E deixei a descrição vazia\n    Quando clico em \"Criar chamado\"\n    Então vejo \"Descrição é obrigatória\"\n    E o chamado não é criado\n\n  Cenário: Título com 100 caracteres\n    Dado que estou na tela \"Novo chamado\"\n    E preenchi o título com 100 caracteres\n    Quando clico em \"Criar chamado\"\n    Então o chamado é criado\n";  // o arquivo do jeito que fica no fim do EP06
const gherkinDe = (d, id = 'FD-101') => (d.gherkin || {})[id] ?? GK_INICIO;
const GK_PASSO = /^(Dado|Dada|Dados|Dadas|Quando|Então|Entao|E|Mas)\b/;
const GK_VAGO = /\b(erro|funciona|funcionar|corretamente|certo|ok|normal|deve dar)\b/i;
function revisaGherkin(txt) {
  const linhas = txt.split('\n'); const r = { funcionalidade: false, cenarios: [], soltas: [] };
  let atual = null, ultimo = null, viuAlgo = false;
  linhas.forEach((bruta, i) => {
    const l = bruta.trim(); if (!l || l.startsWith('#')) return;
    if (/^Funcionalidade:/.test(l)) { if (!viuAlgo) r.funcionalidade = true; viuAlgo = true; return; }
    viuAlgo = true;
    if (/^(Cenário|Cenario|Esquema do Cenário|Esquema do cenário):/.test(l)) {
      atual = { nome: l.replace(/^[^:]+:\s*/, '') || '(sem nome)', linha: i + 1, dado: false, quando: false, entao: false, acoes: 0, ordem: false, vago: [] }; r.cenarios.push(atual); ultimo = null; return;
    }
    const m = l.match(GK_PASSO);
    if (!m) { if (atual && !/^(Exemplos:|\|)/.test(l)) r.soltas.push(i + 1); return; }
    if (!atual) { r.soltas.push(i + 1); return; }
    let k = m[1]; if (k === 'E' || k === 'Mas') k = ultimo || 'dado'; else k = /^Dad/.test(k) ? 'dado' : k === 'Quando' ? 'quando' : 'entao';
    if (k === 'dado' && (atual.quando || atual.entao)) atual.ordem = true;
    if (k === 'quando' && atual.entao) atual.ordem = true;
    atual[k] = true; if (k === 'quando') atual.acoes += 1 + (l.match(/\se\s+(clico|preencho|digito|envio|seleciono|anexo|abro|salvo|apago|escolho)\b/gi) || []).length;
    if (k === 'entao' && GK_VAGO.test(l) && !/"[^"]+"/.test(l)) atual.vago.push(i + 1);
    ultimo = k;
  });
  return r;
}
function pintaGherkin(txt) {
  return txt.split('\n').map((l) => {
    let h = esc(l);
    if (/^\s*#/.test(l)) return `<span class="gc">${h}</span>`;
    h = h.replace(/^(\s*)(Funcionalidade:|Cenário:|Cenario:|Esquema do [Cc]enário:|Exemplos:|Contexto:)/, '$1<span class="gf">$2</span>')
      .replace(/^(\s*)(Dado|Dada|Dados|Dadas|Quando|Então|Entao|E|Mas)\b/, '$1<span class="gk">$2</span>')
      .replace(/&quot;([^&]*?)&quot;/g, '<span class="gs">&quot;$1&quot;</span>');
    return h;
  }).join('\n') + '\n';
}
const progresso = (m, d = dados()) => m.itens.map(([, f]) => !!f(d));
const missaoAtual = () => MISSOES.find((m) => !(dados().conquistas || []).includes(m.id)) || null;
function nivelAtual() { const d = dados() || {}; const fe = MISSOES.filter((m) => (d.conquistas || []).includes(m.id)); return fe.length ? fe[fe.length - 1].nivel : 'QA estagiário'; }
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
  const nv = $('[data-test=nivel]'); if (nv) nv.textContent = m.nivel;
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
const ICONE = {
  dashboard: '<path d="M3 10.5 12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>',
  chamados: '<path d="M4 5h16v14H4z"/><path d="M8 9h8M8 13h5"/>',
  quadro: '<path d="M4 4h4v16H4zM10 4h4v10h-4zM16 4h4v13h-4z"/>',
  plano: '<path d="M9 5h11M9 12h11M9 19h11"/><path d="m3.5 5 1.5 1.5L7.5 4M3.5 12l1.5 1.5L7.5 11M3.5 19l1.5 1.5L7.5 18"/>',
  chat: '<path d="M4 5h16v11H9l-5 4z"/>',
  configuracoes: '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1 7 17M17 7l2.1-2.1"/>',
};
const ico = (k) => `<svg viewBox="0 0 24 24" aria-hidden="true">${ICONE[k]}</svg>`;
function casca(pagina, conteudo) {
  const c = contas()[sessao()] || { nome: '' };
  const it = (h, n, k) => `<a href="${h}" data-test="menu-${k}" class="${pagina === k ? 'on' : ''}">${ico(k)}<span>${n}</span></a>`;
  document.body.innerHTML = `<div class="app"><aside class="side">${MARCA}<nav>
    ${it('dashboard.html', 'Início', 'dashboard')}${it('chamados.html', 'Chamados', 'chamados')}${it('quadro.html', 'Quadro', 'quadro')}${it('chat.html', 'FlowChat', 'chat')}</nav>
    <div class="side-fim">${cardMissao()}<nav class="sec-nav">${it('configuracoes.html', 'Configurações', 'configuracoes')}</nav>
    <div class="eu"><span class="vc">VC</span><div><b data-test="usuario-logado">${esc(c.nome)}</b><span data-test="nivel">${nivelAtual()}</span></div><button data-test="sair">Sair</button></div></div></aside>
    <main class="main"><div class="conteudo">${conteudo}</div></main></div>`;
  $('[data-test=sair]').onclick = sair;
  mostraRecado(); setTimeout(confereMissoes, 300);
}
function sair() { LS.del('fd:sessao'); location.href = 'index.html'; }
const topo = (titulo, sub = '', crumb = '', acoes = '') => `<div class="topo"><div>${crumb ? `<div class="crumb">${crumb}</div>` : ''}<h2 data-test="titulo-pagina">${titulo}</h2>${sub ? `<div class="sub">${sub}</div>` : ''}</div><div class="topo-acoes">${acoes}${pillVersao()}</div></div>`;
const stClasse = (s) => 'st st-' + ({ 'Aberto': 'aberto', 'Em andamento': 'andamento', 'Resolvido': 'resolvido', 'Fechado': 'fechado' }[s] || 'aberto');
const erroCampo = (id, msg) => { const e = $('#' + id); e.classList.add('erro'); const m = document.createElement('div'); m.className = 'msg-erro'; m.setAttribute('data-test', 'erro-' + id); m.textContent = msg; (e.closest('.arquivo') || e).after(m); };
const limpaErros = () => { $$('.msg-erro').forEach((m) => m.remove()); $$('.erro').forEach((e) => e.classList.remove('erro')); };

// ---------- quem pode mover o quê ----------
// O QA só move os próprios cards: de Pronto pra QA pra Em teste (e de volta), e de Em teste pra Concluído quando todos os critérios estão marcados.
const MOVES_QA = { qa: ['teste'], teste: ['qa', 'concluido'] };
function podeMover(c, destino) {
  if (c.coluna === destino) return { ok: false, msg: '' };
  if (c.resp !== 'voce') return { ok: false, msg: `Esse card é ${c.resp === 'gabriela' || c.resp === 'beatriz' ? 'da' : 'do'} ${PESSOAS[c.resp].nome}. Só quem é responsável move.` };
  if (!(MOVES_QA[c.coluna] || []).includes(destino)) return { ok: false, msg: 'O QA não faz esse movimento. Daqui o card só vai pra ' + (MOVES_QA[c.coluna] || []).map((k) => COLUNAS.find((x) => x[0] === k)[1].toLowerCase()).join(' ou ') + '.' };
  if (destino === 'concluido' && c.criterios.length && c.ok.length < c.criterios.length) return { ok: false, msg: 'Antes de concluir, marque no card os critérios de aceite que você validou.' };
  return { ok: true };
}

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
  const ult = [...d.chamados].sort((a, b) => b.criadoEm.localeCompare(a.criadoEm)).slice(0, 4);
  const m = missaoAtual(), pr = m ? progresso(m, d) : [];
  const hero = m ? `<a class="hero" href="${m.link}" data-test="missao-hero"><div class="hk">Missão do ${m.aula}</div><div class="ht">${m.titulo}</div>
      <div class="hl">${m.itens.map(([t], i) => `<div class="pit ${pr[i] ? 'on' : ''}"><b>${pr[i] ? '✓' : i + 1}</b>${t}</div>`).join('')}</div><span class="btn">Continuar a missão</span></a>`
    : `<div class="hero feita"><div class="hk">Missões</div><div class="ht">Tudo feito por agora</div><p class="dica">A próxima missão chega na próxima prática do curso.</p></div>`;
  casca('dashboard', topo(`${oi}, ${esc(c.nome.split(' ')[0])}`, `Sprint ${VERSAO} do FlowDesk`) + `
    <div class="inicio"><div>${hero}</div>
      <div class="lado"><div class="numeros"><div><span data-test="kpi-abertos">${n('Aberto')}</span>abertos</div><div><span data-test="kpi-andamento">${n('Em andamento')}</span>em andamento</div><div><span data-test="kpi-resolvidos">${n('Resolvido')}</span>resolvidos</div></div>
        <h3 class="tit">Seus cards</h3>${meus.length ? meus.map(cardFace).join('') : '<p class="dica">Nenhum card com você agora.</p>'}
        <h3 class="tit">Últimos chamados</h3><div class="lista-simples">${ult.map((x) => `<a href="chamado.html?id=${x.id}"><span class="num">#${x.id}</span><span class="tx">${esc(x.titulo)}</span><span class="${stClasse(x.status)}">${x.status}</span></a>`).join('')}</div></div></div>`);
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

// ---------- quadro (estilo ferramenta de tarefas: status coloridos, etiquetas, prioridade, progresso) ----------
const COR_COLUNA = { afazer: '#8E92A4', dev: '#3B82F6', qa: '#A78BFA', teste: '#F59E0B', concluido: '#22C55E' };
const PRIOS = ['Baixa', 'Normal', 'Alta', 'Urgente'];
const prioDe = (c) => ({ 'Média': 'Normal', 'Crítica': 'Urgente' }[c.prioridade || c.severidade] || c.prioridade || c.severidade || 'Normal');
const flag = (p) => `<span class="flag f-${p.toLowerCase()}"><svg viewBox="0 0 24 24"><path d="M5 21V4h11l-1.5 4L16 12H5"/></svg>${p}</span>`;
const etiqueta = (c) => c.tipo === 'bug' ? '<span class="etq etq-bug">bug</span>' : c.tipo === 'melhoria' ? '<span class="etq etq-mel">melhoria</span>' : '<span class="etq etq-story">história</span>';
const nomeColuna = (k) => COLUNAS.find((x) => x[0] === k)[1];
function cardFace(c) {
  const d = dados(), plano = d.planos[c.id], tot = c.criterios.length, ok = c.ok.length;
  return `<a class="tk ${c.resp === 'voce' ? 'meu' : 'travado'} ${c.tipo === 'bug' ? 'e-bug' : ''}" href="card.html?id=${c.id}" draggable="${c.resp === 'voce'}" ${c.resp === 'voce' ? '' : `title="Card de ${PESSOAS[c.resp].nome}: só quem é responsável move"`} data-id="${c.id}" data-test="card-${c.id}">
    <div class="tk-etq">${etiqueta(c)}<span class="id">${c.id}</span></div><div class="t">${esc(c.titulo)}</div>
    <div class="tk-meta">${flag(prioDe(c))}${plano && plano.length ? `<span class="mini" title="Cenários no plano de testes">☑ ${plano.length}</span>` : ''}${c.comentarios.length ? `<span class="mini" title="Comentários">💬 ${c.comentarios.length}</span>` : ''}<span class="tk-av">${avatar(c.resp)}</span></div>
    ${tot ? `<div class="tk-prog" title="Critérios de aceite validados"><i style="width:${ok / tot * 100}%"></i></div><div class="tk-prog-n">${ok}/${tot} critérios</div>` : ''}</a>`;
}
PAGINAS.quadro = () => {
  casca('quadro', topo(`Sprint ${VERSAO}`, 'Objetivo: melhorar o fluxo de criar chamado') + `<div class="cols">${COLUNAS.map(([k, n]) => `<div class="col" data-col="${k}" data-test="coluna-${k}" style="--cor:${COR_COLUNA[k]}">
      <div class="h"><span class="pill-st"><i></i>${n}</span><span class="cnt" data-test="contagem-${k}"></span>${k === 'afazer' ? '<button class="mais" data-test="nova-tarefa" title="Nova tarefa">+</button>' : ''}</div>
      <div class="cards"></div>${k === 'afazer' ? '<button class="add-tarefa" data-test="adicionar-tarefa">+ Adicionar tarefa</button>' : ''}</div>`).join('')}</div>
    <p class="dica" style="margin-top:12px">Você move os seus cards arrastando, ou pelo próprio card. Os cards dos outros ficam com eles.</p>`);
  const pinta = () => {
    COLUNAS.forEach(([k]) => {
      const l = dados().cards.filter((c) => c.coluna === k), col = $(`[data-col=${k}]`);
      $('.cards', col).innerHTML = l.map(cardFace).join('');
      $('[data-test=contagem-' + k + ']', col).textContent = l.length || '';
    });
    $$('.tk').forEach((t) => { t.ondragstart = (e) => { if (t.getAttribute('draggable') !== 'true') return e.preventDefault(); e.dataTransfer.setData('text/plain', t.dataset.id); }; });
  };
  $$('.col').forEach((col) => {
    col.ondragover = (e) => { e.preventDefault(); col.classList.add('sobre'); };
    col.ondragleave = () => col.classList.remove('sobre');
    col.ondrop = (e) => {
      e.preventDefault(); col.classList.remove('sobre');
      const c = dados().cards.find((x) => x.id === e.dataTransfer.getData('text/plain')); if (!c) return;
      const p = podeMover(c, col.dataset.col); if (!p.ok) { if (p.msg) toast(p.msg, true); return; }
      c.coluna = col.dataset.col; salvar(); pinta(); toast(`${c.id} movido para ${nomeColuna(c.coluna).toLowerCase()}`);
    };
  });
  $$('[data-test=nova-tarefa],[data-test=adicionar-tarefa]').forEach((b) => { b.onclick = () => novaTarefa(pinta); });
  pinta();
  if (qs.get('novo') === 'bug') novaTarefa(pinta);
};
function novaTarefa(depois, ctx) {
  const d = dados();
  const o = document.createElement('div'); o.className = 'modal-fundo'; o.setAttribute('data-test', 'modal-nova-tarefa');
  o.innerHTML = `<form class="modal" id="fT" novalidate><div class="modal-h"><h3>Nova tarefa</h3><button type="button" class="icone" data-fecha data-test="fechar-modal">✕</button></div>
    <div class="seg" role="radiogroup"><label data-test="tipo-bug"><input type="radio" name="tipo" value="bug" checked><span>Bug</span></label><label data-test="tipo-melhoria"><input type="radio" name="tipo" value="melhoria"><span>Melhoria</span></label></div>
    <div class="campo"><label for="tTitulo">Título <i>*</i></label><input class="in" id="tTitulo" data-test="tarefa-titulo" placeholder="O que acontece, e onde"></div>
    <div class="linha2"><div class="campo"><label for="tPrio">Prioridade</label><select class="in" id="tPrio" data-test="tarefa-prioridade">${PRIOS.map((p) => `<option ${p === 'Normal' ? 'selected' : ''}>${p}</option>`).join('')}</select></div>
      <div class="campo"><label for="tCard">Card relacionado</label><select class="in" id="tCard" data-test="tarefa-card"><option value="">Nenhum</option>${d.cards.filter((c) => c.tipo !== 'bug').map((c) => `<option value="${c.id}" ${c.id === 'FD-101' ? 'selected' : ''}>${c.id} · ${esc(c.titulo)}</option>`).join('')}</select></div></div>
    ${ctx ? `<p class="liga" data-test="bug-cenario">🔗 Ligado ao cenário ${ctx.n} do plano: <b>${esc(ctx.nome)}</b></p>` : ''}
    <div class="so-bug"><div class="campo"><label for="tPassos">Passos para reproduzir <i>*</i></label><textarea class="in" id="tPassos" data-test="bug-passos" placeholder="1. …&#10;2. …&#10;3. …"></textarea></div>
      <div class="linha2"><div class="campo"><label for="tEsp">Resultado esperado <i>*</i></label><input class="in" id="tEsp" data-test="bug-esperado"></div><div class="campo"><label for="tObt">Resultado obtido <i>*</i></label><input class="in" id="tObt" data-test="bug-obtido"></div></div>
      <div class="campo"><label>Evidência <small>(print ou vídeo, opcional)</small></label><label class="arquivo" for="tEvid"><input type="file" id="tEvid" data-test="bug-evidencia"><span class="btn sec peq">Escolher arquivo</span><span class="nome" id="nomeEv">Nenhum arquivo escolhido</span></label></div></div>
    <div class="so-mel" hidden><div class="campo"><label for="tDesc">Descrição <i>*</i></label><textarea class="in" id="tDesc" data-test="melhoria-descricao" placeholder="O que poderia ser melhor, e por quê"></textarea></div></div>
    <p class="dica" id="tDest">O bug vai pra coluna A fazer, com a Gabriela.</p>
    <div class="fbtns"><button type="button" class="btn sec" data-fecha>Cancelar</button><button class="btn" data-test="criar-tarefa">Criar tarefa</button></div></form>`;
  document.body.appendChild(o);
  const fecha = () => o.remove();
  $$('[data-fecha]', o).forEach((b) => { b.onclick = fecha; });
  o.onclick = (e) => { if (e.target === o) fecha(); };
  const tipo = () => $('input[name=tipo]:checked', o).value;
  $$('input[name=tipo]', o).forEach((r) => { r.onchange = () => { const bug = tipo() === 'bug'; $('.so-bug', o).hidden = !bug; $('.so-mel', o).hidden = bug; $('#tDest').textContent = bug ? 'O bug vai pra coluna A fazer, com a Gabriela.' : 'A melhoria vai pra coluna A fazer, com o Rafael, que decide se entra na sprint.'; limpaErros(); }; });
  $('#tEvid').onchange = () => { const f = $('#tEvid').files[0]; $('#nomeEv').textContent = f ? f.name : 'Nenhum arquivo escolhido'; };
  $('#tTitulo').focus();
  $('#fT').onsubmit = (ev) => {
    ev.preventDefault(); limpaErros(); let ok = true; const v = (i) => $('#' + i).value.trim(), bug = tipo() === 'bug';
    const obrig = [['tTitulo', 'Dê um título pra tarefa']].concat(bug ? [['tPassos', 'Escreva os passos pra reproduzir'], ['tEsp', 'Escreva o resultado esperado'], ['tObt', 'Escreva o resultado obtido']] : [['tDesc', 'Descreva a melhoria']]);
    obrig.forEach(([i, m]) => { if (!v(i)) { erroCampo(i, m); ok = false; } });
    if (!ok) return;
    let id;
    if (bug) {
      id = 'BUG-' + String(d.proximoBug++).padStart(2, '0'); const f = $('#tEvid').files[0];
      d.cards.push({ id, titulo: v('tTitulo'), coluna: 'afazer', resp: 'gabriela', tipo: 'bug', prioridade: v('tPrio'), relacionado: v('tCard'), cenario: ctx ? ctx.nome : '', passos: v('tPassos'), esperado: v('tEsp'), obtido: v('tObt'), evidencia: f ? f.name : '', criterios: [], ok: [], comentarios: [], criadoEm: agora() });
      d.chat.bugs.push({ de: 'voce', tx: `Abri o ${id}: ${v('tTitulo')}`, quando: agora() });
    } else {
      d.proximoMelhoria = d.proximoMelhoria || 1; id = 'MEL-' + d.proximoMelhoria++;
      d.cards.push({ id, titulo: v('tTitulo'), coluna: 'afazer', resp: 'rafael', tipo: 'melhoria', prioridade: v('tPrio'), relacionado: v('tCard'), descricao: v('tDesc'), criterios: [], ok: [], comentarios: [], criadoEm: agora() });
    }
    if (bug && ctx) { const l = d.planos[ctx.card] || []; if (l[ctx.i]) l[ctx.i].bug = id; }
    salvar(); fecha(); toast(`${id} criado${bug ? ' e enviado pra Gabriela' : ''}`); if (depois) depois(id); confereMissoes();
  };
}

// ---------- card (detalhes, plano de testes e comentários em abas) ----------
PAGINAS.card = () => {
  const d = dados(), c = d.cards.find((x) => x.id === (qs.get('id') || '').toUpperCase());
  if (!c) return casca('quadro', topo('Card não encontrado') + '<a class="btn sec" href="quadro.html">Voltar pro quadro</a>');
  const temPlano = !!d.planos[c.id];
  const abas = [['detalhes', 'Detalhes'], ...(temPlano ? [['plano', 'Plano de testes'], ['gherkin', 'Gherkin']] : []), ['comentarios', 'Comentários']];
  let aba = abas.some(([k]) => k === qs.get('aba')) ? qs.get('aba') : 'detalhes';
  const tot = c.criterios.length;
  casca('quadro', `<div class="topo"><div><div class="crumb"><a href="quadro.html">Quadro</a> / Sprint ${VERSAO}</div>
      <h2 data-test="titulo-pagina">${etiqueta(c)} <span style="color:var(--acc2)">${c.id}</span> · <span data-test="card-titulo" style="color:var(--txt)">${esc(c.titulo)}</span></h2></div><div class="topo-acoes">${pillVersao()}</div></div>
    <div class="meta">
      <div class="mi"><div class="k">Status</div><div class="v">${c.resp === 'voce' ? `<select class="in" id="mover" data-test="mover-card" style="height:32px;font-size:14px;min-width:190px">${COLUNAS.filter(([k]) => k === c.coluna || (MOVES_QA[c.coluna] || []).includes(k)).map(([k, n]) => `<option value="${k}" ${k === c.coluna ? 'selected' : ''}>${n}</option>`).join('')}</select>` : `<span class="pill-st" style="--cor:${COR_COLUNA[c.coluna]}" data-test="coluna-card"><i></i>${nomeColuna(c.coluna)}</span>`}</div></div>
      <div class="mi"><div class="k">Responsável</div><div class="v">${avatar(c.resp)}${PESSOAS[c.resp].nome}</div></div>
      <div class="mi"><div class="k">Prioridade</div><div class="v" data-test="card-prioridade">${flag(prioDe(c))}</div></div>
      ${tot ? `<div class="mi"><div class="k">Critérios</div><div class="v" id="critN">${c.ok.length}/${tot}</div></div>` : ''}</div>
    <nav class="abas">${abas.map(([k, n]) => `<button class="${k === aba ? 'on' : ''}" data-aba="${k}" data-test="aba-${k}">${n}<span class="n" id="n-${k}"></span></button>`).join('')}</nav>
    <div id="abaConteudo"></div>`);
  const contagens = () => { if ($('#n-plano')) $('#n-plano').textContent = d.planos[c.id].length || ''; if ($('#n-gherkin')) $('#n-gherkin').textContent = revisaGherkin(gherkinDe(dados(), c.id)).cenarios.length || ''; $('#n-comentarios').textContent = c.comentarios.length || ''; };
  const campo = (k, v) => `<div class="sec"><div class="k">${k}</div>${v ? `<div class="v">${esc(v)}</div>` : '<div class="v nada">Nada informado.</div>'}</div>`;
  const mostra = (k) => {
    aba = k; $$('.abas button').forEach((b) => b.classList.toggle('on', b.dataset.aba === k));
    history.replaceState(null, '', `card.html?id=${c.id}${k === 'detalhes' ? '' : '&aba=' + k}`);
    const A = $('#abaConteudo');
    if (k === 'detalhes') {
      A.innerHTML = c.tipo === 'bug'
        ? `<div class="sec"><div class="k">Card relacionado</div><div class="v">${c.relacionado ? `<a href="card.html?id=${c.relacionado}">${c.relacionado}</a>` : '—'}</div></div>` + campo('Passos para reproduzir', c.passos) + campo('Resultado esperado', c.esperado) + campo('Resultado obtido', c.obtido) + campo('Evidência', c.evidencia ? '📎 ' + c.evidencia : '')
        : campo('Descrição', c.descricao) + (c.tipo === 'melhoria' ? '' : `<div class="sec" id="sCrit"><div class="k">Critérios de aceite</div>${tot ? c.criterios.map((k2, i) => `<label class="cr"><input type="checkbox" data-i="${i}" data-test="criterio" ${c.ok.includes(i) ? 'checked' : ''}>${esc(k2)}</label>`).join('') : '<div class="v nada">Nenhum critério definido.</div>'}</div>`)
          + (temPlano ? `<div style="margin-top:16px"><button class="btn" data-test="abrir-plano" id="abrePlano">Abrir plano de testes</button></div>` : '');
      if (c.tipo !== 'bug' && temPlano) {
        const pl = d.planos[c.id], ex = pl.filter((x) => x.exec === 'passou' || x.exec === 'falhou').length, fal = pl.filter((x) => x.exec === 'falhou').length, bugs = pl.filter((x) => x.bug).length, gk = revisaGherkin(gherkinDe(dados(), c.id)).cenarios.length;
        const linha = (n, l, cor) => `<div class="rs-l"><span>${l}</span><b${cor ? ` style="color:${cor}"` : ''}>${n}</b></div>`;
        A.innerHTML = `<div class="det"><div class="det-e">${A.innerHTML}</div><aside class="rs" data-test="resumo-card"><div class="rs-k">Resumo do teste</div>${linha(pl.length, 'Cenários no plano')}${linha(gk, 'Cenários em Gherkin')}${linha(`${ex}/${pl.length}`, 'Executados')}${linha(fal, 'Falharam', fal ? '#fca5a5' : '')}${linha(bugs, 'Bugs ligados', bugs ? '#c4b5fd' : '')}<div class="rs-bar"><i style="width:${pl.length ? ex / pl.length * 100 : 0}%"></i></div></aside></div>`;
      }
      $$('[data-test=criterio]').forEach((k2) => { k2.onchange = () => { const i = +k2.dataset.i; c.ok = k2.checked ? [...new Set([...c.ok, i])] : c.ok.filter((x) => x !== i); salvar(); if ($('#critN')) $('#critN').textContent = `${c.ok.length}/${tot}`; }; });
      if ($('#abrePlano')) $('#abrePlano').onclick = () => mostra('plano');
    } else if (k === 'plano') {
      montaPlano(A, c);
    } else if (k === 'gherkin') {
      montaGherkin(A, c, contagens);
    } else {
      A.innerHTML = `<div class="sec"><div id="coms">${c.comentarios.map((m) => `<div class="coment">${avatar('voce')}<div class="bx"><b>Você</b><small>${dataBR(m.quando)}</small><div>${esc(m.tx)}</div></div></div>`).join('') || '<div class="v nada" style="font-size:15px">Nenhum comentário ainda.</div>'}</div>
        <div style="display:flex;gap:10px;margin-top:12px"><input class="in" id="com" placeholder="Escreva um comentário…" data-test="comentario"><button class="btn" id="enviaCom" data-test="enviar-comentario">Comentar</button></div></div>`;
      $('#enviaCom').onclick = () => { const t = $('#com').value.trim(); if (!t) return; c.comentarios.push({ tx: t, quando: agora() }); salvar(); contagens(); mostra('comentarios'); };
    }
    contagens();
  };
  $$('.abas button').forEach((b) => { b.onclick = () => mostra(b.dataset.aba); });
  if ($('#mover')) $('#mover').onchange = () => { const p = podeMover(c, $('#mover').value); if (!p.ok) { $('#mover').value = c.coluna; return p.msg && toast(p.msg, true); } c.coluna = $('#mover').value; salvar(); toast(`${c.id} movido para ${nomeColuna(c.coluna).toLowerCase()}`); };
  mostra(aba);
};

function montaGherkin(A, card, contagens) {
  const arq = card.id === 'FD-101' ? 'criar-chamado.feature' : card.id.toLowerCase() + '.feature';
  A.innerHTML = `<div class="plano-barra"><p class="dica">Os cenários do plano, do jeito que o time inteiro entende: <b>Dado</b> o contexto, <b>Quando</b> a ação, <b>Então</b> o resultado.</p>
      <div class="gk-acoes"><button type="button" class="btn sec peq" id="gkModelo" data-test="inserir-cenario">+ Modelo de cenário</button><button type="button" class="btn sec peq" id="gkBaixa" data-test="baixar-feature">Baixar .feature</button></div></div>
    <div class="plano"><div class="esq">
      <div class="gk-ed"><div class="gk-tab">${arq}</div>
        <div class="gk-corpo"><pre class="gk-nums" id="gkNums" aria-hidden="true"></pre><div class="gk-area"><pre class="gk-cor" id="gkCor" aria-hidden="true"></pre>
          <textarea id="gk" data-test="editor-gherkin" spellcheck="false" autocomplete="off" autocapitalize="off" aria-label="Arquivo ${arq}"></textarea></div></div></div>
      <p class="dica" style="margin-top:10px">Dica: <b>Tab</b> faz o recuo. O FlowDesk salva enquanto você escreve.</p>
    </div>
    <aside><div class="cov" id="gkRev" data-test="revisao-gherkin"></div></aside></div>`;
  const ta = $('#gk'), cor = $('#gkCor'), nums = $('#gkNums');
  ta.value = gherkinDe(dados(), card.id);
  const atualiza = () => {
    const t = ta.value, d = dados(); d.gherkin = d.gherkin || {}; d.gherkin[card.id] = t; salvar();
    cor.innerHTML = pintaGherkin(t); nums.textContent = t.split('\n').map((_, i) => i + 1).join('\n');
    const r = revisaGherkin(t);
    const item = (ok, tx) => `<div class="rl ${ok ? 'on' : ''}"><b>✓</b>${tx}</div>`;
    const probs = (c) => [!c.dado && 'falta o Dado', !c.quando && 'falta o Quando', !c.entao && 'falta o Então', c.ordem && 'a ordem é Dado → Quando → Então',
      c.acoes > 1 && `${c.acoes} ações no Quando: um cenário testa uma ação só`, c.vago.length && `Então vago na linha ${c.vago[0]}: que erro? onde?`].filter(Boolean);
    $('#gkRev').innerHTML = `<div class="hd">Revisão do Gherkin<span class="cnt" data-test="gherkin-contagem">${r.cenarios.length}</span></div>`
      + item(r.funcionalidade, 'Começa pela Funcionalidade')
      + (r.cenarios.length ? r.cenarios.map((c) => { const p = probs(c); return `<div class="gk-cen ${p.length ? 'mal' : 'ok'}" data-test="gherkin-cenario"><div class="n"><b>${p.length ? '!' : '✓'}</b>${esc(c.nome)}</div>${p.map((x) => `<div class="p">${x}</div>`).join('')}</div>`; }).join('')
        : '<div class="gk-vazio">Nenhum cenário ainda. Comece com <b>Cenário:</b> e o nome dele.</div>')
      + (r.soltas.length ? `<div class="ex">Linha ${r.soltas[0]} sem palavra-chave do Gherkin (Dado, Quando, Então, E…)</div>` : '');
    contagens(); confereMissoes();
  };
  const sincroniza = () => { cor.scrollTop = ta.scrollTop; cor.scrollLeft = ta.scrollLeft; nums.scrollTop = ta.scrollTop; };
  ta.addEventListener('input', atualiza); ta.addEventListener('scroll', sincroniza);
  ta.addEventListener('keydown', (ev) => {
    if (ev.key !== 'Tab') return; ev.preventDefault();
    const a = ta.selectionStart; ta.setRangeText('  ', a, ta.selectionEnd, 'end'); atualiza();
  });
  $('#gkModelo').onclick = () => {
    const mod = '\n  Cenário: \n    Dado que \n    Quando \n    Então \n';
    const fim = ta.value.replace(/\s+$/, ''); ta.value = fim + '\n' + mod; ta.focus();
    const pos = ta.value.lastIndexOf('Cenário: ') + 9; ta.setSelectionRange(pos, pos); atualiza();
  };
  $('#gkBaixa').onclick = () => {
    const url = URL.createObjectURL(new Blob([ta.value], { type: 'text/plain;charset=utf-8' }));
    const l = document.createElement('a'); l.href = url; l.download = arq; document.body.appendChild(l); l.click(); l.remove(); setTimeout(() => URL.revokeObjectURL(url), 2000);
  };
  atualiza();
}

function montaPlano(A, card) {
  const d = dados(), id = card.id, lista = d.planos[id];
  const TIPOS = { P: ['POSITIVO', 'tP'], N: ['NEGATIVO', 'tN'], L: ['VALOR LIMITE', 'tL'] };
  A.innerHTML = `<div class="plano-barra"><p class="dica">Cada cenário: uma situação, os passos e o resultado esperado.</p></div>
    <div class="plano"><div class="esq">
      <div class="xres" id="xres" data-test="resumo-execucao"></div>
      <table class="tabela"><thead><tr><th style="width:40px">#</th><th>Cenário</th><th style="width:196px">Execução</th><th style="width:76px"></th></tr></thead><tbody id="linhas"></tbody></table>
      <button type="button" class="btn sec" id="abreForm" data-test="novo-cenario" style="margin-top:14px">+ Novo cenário</button>
      <form class="fcard" id="f" novalidate style="margin-top:14px;max-width:none"><h3 style="font-size:18px;margin-bottom:14px" id="fTit">Novo cenário</h3>
        <div style="display:flex;gap:14px;flex-wrap:wrap"><div class="campo" style="flex:2;min-width:240px"><label for="cNome">Cenário <i>*</i></label><input class="in" id="cNome" data-test="cenario-nome" placeholder="Ex.: Criar sem título"></div>
          <div class="campo" style="flex:1;min-width:170px"><label for="cTipo">Tipo</label><select class="in" id="cTipo" data-test="cenario-tipo"><option value="P">Positivo</option><option value="N">Negativo</option><option value="L">Valor limite</option></select></div></div>
        <div class="campo"><label for="cPassos">Passos</label><textarea class="in" id="cPassos" data-test="cenario-passos" placeholder="1. Abrir a tela Novo chamado&#10;2. …"></textarea></div>
        <div class="campo"><label for="cEsp">Resultado esperado <i>*</i></label><input class="in" id="cEsp" data-test="cenario-esperado" placeholder="Seja específico: o que aparece, onde, e o que acontece com o chamado"></div>
        <div class="campo"><label>Quais regras esse cenário cobre?</label><div class="regras-check">${REGRAS.map((r, i) => `<label class="cr"><input type="checkbox" value="${i}" data-test="cenario-regra">${r}</label>`).join('')}</div></div>
        <div class="fbtns"><button type="button" class="btn sec" id="cancela" hidden data-test="cancelar-edicao">Cancelar</button><button class="btn" data-test="salvar-cenario" id="salva">Adicionar cenário</button></div>
      </form></div>
      <aside><div class="cov" id="cov" data-test="cobertura"><div class="hd">Cobertura das regras<span class="cnt" id="cnt" data-test="cobertura-contagem">0/6</span></div><div class="bar"><i id="bar"></i></div>
        ${REGRAS.map((r, i) => `<div class="rl" id="u${i}" data-test="regra"><b>✓</b>${r}<span class="q" id="q${i}" hidden></span></div>`).join('')}<div class="ex" id="ex" hidden></div></div><div class="pop-wrap arq-box"><button type="button" class="btn sec peq" id="arqBtn" data-test="abrir-arquivos">Arquivos de teste</button><div class="arqs pop-arq" id="arqPop" hidden><h3>Arquivos de teste</h3><p class="dica">Gerados na hora, no tamanho exato, pra testar o anexo.</p>${[['documento-5MB-exato.pdf', LIMITE_ANEXO], ['documento-5,1MB.pdf', Math.floor(5.1 * 1048576)], ['documento-1MB.pdf', 1048576], ['print-da-tela.png', 48 * 1024], ['foto.jpg', 220 * 1024], ['programa.exe', 12 * 1024]].map(([n, b]) => `<a href="#" data-arq="${n}" data-b="${b}" data-test="arquivo-teste">${n}<small>${tamanho(b)}</small></a>`).join('')}</div></div></aside></div>`;
  let editando = null; const abertos = new Set();
  const mostraForm = (on) => { $('#f').hidden = !on; $('#abreForm').hidden = on; };
  mostraForm(lista.length === 0);
  $('#abreForm').onclick = () => { mostraForm(true); $('#cNome').focus(); };
  $('#arqBtn').onclick = (ev) => { ev.stopPropagation(); $('#arqPop').hidden = !$('#arqPop').hidden; };
  document.addEventListener('click', (ev) => { if ($('#arqPop') && !ev.target.closest('.pop-wrap')) $('#arqPop').hidden = true; });
  const pinta = () => {
    $('#linhas').innerHTML = lista.length ? lista.map((c, i) => {
      const fora = !c.regras.length, t = TIPOS[c.tipo];
      return `<tr class="${fora ? 'fora' : ''} st-${c.exec || 'nao'}" data-test="linha-cenario"><td class="num"><span>${i + 1}</span></td><td><div class="cn">${esc(c.nome)}</div><div class="tgs"><span class="tg ${t[1]}">${t[0]}</span>${fora ? `<span class="tg tX">FORA DAS REGRAS</span>` : ''}</div>${c.passos ? `<button type="button" class="link" data-ps="${i}" data-test="ver-passos">${abertos.has(i) ? 'Esconder passos' : 'Ver passos'}</button><div class="passos" ${abertos.has(i) ? '' : 'hidden'}>${esc(c.passos)}</div>` : ''}<div class="res"><small>Resultado esperado</small>${esc(c.esperado)}</div></td>
        <td><div class="xcel"><div class="xseg"><button type="button" class="sg ok ${c.exec === 'passou' ? 'on' : ''}" data-x="${i}" data-v="passou" data-test="marcar-passou">✓ Passou</button><button type="button" class="sg nok ${c.exec === 'falhou' ? 'on' : ''}" data-x="${i}" data-v="falhou" data-test="marcar-falhou">✕ Falhou</button></div><select class="exec-sel" data-i="${i}" data-test="execucao" aria-label="Execução do cenário ${i + 1}"><option value="nao" ${c.exec === 'passou' || c.exec === 'falhou' ? '' : 'selected'}>Não executado</option><option value="passou" ${c.exec === 'passou' ? 'selected' : ''}>Passou</option><option value="falhou" ${c.exec === 'falhou' ? 'selected' : ''}>Falhou</option></select><div class="xlinks">${c.exec === 'falhou' ? (c.bug ? `<a class="bugchip" href="card.html?id=${c.bug}" data-test="bug-ligado">🐞 ${c.bug}</a>` : `<button type="button" class="xl bug" data-bug="${i}" data-test="reportar-bug">🐞 Reportar bug</button>`) : ''}${c.exec && c.exec !== 'nao' ? `<label class="xl ev ${c.evid ? 'tem' : ''}" title="Print ou vídeo da execução"><input type="file" data-ev="${i}" data-test="evidencia-cenario" accept="image/*,video/*,.pdf" hidden>📎 ${c.evid ? esc(c.evid) : 'Anexar evidência'}</label>` : ''}</div></div></td>
        <td><div class="acoes"><button class="icone" data-ed="${i}" data-test="editar-cenario" title="Editar cenário"><svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg></button><button class="icone rm" data-rm="${i}" data-test="excluir-cenario" title="Excluir cenário"><svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M8 6V4h8v2"/><path d="M19 6l-1 14H6L5 6"/></svg></button></div></td></tr>`;
    }).join('') : '<tr><td colspan="4" class="vazio" data-test="plano-vazio">Nenhum cenário ainda</td></tr>';
    let n = 0;
    REGRAS.forEach((r, i) => { const quem = lista.map((c, j) => c.regras.includes(i) ? j + 1 : 0).filter(Boolean); const on = quem.length > 0; if (on) n++; $('#u' + i).classList.toggle('on', on); $('#q' + i).hidden = !on; $('#q' + i).textContent = quem.length === 1 ? 'CENÁRIO ' + quem[0] : quem.join(' · '); });
    setTimeout(confereMissoes, 400);
    $('#cnt').textContent = n + '/6'; $('#bar').style.width = (n / 6 * 100) + '%'; $('#cov').classList.toggle('done', n === 6);
    const fora = lista.map((c, j) => c.regras.length ? 0 : j + 1).filter(Boolean);
    $('#ex').hidden = !fora.length; $('#ex').textContent = `+ Cenário ${fora.join(', ')}: fora das regras`;
    const ok = lista.filter((c) => c.exec === 'passou').length, nok = lista.filter((c) => c.exec === 'falhou').length, tot = lista.length;
    $('#xres').hidden = !tot;
    $('#xres').innerHTML = `<div class="xtop"><span class="xt">Execução</span><span class="xn"><b>${ok + nok}</b> de ${tot} executados</span></div><div class="xb"><i style="width:${tot ? ok / tot * 100 : 0}%"></i><i class="f" style="width:${tot ? nok / tot * 100 : 0}%"></i></div><div class="xleg"><span class="xp"><i></i>${ok} passou</span><span class="xf"><i></i>${nok} falhou</span><span class="xz"><i></i>${tot - ok - nok} a executar</span></div>`;
    if ($('#n-plano')) $('#n-plano').textContent = lista.length || '';
    $$('[data-test=execucao]').forEach((s) => { s.onchange = () => { lista[+s.dataset.i].exec = s.value; salvar(); pinta(); }; });
    $$('[data-x]').forEach((b) => { b.onclick = () => { const c = lista[+b.dataset.x]; c.exec = c.exec === b.dataset.v ? 'nao' : b.dataset.v; salvar(); pinta(); }; });
    $$('[data-ev]').forEach((f) => { f.onchange = () => { const x = f.files[0]; if (!x) return; lista[+f.dataset.ev].evid = x.name; salvar(); pinta(); toast('Evidência anexada ao cenário ' + (+f.dataset.ev + 1)); }; });
    $$('[data-bug]').forEach((b) => { b.onclick = () => { const i = +b.dataset.bug; novaTarefa(() => pinta(), { card: card.id, i, n: i + 1, nome: lista[i].nome }); }; });
    $$('[data-ed]').forEach((b) => { b.onclick = () => edita(+b.dataset.ed); });
    $$('[data-ps]').forEach((b) => { b.onclick = () => { const i = +b.dataset.ps; abertos.has(i) ? abertos.delete(i) : abertos.add(i); pinta(); }; });
    $$('[data-rm]').forEach((b) => { b.onclick = () => { lista.splice(+b.dataset.rm, 1); salvar(); pinta(); toast('Cenário excluído'); }; });
  };
  const limpa = () => { editando = null; $('#f').reset(); $('#fTit').textContent = 'Novo cenário'; $('#salva').textContent = 'Adicionar cenário'; $('#cancela').hidden = !lista.length; limpaErros(); };
  const edita = (i) => {
    const c = lista[i]; editando = i; limpaErros();
    $('#cNome').value = c.nome; $('#cTipo').value = c.tipo; $('#cPassos').value = c.passos; $('#cEsp').value = c.esperado;
    $$('[data-test=cenario-regra]').forEach((k) => { k.checked = c.regras.includes(+k.value); });
    mostraForm(true); $('#fTit').textContent = `Editando o cenário ${i + 1}`; $('#salva').textContent = 'Salvar cenário'; $('#cancela').hidden = false; $('#f').scrollIntoView({ behavior: 'smooth' });
  };
  $('#cancela').onclick = () => { limpa(); if (lista.length) mostraForm(false); };
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
  $('#cancela').hidden = !lista.length;
  $$('[data-arq]').forEach((a) => {
    a.onclick = (ev) => {
      ev.preventDefault();
      const n = a.dataset.arq, b = +a.dataset.b, bytes = new Uint8Array(b), cab = { pdf: '%PDF-1.4\n', png: '\x89PNG\r\n\x1a\n', jpg: '\xff\xd8\xff\xe0', exe: 'MZ' }[extensao(n)] || '';
      for (let i = 0; i < cab.length; i++) bytes[i] = cab.charCodeAt(i) & 255;
      const url = URL.createObjectURL(new Blob([bytes])); const l = document.createElement('a'); l.href = url; l.download = n; document.body.appendChild(l); l.click(); l.remove(); setTimeout(() => URL.revokeObjectURL(url), 2000);
    };
  });
  pinta();
}

// endereços antigos continuam funcionando
PAGINAS.plano = () => location.replace(`card.html?id=${(qs.get('card') || 'FD-101').toUpperCase()}&aba=plano`);
PAGINAS['reportar-bug'] = () => location.replace('quadro.html?novo=bug');


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

// respostas do time no FlowChat (roteiro simples por palavra-chave, pra o chat não parecer vazio)
function respostaDoTime(tx, canal) {
  const t = tx.toLowerCase(), d = dados(), bug = d.cards.filter((c) => c.tipo === 'bug').pop();
  const R = (de, ...op) => ({ de, tx: op[Math.floor(Math.random() * op.length)] });
  if (/bug|erro|falh|quebr/.test(t)) return bug ? R('gabriela', `Vi o ${bug.id}. Vou olhar ainda hoje e te aviso 👀`, `Já tô olhando o ${bug.id}. Se tiver print, joga no card!`) : R('gabriela', 'Opa! Abre o card em "Reportar bug" com o passo a passo que eu olho 👀', 'Me manda os passos pra reproduzir? Aí eu consigo ver aqui.');
  if (/regra|crit[eé]rio|card|fd-?10\d|limite|anexo|t[ií]tulo/.test(t)) return R('rafael', 'Tá tudo nos critérios do FD-101. Se faltar alguma regra, me chama que a gente conversa 👍', 'Boa! Se tiver dúvida de regra, pode perguntar. Eu prefiro responder agora do que descobrir depois.');
  if (/release|prazo|sexta|entrega|review/.test(t)) return R('beatriz', 'A release é sexta, depois da review. Se algo for segurar, me avisa antes 🙏', 'Anotado. Prioridade continua sendo o FD-101.');
  if (/daily|reuni[aã]o|retro|sprint/.test(t)) return R('lucas', 'Daily é às 9h15, todo dia. Curta e direto ao ponto.', 'Na daily, fala o que fez, o que vai fazer e se tem algo travando.');
  if (/^(oi|ol[aá]|bom dia|boa tarde|boa noite|e a[ií])/.test(t)) return R('gabriela', 'Oi! 👋', 'E aí! Tudo certo por aí?');
  if (/obrigad|valeu|vlw/.test(t)) return R('rafael', 'Imagina! 🙌', 'Tamo junto!');
  if (/\?/.test(t)) return R('vinicius', 'Boa pergunta. Se for regra, o Rafael responde. Se for código, a Gabriela. Se não souber pra quem, pergunta aqui mesmo 😉');
  const pad = { 'time-produto': 'vinicius', bugs: 'gabriela', releases: 'beatriz', geral: 'beatriz' }[canal] || 'vinicius';
  return R(pad, 'Chegou aqui 👍', 'Anotado!', 'Valeu por avisar.');
}
PAGINAS.chat = () => {
  const d = dados(), canal = d.chat[qs.get('canal')] ? qs.get('canal') : 'time-produto', l = d.chat[canal];
  const msgHtml = (m) => `<div class="msg" data-test="mensagem">${m.de === 'voce' ? '<span class="vc">VC</span>' : `<img src="img/av_${m.de}.png" alt="">`}<div><div class="who">${PESSOAS[m.de].nome}<i>${PESSOAS[m.de].papel}</i><small>${hora(m.quando)}</small></div><div class="tx">${esc(m.tx)}</div></div></div>`;
  document.body.innerHTML = `<div class="chat"><div class="chan"><span class="marca" style="font-size:18px"><img src="img/icon.png" alt="" style="height:28px">FlowChat</span>
      <div class="t">Canais</div>${Object.keys(d.chat).map((k) => `<a href="chat.html?canal=${k}" class="${k === canal ? 'on' : ''}" data-test="canal-${k}"># ${k}</a>`).join('')}
      <a href="dashboard.html" style="margin-top:auto;color:var(--mut);font-size:14px" data-test="voltar-flowdesk">← Voltar pro FlowDesk</a></div>
    <div class="msgs"><div class="chead"># ${canal}<span>6 membros</span></div><div class="lista" id="lista" data-test="mensagens">${l.map(msgHtml).join('')}</div>
      <div class="digitando" id="dig" data-test="digitando" hidden></div>
      <form class="composer" id="f"><input class="in" id="tx" placeholder="Escreva uma mensagem…" data-test="mensagem-texto" autocomplete="off"><button class="btn" data-test="enviar-mensagem">Enviar</button></form></div></div>`;
  const desce = () => { $('#lista').scrollTop = 1e9; };
  desce();
  $('#f').onsubmit = (ev) => {
    ev.preventDefault(); const t = $('#tx').value.trim(); if (!t) return;
    const m = { de: 'voce', tx: t, quando: agora() }; l.push(m); salvar(); $('#lista').insertAdjacentHTML('beforeend', msgHtml(m)); $('#tx').value = ''; desce();
    const r = respostaDoTime(t, canal);
    setTimeout(() => { $('#dig').hidden = false; $('#dig').textContent = `${PESSOAS[r.de].nome} está digitando…`; }, 700);
    setTimeout(() => { $('#dig').hidden = true; const rm = { ...r, quando: agora() }; l.push(rm); salvar(); $('#lista').insertAdjacentHTML('beforeend', msgHtml(rm)); desce(); }, 2400);
  };
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
