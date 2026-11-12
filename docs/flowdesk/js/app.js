// FlowDesk: site de treino do curso Vida de QA.
// Cada aluno cria a própria conta. Tudo fica salvo só no navegador dele (localStorage).
// A sprint muda sozinha: começa na 14 (com os bugs da sprint) e vira 15 quando o aluno termina a missão do EP08.
// ?versao=14, 15 ou 16 na URL força uma versão só naquela visita (pra testar).
'use strict';

// ---------- armazenamento ----------
const LS = {
  get(k, d) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* navegador sem armazenamento */ } },
  del(k) { try { localStorage.removeItem(k); } catch (e) { } },
};
const qs = new URLSearchParams(location.search);
const LIMITE_ANEXO = 5 * 1024 * 1024;
const FORMATOS = ['pdf', 'png', 'jpg', 'jpeg'];

const contas = () => LS.get('fd:contas', {});
const sessao = () => LS.get('fd:sessao', null);
const chaveDados = () => 'fd:dados:' + sessao();
let D = null;
// versões novas do site completam o que faltar nos dados antigos, sem apagar nada do aluno
const migra = (d) => { if (!d) return d; const base = semente(); for (const k of Object.keys(base)) if (d[k] === undefined) d[k] = base[k]; for (const k of Object.keys(base.chat || {})) if (d.chat && !d.chat[k]) d.chat[k] = base.chat[k]; return d; };
const dados = () => { if (!D) { D = migra(LS.get(chaveDados(), null)); if (D) andaSprint(D); } return D; };
const salvar = () => LS.set(chaveDados(), D);
// sem ninguém logado (tela de login), a versão é a mais nova que este navegador já viu
const _conq = (LS.get(chaveDados(), null) || {}).conquistas || Object.keys(localStorage).filter((k) => k.startsWith('fd:dados:')).flatMap((k) => (LS.get(k, null) || {}).conquistas || []);
const VERSAO = qs.get('versao') ? Math.min(17, Math.max(14, +qs.get('versao') || 14)) : (_conq.includes('ep14') ? 17 : _conq.includes('ep12') ? 16 : _conq.includes('ep08') ? 15 : 14);
// bugs plantados por versão
const BUG = {
  tituloSoEspacos: VERSAO < 15,  // aceita título só com espaços (não usa trim)
  anexo5mbExato: VERSAO < 15,    // recusa o arquivo de exatamente 5 MB (usa >= em vez de >)
  titulo100: VERSAO === 15,      // regressão da correção: com o trim, o limite virou < 100 em vez de <= 100
  duplicado: VERSAO === 17,      // o botão só trava depois que o servidor responde: com rede lenta, dois cliques criam dois chamados
  buscaAcento: VERSAO === 17,    // o servidor tira o acento dos títulos, mas não o da busca
  buscaEmoji: VERSAO === 17,     // a tela corta a busca em 30 posições e pode partir um emoji no meio (URIError)
  rascunho: VERSAO === 17,       // o rascunho do novo chamado fica numa chave só do navegador e não sai no logout
};
// caça aos bugs: endereço do Worker (vazio = temporada ainda não aberta)
const CACA_API = '';
// ajuste fino por contexto (compatibilidade entre telas)
const _K = [[2521, 2396, 2958], [3223, 3349, 3525], [2641, 3778, 1525]];
const _hk = (k) => { let h = 7; for (const ch of k) h = (h * 33 + ch.charCodeAt(0)) >>> 0; return h % 4093; };
const _h = (s) => { let h = 2166136261; for (const ch of s) { h ^= ch.charCodeAt(0); h = Math.imul(h, 16777619) >>> 0; } return h.toString(36); };
const _sl = () => ['fl', '0w', 'd3', 'sk'].join('') + String.fromCharCode(81) + 6 * 7;
// registra, sem avisar, que o comportamento aconteceu de verdade neste navegador
function _pv(k) {
  const pc = CACA_API && LS.get('fd:placar', null); if (!pc || pc.encerrada || !_c(k)) return;
  const T = pc.temporada || 1, n = _K[T - 1].indexOf(_hk(k)) + 1, p = LS.get('fd:caca-prova', {}), id = T + '-' + n;
  if (n < 1 || p[id]) return; const q = Date.now(); p[id] = { t: T, n, q, tk: _h(`${T}|${n}|${q}|${_sl()}`) }; LS.set('fd:caca-prova', p);
}
const _c = (k) => { const pc = CACA_API && LS.get('fd:placar', null); if (!pc || pc.encerrada) return 0; let h = 7; for (const ch of k) h = (h * 33 + ch.charCodeAt(0)) >>> 0; return (_K[(pc.temporada || 1) - 1] || []).includes(h % 4093) ? 1 : 0; };

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
const TIME = [
  ['rafael', 'Escreve as histórias e os critérios. Dúvida de regra é com ele.'],
  ['gabriela', 'Desenvolve o FD-101. Achou bug? Ela quer saber primeiro.'],
  ['lucas', 'Cuida da arquitetura e puxa a daily às 9h15.'],
  ['beatriz', 'Decide prioridade e data de release.'],
  ['vinicius', 'QA sênior, seu mentor. Pode perguntar qualquer coisa.'],
];
const COLUNAS = [['afazer', 'A fazer'], ['dev', 'Desenvolvimento'], ['qa', 'Pronto pra QA'], ['teste', 'Em teste'], ['concluido', 'Concluído']];
const STATUS = ['Aberto', 'Em andamento', 'Resolvido', 'Fechado'];
const REGRAS = ['Título obrigatório', 'Descrição obrigatória', 'Título até 100 caracteres', 'Anexo opcional: PDF, PNG ou JPG até 5 MB', 'Mensagem de sucesso e tela do chamado', 'Status inicial: Aberto'];
const REGRA_ESPACOS = 'Título só com espaços conta como vazio';
if (VERSAO >= 16) REGRAS.push(REGRA_ESPACOS);  // o Rafael respondeu a dúvida do cenário 9: virou regra na Sprint 16
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


// ---------- sprints novas: a Gabriela entrega as correções e os bugs andam sozinhos ----------
function andaSprint(d, v = VERSAO, grava = true) {
  d.sprints = d.sprints || {}; let mudou = false;
  const com = (c, tx) => c.comentarios.push({ de: 'gabriela', tx, quando: agora() });
  if (v >= 15 && !d.sprints[15]) {
    d.sprints[15] = agora(); mudou = true;
    bugsDe(d).filter((b) => b.coluna !== 'concluido').forEach((b) => { b.coluna = 'qa'; b.corrigidoEm = 15; const t = textoBug(b);
      com(b, /espa[çc]o/i.test(t) ? 'Corrigi os dois. O título agora ignora espaços, e o limite do anexo aceita 5 MB certinho. Pode testar.' : /anexo|mb|arquivo/i.test(t) ? 'Corrigi na Sprint 15: o limite do anexo agora aceita 5 MB certinho. Pode testar.' : 'Corrigi na Sprint 15. Pode testar.'); });
    d.chat.releases.push({ de: 'lucas', tx: 'Release da Sprint 15 publicada em homologação: correções dos bugs do FD-101.', quando: agora() });
    d.chat.bugs.push({ de: 'gabriela', tx: 'Corrigi os bugs que você abriu. Estão em Pronto pra QA. Pode testar 🙏', quando: agora() });
  }
  if (v >= 16 && !d.sprints[16]) {
    d.sprints[16] = agora(); mudou = true;
    bugsDe(d).filter((b) => b.coluna !== 'concluido' && (!b.corrigidoEm || b.reaberto)).forEach((b) => { b.coluna = 'qa'; b.corrigidoEm = 16; b.reaberto = false;
      com(b, b.regressao || /100|cem|caracter/i.test(textoBug(b)) ? 'Corrigido na Sprint 16: voltei o limite pra 100. Era um < no lugar do <=. Pode testar.' : 'Corrigido na Sprint 16. Pode testar.'); });
    const f = d.cards.find((c) => c.id === 'FD-101'); if (f && !f.criterios.includes(REGRA_ESPACOS)) f.criterios.push(REGRA_ESPACOS);
    d.chat.releases.push({ de: 'lucas', tx: 'Release da Sprint 16 publicada em homologação: correção da regressão do título.', quando: agora() });
    d.chat.bugs.push({ de: 'gabriela', tx: 'Vi a regressão. Foi mal, troquei o <= por < quando coloquei o trim. Já subi a correção na Sprint 16.', quando: agora() });
    d.chat['time-produto'].push({ de: 'rafael', tx: 'Decidido: título só com espaços conta como vazio. Virou a regra 7 do FD-101.', quando: agora() });
  }
  if (v >= 17 && !d.sprints[17]) {
    d.sprints[17] = agora(); mudou = true;
    const novo = (titulo, descricao, cliente, por, status) => { const id = d.proximoChamado++; d.chamados.push({ id, titulo, descricao, cliente, status: status || 'Aberto', criadoEm: agora(), criadoPor: por, anexo: null, historico: [{ quando: agora(), tx: 'Chamado criado com status Aberto' }] }); };
    novo('Manutenção do forno da padaria', 'O forno principal precisa de manutenção antes do fim de semana.', 'Padaria Pão Quente', 'Rafael');
    novo('Caixa dos fundos travou hoje 🔥 urgente', 'O caixa dos fundos travou duas vezes durante a manhã.', 'Padaria Pão Quente', 'Sandra');
    d.chat.suporte = d.chat.suporte || [];
    d.chat.suporte.push({ de: 'beatriz', tx: 'Encaminhando da Sandra, da Padaria Pão Quente: “Às vezes, quando eu abro um chamado, ele aparece duas vezes na lista. Não é sempre. Hoje foi duas vezes.”', quando: agora() });
    d.chat.releases.push({ de: 'lucas', tx: 'Release da Sprint 17 publicada em homologação: a busca e a criação de chamados agora passam pela API, e o novo chamado guarda rascunho.', quando: agora() });
    // Sprint 17: depois de criar, a tela fica no formulário (pedido do suporte, que abre vários chamados seguidos)
    const fd = d.cards.find((c) => c.id === 'FD-101'); if (fd && fd.criterios[4]) fd.criterios[4] = 'Depois de criar: mensagem de sucesso com o número do chamado, e o formulário limpo pro próximo';
    d.chat['time-produto'].push({ de: 'rafael', tx: 'Mudança da Sprint 17, a pedido do suporte: depois de criar, a tela fica no formulário com a mensagem e o número do chamado. Quem abre vários seguidos não precisa voltar toda hora.', quando: agora() });
  }
  if (mudou && grava) LS.set(chaveDados(), d);
  return d;
}
// ---------- servidor (Sprint 17 em diante): o service worker faz o papel da API ----------
const usaApi = () => VERSAO >= 17 && 'serviceWorker' in navigator && /^https?:/.test(location.protocol);
let _swPronto = null;
function swPronto() {
  if (!_swPronto) _swPronto = (async () => {
    await navigator.serviceWorker.register('sw.js?v=1794479423');
    if (navigator.serviceWorker.controller) return true;
    await new Promise((r) => { navigator.serviceWorker.addEventListener('controllerchange', r, { once: true }); setTimeout(r, 4000); });
    return !!navigator.serviceWorker.controller;
  })().catch(() => false);
  return _swPronto;
}
if ('serviceWorker' in navigator) navigator.serviceWorker.addEventListener('message', (ev) => {
  const m = ev.data || {}, porta = ev.ports && ev.ports[0]; if (!porta || !sessao()) return;
  if (m.tipo === 'lista') porta.postMessage({ lista: dados().chamados.map(({ id, titulo, cliente, status, criadoEm }) => ({ id, titulo, cliente, status, criadoEm })), bugAcento: BUG.buscaAcento });
  if (m.tipo === 'cria') {
    const d = dados(), c = m.chamado, id = d.proximoChamado++;
    const x = { id, titulo: String(c.titulo).trim(), descricao: String(c.descricao).trim(), cliente: c.cliente, status: 'Aberto', criadoEm: agora(), criadoPor: 'Você', anexo: c.anexo || null, v: VERSAO, historico: [{ quando: agora(), tx: 'Chamado criado com status Aberto' }] };
    d.chamados.push(x); salvar(); porta.postMessage({ id, titulo: x.titulo, cliente: x.cliente, status: x.status, criadoEm: x.criadoEm });
  }
});
if (usaApi()) swPronto();
const RASCUNHO = 'fd:rascunho';
// quem viu rascunho de outra conta (vale pra missão do EP20, em qualquer conta deste navegador)
// o bug do rascunho pode ser reportado logado em qualquer conta (a sua ou a do Lucas): conta pra missão do mesmo jeito
const bugsGlobais = (d) => [...bugsDe(d), ...Object.keys(contas()).flatMap((e) => ((LS.get('fd:dados:' + e, null) || {}).cards || []).filter((c) => c.tipo === 'bug'))];
const vazouRascunho = () => Object.keys(contas()).some((e) => (LS.get('fd:dados:' + e, null) || {}).viuRascunhoAlheio);
const rodadaDe = (d, id = 'FD-101') => (d.rodadas || {})[id] || null;
// grupos de cenário, pelo que cada um cobre (pra conferir a análise de impacto)
const cenTitulo = (c) => c.regras.some((r) => r === 0 || r === 2 || r === 6);
const cenAnexo = (c) => c.regras.includes(3);
const cenFeliz = (c) => c.tipo === 'P' && c.regras.some((r) => r === 4 || r === 5);
const cenSoDescricao = (c) => c.regras.length === 1 && c.regras[0] === 1;

// ---------- saves por episódio (pontos de continuação do curso) ----------
// Cada save deixa o FlowDesk do jeito que o curso espera naquele ponto. Novos episódios: acrescentar aqui.
const CENARIOS_EP03 = [
  ['Caminho feliz: tudo válido', 'P', '1. Abrir a tela Novo chamado\n2. Preencher título e descrição\n3. Clicar em Criar chamado', 'Mensagem de sucesso, abre a tela do chamado, status Aberto', [4, 5]],
  ['Criar sem título', 'N', '1. Abrir a tela Novo chamado\n2. Deixar o título vazio\n3. Preencher a descrição\n4. Clicar em Criar chamado', 'Aparece "Título é obrigatório" e o chamado não é criado', [0]],
  ['Criar sem descrição', 'N', '1. Abrir a tela Novo chamado\n2. Preencher o título\n3. Deixar a descrição vazia\n4. Clicar em Criar chamado', 'Aparece "Descrição é obrigatória" e o chamado não é criado', [1]],
  ['Título com 100 caracteres', 'L', '1. Abrir a tela Novo chamado\n2. Colar um título com 100 caracteres\n3. Preencher a descrição\n4. Clicar em Criar chamado', 'Aceita e cria o chamado', [2]],
  ['Tentar digitar o 101º caractere', 'L', '1. Abrir a tela Novo chamado\n2. Colar um título com 100 caracteres\n3. Tentar digitar mais uma letra', 'O campo para em 100 caracteres', [2]],
  ['Anexo PDF de exatamente 5 MB', 'L', '1. Abrir a tela Novo chamado\n2. Preencher título e descrição\n3. Anexar documento-5MB-exato.pdf\n4. Clicar em Criar chamado', 'Aceita o anexo e cria o chamado', [3]],
  ['Anexo de 5,1 MB', 'L', '1. Abrir a tela Novo chamado\n2. Preencher título e descrição\n3. Anexar documento-5,1MB.pdf', 'Recusa o arquivo e avisa o limite de 5 MB', [3]],
  ['Anexo em formato .exe', 'N', '1. Abrir a tela Novo chamado\n2. Preencher título e descrição\n3. Anexar programa.exe', 'Recusa o arquivo: formato não aceito', [3]],
  ['Título só com espaços em branco', 'N', '1. Abrir a tela Novo chamado\n2. Digitar só espaços no título\n3. Preencher a descrição\n4. Clicar em Criar chamado', 'Nenhuma regra diz o que acontece', []],
].map(([nome, tipo, passos, esperado, regras]) => ({ nome, tipo, passos, esperado, regras, exec: 'nao' }));
const evNome = (i) => `cenario-${String(i + 1).padStart(2, '0')}.png`;
function depoisDoEp08() {
  const d = semente();
  d.planos['FD-101'] = CENARIOS_EP03.map((c, i) => ({ ...c, exec: i === 5 || i === 8 ? 'falhou' : 'passou', evid: evNome(i), ...(i === 5 || i === 8 ? { jaFalhou: true } : {}) }));
  d.planos['FD-101'][8].bug = 'BUG-01'; d.planos['FD-101'][5].bug = 'BUG-02';
  d.gherkin = { 'FD-101': GK_EP06 };
  const b = (id, titulo, cenario, passos, esperado, obtido, evidencia) => ({ id, titulo, coluna: 'afazer', resp: 'gabriela', tipo: 'bug', prioridade: 'Normal', relacionado: 'FD-101', cenario, passos, esperado, obtido, evidencia, criterios: [], ok: [], comentarios: [], criadoEm: agora() });
  d.cards.push(b('BUG-01', 'Criar chamado aceita título só com espaços', 'Título só com espaços em branco', '1. Abrir Novo chamado\n2. Digitar só espaços no título\n3. Preencher a descrição\n4. Clicar em Criar chamado', 'Aparece "Título é obrigatório" e o chamado não é criado', 'O chamado é criado sem título', evNome(8)));
  d.cards.push(b('BUG-02', 'Anexo de exatamente 5 MB é recusado', 'Anexo PDF de exatamente 5 MB', '1. Abrir Novo chamado\n2. Anexar documento-5MB-exato.pdf', 'Aceita o anexo e cria o chamado', 'Aparece "O arquivo passa do limite de 5 MB"', evNome(5)));
  d.proximoBug = 3; d.conquistas = ['ep03', 'ep06', 'ep08'];
  return d;
}
function depoisDoEp10() {
  const d = andaSprint(depoisDoEp08(), 15, false);
  bugsDe(d).forEach((b) => { b.coluna = 'concluido'; b.retestes = [{ quando: agora(), versao: 15, res: 'passou', evid: `reteste-${b.id.toLowerCase()}.png`, com: '' }]; });
  d.conquistas.push('ep10');
  return d;
}
function depoisDoEp12() {
  const d = depoisDoEp10(), l = d.planos['FD-101'], sel = [0, 1, 3, 4, 5, 6, 7];
  l.forEach((c, i) => { if (!sel.includes(i)) return; c.hist = [{ r: 1, v: 14, exec: c.exec, evid: c.evid, ...(c.bug ? { bug: c.bug } : {}) }]; delete c.bug; c.exec = i === 3 ? 'falhou' : 'passou'; c.evid = `rodada2-${evNome(i)}`; if (i === 3) { c.jaFalhou = true; c.bug = 'BUG-03'; } });
  d.rodadas = { 'FD-101': { n: 2, versao: 15, data: agora(), sel } };
  d.cards.push({ id: 'BUG-03', titulo: 'Título com exatamente 100 caracteres é recusado', coluna: 'afazer', resp: 'gabriela', tipo: 'bug', prioridade: 'Alta', relacionado: 'FD-101', cenario: 'Título com 100 caracteres', passos: '1. Abrir Novo chamado\n2. Colar um título com 100 caracteres\n3. Preencher a descrição\n4. Clicar em Criar chamado', esperado: 'Aceita e cria o chamado', obtido: 'Aparece "Título deve ter até 100 caracteres". Com 99 caracteres, cria normal', evidencia: 'rodada2-cenario-04.png', regressao: true, funcionava: 14, quebrou: 15, criterios: [], ok: [], comentarios: [], criadoEm: agora() });
  d.proximoBug = 4;
  d.chat['time-produto'].push({ de: 'voce', tx: 'Beatriz, a Sprint 15 corrigiu os dois bugs, mas quebrou o título de 100 caracteres. Abri o BUG-03. Não recomendo subir sem essa correção.', quando: agora() }, { de: 'beatriz', tx: 'Segura a release então. Gabi, prioridade no BUG-03.', quando: agora() });
  d.conquistas.push('ep12');
  return d;
}
function depoisDoEp12b() { return depoisDoEp12(); }
function depoisDoEp14() {
  const d = andaSprint(depoisDoEp12(), 16, false), l = d.planos['FD-101'], sel = [0, 1, 3, 4, 8];
  bugsDe(d).forEach((b) => { if (b.coluna !== 'concluido') { b.coluna = 'concluido'; b.retestes = [...(b.retestes || []), { quando: agora(), versao: 16, res: 'passou', evid: `reteste-${b.id.toLowerCase()}.png`, com: '' }]; } });
  l.forEach((c, i) => { if (!sel.includes(i)) return; c.hist = [...(c.hist || []), { r: 2, v: 15, exec: c.exec, evid: c.evid }]; c.exec = 'passou'; c.evid = `rodada3-${evNome(i)}`; delete c.bug; });
  l[8].regras = [6]; l[8].esperado = 'Aparece "Título é obrigatório" e o chamado não é criado';
  d.rodadas = { 'FD-101': { n: 3, versao: 16, data: agora(), sel } };
  d.gherkin['FD-101'] = (d.gherkin['FD-101'] || GK_EP06) + '\n  Cenário: Criar chamado com título só com espaços\n    Dado que estou na tela "Novo chamado"\n    E preenchi o título só com espaços\n    E preenchi a descrição\n    Quando clico em "Criar chamado"\n    Então vejo "Título é obrigatório"\n    E o chamado não é criado\n';
  d.conquistas.push('ep14'); return d;
}
const bugM3 = (d, id, titulo, passos, esperado, obtido, evidencia, extra) => d.cards.push({ id, titulo, coluna: 'afazer', resp: 'gabriela', tipo: 'bug', prioridade: 'Normal', relacionado: '', cenario: '', passos, esperado, obtido, evidencia, criterios: [], ok: [], comentarios: [], criadoEm: agora(), ...(extra || {}) });
function depoisDoEp16() {
  const d = andaSprint(depoisDoEp14(), 17, false); d.conquistas.push('d1');
  bugM3(d, 'BUG-04', 'Chamado criado em dobro com rede lenta e clique duplo', '1. Na aba Rede, limitar para 3G\n2. Abrir Novo chamado e preencher\n3. Clicar duas vezes em Criar chamado', 'Um chamado só', 'Dois chamados iguais. 8 em 10 tentativas', 'rede-dois-post.png', { prioridade: 'Alta' });
  d.proximoBug = 5; d.conquistas.push('ep16'); return d;
}
function depoisDoEp18() {
  const d = depoisDoEp16();
  bugM3(d, 'BUG-05', 'Busca com acento não encontra o chamado', '1. Abrir Chamados\n2. Buscar por manutenção', 'Aparece o chamado Manutenção do forno da padaria', 'Nenhum chamado encontrado', 'rede-busca-acento.png', { tecnico: 'GET api/chamados?busca=manuten%C3%A7%C3%A3o respondeu 200 com [] (sem acento acha)' });
  bugM3(d, 'BUG-06', 'Busca com título que tem emoji fica carregando pra sempre', '1. Abrir Chamados\n2. Colar na busca: Caixa dos fundos travou hoje 🔥 urgente', 'Aparece o chamado', 'Fica em Carregando… e nenhum pedido sai', 'console-urierror.png', { tecnico: 'URIError: URI malformed' });
  d.proximoBug = 7; d.conquistas.push('ep18'); return d;
}
function contaDoLucas(d) {
  const cs = contas(); cs['lucas@flowdesk.com'] = { nome: 'Lucas Ribeiro', senha: '123456', criadaEm: agora() }; LS.set('fd:contas', cs);
  const l = JSON.parse(JSON.stringify(d)); delete l.meuRascunho; delete l.viuRascunhoAlheio; LS.set('fd:dados:lucas@flowdesk.com', l); return d;
}
const SAVES = [
  { id: 'inicio', nome: 'Começo do curso', quando: 'do EP00 ao EP04', monta: () => semente() },
  { id: 'ep04', nome: 'Início do EP05', quando: 'Cenários em Gherkin', monta: () => { const d = semente(); d.planos['FD-101'] = CENARIOS_EP03.map((c) => ({ ...c })); d.conquistas = ['ep03']; return d; } },
  { id: 'ep06', nome: 'Início do EP06', quando: 'Prática do Gherkin', monta: () => { const d = semente(); d.planos['FD-101'] = CENARIOS_EP03.map((c) => ({ ...c })); d.conquistas = ['ep03']; return d; } },
  { id: 'ep07', nome: 'Início do EP07', quando: 'Primeiro bug', monta: () => { const d = semente(); d.planos['FD-101'] = CENARIOS_EP03.map((c) => ({ ...c })); d.gherkin = { 'FD-101': GK_EP06 }; d.conquistas = ['ep03', 'ep06']; return d; } },
  { id: 'ep08', nome: 'Início do EP08', quando: 'Executar o plano', monta: () => { const d = semente(); d.planos['FD-101'] = CENARIOS_EP03.map((c) => ({ ...c })); d.gherkin = { 'FD-101': GK_EP06 }; d.conquistas = ['ep03', 'ep06']; return d; } },
  { id: 'ep10', nome: 'Início do EP10', quando: 'Retestar os bugs', monta: depoisDoEp08 },
  { id: 'ep12', nome: 'Início do EP12', quando: 'Rodada de regressão', monta: depoisDoEp10 },
  { id: 'ep14', nome: 'Início do EP14', quando: 'Sprint 16', monta: depoisDoEp12 },
  { id: 'ep16', nome: 'Início do EP16', quando: 'O chamado duplicado · já efetivado como júnior', monta: () => { const d = depoisDoEp14(); d.conquistas.push('d1'); return d; } },
  { id: 'ep18', nome: 'Início do EP18', quando: 'Tela ou servidor?', monta: depoisDoEp16 },
  { id: 'ep20', nome: 'Início do EP20', quando: 'O rascunho · com a conta de teste do Lucas', monta: () => { LS.del(RASCUNHO); return contaDoLucas(depoisDoEp18()); } },
];


// ---------- missões (conferidas pelo próprio site) ----------
// Uma missão por prática guiada. O site confere sozinho e libera a conquista. Novas práticas: acrescentar aqui.
// cenário que ninguém consegue entender (nome de uma palavra só, resultado esperado curtinho) não conta na cobertura
const fraco = (c) => (c.nome || '').trim().split(/\s+/).length < 2 || (c.esperado || '').trim().length < 8;
const CHAVES = [/t[ií]tulo/i, /descri/i, /100|101|cem|limite|caracter/i, /anexo|arquivo|pdf|png|jpe?g|mb|exe/i, /mensagem|sucesso|tela do chamado|criad/i, /aberto|status/i, /espa[çc]o|vazi/i];
// a Gabriela lê o cenário como quem vai ter que executar: devolve [tom, recado]
function revisaCenario(c) {
  const nome = c.nome.trim(), esp = c.esperado.trim(), tudo = `${nome} ${c.passos} ${esp}`;
  if (nome.split(/\s+/).length < 2) return ['ruim', `“${nome}” não me diz o que vai ser testado. Dá um nome que eu entenda sem abrir, tipo “Criar sem título”. Do jeito que tá, ele não conta na cobertura.`];
  if (esp.length < 8) return ['ruim', 'O resultado esperado tá curto demais. O que aparece na tela? O que acontece com o chamado? Do jeito que tá, ele não conta na cobertura.'];
  if (/\bsem\b.+\be\b.+\bsem\b/i.test(nome)) return ['ruim', 'Aí tem dois testes num cenário só. Se falhar, qual dos dois quebrou? Separa em dois.'];
  if (/(deve|tem que|precisa|vai)\s+(funcionar|dar (erro|certo))|^(ok|funciona|d[áa] erro|d[áa] certo)\.?$/i.test(esp)) return ['ruim', `“${esp}” eu não consigo conferir. Escreve a mensagem exata que aparece e o que acontece com o chamado.`];
  const semChave = c.regras.find((i) => !CHAVES[i].test(tudo));
  if (semChave !== undefined) return ['ruim', `Você marcou a regra “${REGRAS[semChave]}”, mas o cenário não fala disso. Marcou a regra certa?`];
  if (!c.passos.trim()) return ['ruim', 'Sem os passos eu vou ter que adivinhar. Com o que eu preencho? Onde eu clico?'];
  if (c.tipo === 'P' && /\bsem\b|inv[áa]lid|errad|vazi/i.test(nome)) return ['ruim', 'Isso tem cara de cenário negativo, não positivo. Confere o tipo.'];
  if (!c.regras.length) return ['ok', 'Esse não cobre nenhuma regra do card. Se foi de propósito, boa: é assim que se acha o que ninguém pensou.'];
  return ['ok', ['Esse eu consigo testar sem te perguntar nada.', 'Claro e direto. Pode mandar o próximo.', 'Entendi de primeira. É isso.'][nome.length % 3]];
}
const coberturaFD101 = (d) => new Set((d.planos['FD-101'] || []).filter((c) => !fraco(c)).flatMap((c) => c.regras)).size;
const MISSOES = [
  { id: 'ep03', titulo: 'Plano de testes do FD-101', aula: 'EP04', conquista: 'Plano de testes no FlowDesk', nivel: 'QA estagiário', link: 'card.html?id=FD-101&aba=plano', itens: [
    ['Escreva pelo menos 8 cenários', (d) => (d.planos['FD-101'] || []).length >= 8],
    ['Use os três tipos: positivo, negativo e valor limite', (d) => ['P', 'N', 'L'].every((t) => (d.planos['FD-101'] || []).some((c) => c.tipo === t))],
    ['Cubra as 6 regras do card', (d) => coberturaFD101(d) >= 6],
    ['Encontre um cenário fora das regras', (d) => (d.planos['FD-101'] || []).some((c) => !c.regras.length)],
  ] },
  { id: 'ep06', titulo: 'Cenários do FD-101 em Gherkin', aula: 'EP06', conquista: 'Feature do FD-101 no FlowDesk', nivel: 'QA estagiário', link: 'card.html?id=FD-101&aba=gherkin', itens: [
    ['Comece pela Funcionalidade', (d) => revisaGherkin(gherkinDe(d)).funcionalidade],
    ['Escreva pelo menos 4 cenários', (d) => revisaGherkin(gherkinDe(d)).cenarios.length >= 4],
    ['Todo cenário com Dado, Quando e Então', (d) => { const r = revisaGherkin(gherkinDe(d)); return r.cenarios.length > 0 && r.cenarios.every((c) => c.dado && c.quando && c.entao && !c.ordem); }],
    ['Um Quando por cenário: uma ação só', (d) => { const r = revisaGherkin(gherkinDe(d)); return r.cenarios.length > 0 && r.cenarios.every((c) => c.acoes <= 1); }],
    ['Nenhum Então vago', (d) => { const r = revisaGherkin(gherkinDe(d)); return r.cenarios.length > 0 && r.cenarios.every((c) => !c.vago.length); }],
  ] },
  { id: 'ep08', titulo: 'Executar o plano do FD-101', aula: 'EP08', conquista: 'Primeiros bugs achados', nivel: 'QA estagiário', link: 'card.html?id=FD-101&aba=plano', itens: [
    ['Execute todos os cenários do plano', (d) => { const l = d.planos['FD-101'] || []; return l.length >= 8 && l.every((c) => c.exec && c.exec !== 'nao'); }],
    ['Reporte o bug do título só com espaços', (d) => bugsDe(d).some((b) => /espa[çc]o/i.test(textoBug(b)))],
    ['Ache e reporte o bug do anexo', (d) => bugsDe(d).some((b) => /anexo|5\s?mb|arquivo/i.test(textoBug(b)))],
    ['Todo cenário que falhou tem um bug ligado', (d) => { const f = (d.planos['FD-101'] || []).filter((c) => c.exec === 'falhou'); return f.length > 0 && f.every((c) => c.bug); }],
  ] },
  { id: 'ep10', titulo: 'Retestar os bugs da Sprint 15', aula: 'EP10', conquista: 'Bugs fechados com reteste', nivel: 'QA estagiário', link: 'quadro.html', itens: [
    ['Reteste na versão certa: Sprint 15', (d) => { const r = bugsDe(d).filter((b) => b.corrigidoEm === 15).flatMap((b) => b.retestes || []); return r.length >= 2 && r.every((x) => x.versao >= 15); }],
    ['Reteste o bug do título com evidência', (d) => bugsDe(d).some((b) => /espa[çc]o/i.test(textoBug(b)) && (b.retestes || []).some((r) => r.res === 'passou' && r.evid))],
    ['Reteste o bug do anexo com evidência', (d) => bugsDe(d).some((b) => /anexo|5\s?mb|arquivo/i.test(textoBug(b)) && (b.retestes || []).some((r) => r.res === 'passou' && r.evid))],
    ['Feche os dois bugs', (d) => { const b = bugsDe(d).filter((x) => x.corrigidoEm === 15); return b.length >= 2 && b.every((x) => x.coluna === 'concluido'); }],
  ] },
  { id: 'ep12', titulo: 'Rodada de regressão da Sprint 15', aula: 'EP12', conquista: 'Primeira regressão pega', nivel: 'QA estagiário', link: 'card.html?id=FD-101&aba=plano', itens: [
    ['Abra a rodada 2 só com o que a correção encosta', (d) => { const R = rodadaDe(d), l = d.planos['FD-101'] || []; return !!R && R.n >= 2 && R.versao === 15 && l.every((c, i) => cenSoDescricao(c) ? !R.sel.includes(i) : (cenTitulo(c) || cenAnexo(c) || cenFeliz(c)) && c.regras.length ? R.sel.includes(i) : true); }],
    ['Execute a rodada com evidência em todos', (d) => { const R = rodadaDe(d), l = d.planos['FD-101'] || []; return !!R && R.versao === 15 && R.sel.length > 0 && R.sel.every((i) => l[i] && l[i].exec !== 'nao' && l[i].evid); }],
    ['Reporte o bug de regressão com as versões', (d) => bugsDe(d).some((b) => b.regressao && b.funcionava && b.quebrou)],
    ['Avise a Beatriz no FlowChat', (d) => { const R = rodadaDe(d); return !!R && Object.values(d.chat).some((m) => m.some((x) => x.de === 'voce' && x.quando >= R.data && !/^(Abri|Reabri) o BUG-\d+/.test(x.tx) && /regress|release|segur|recomend|subir|quebr/i.test(x.tx))); }],
  ] },
  { id: 'ep14', titulo: 'Fechar o ciclo na Sprint 16', aula: 'EP14', conquista: 'Ciclo fechado', nivel: 'QA estagiário', link: 'quadro.html', itens: [
    ['Reteste e feche o bug de regressão', (d) => bugsDe(d).some((b) => b.corrigidoEm === 16 && b.coluna === 'concluido' && (b.retestes || []).some((r) => r.versao === 16 && r.res === 'passou'))],
    ['Rode a rodada 3: caminho feliz e cenários de título', (d) => { const R = rodadaDe(d), l = d.planos['FD-101'] || []; return !!R && R.n >= 3 && R.versao === 16 && l.some((c, i) => cenFeliz(c) && R.sel.includes(i)) && l.every((c, i) => !(cenTitulo(c) && c.regras.length) || R.sel.includes(i)) && R.sel.every((i) => l[i] && l[i].exec !== 'nao' && l[i].evid); }],
    ['Ligue o cenário do título só com espaços à regra nova', (d) => (d.planos['FD-101'] || []).some((c) => c.regras.includes(6))],
    ['Escreva o cenário de regressão no Gherkin', (d) => /^\s*Cen[aá]rio:[^\n]*espa[çc]o[^\n]*\n(?:[^\n]*\n)*?\s*Ent[aã]o\s+\S/im.test(gherkinDe(d))],
  ] },
  { id: 'ep16', titulo: 'Achar a condição do duplicado', aula: 'EP16', conquista: 'Bug intermitente com condição', nivel: 'QA júnior', link: 'novo-chamado.html', itens: [
    ['Faça o chamado sair em dobro', (d) => { const l = d.chamados.filter((c) => c.criadoPor === 'Você' && c.v >= 17); return l.some((a) => l.some((b) => b !== a && b.titulo === a.titulo && Math.abs(new Date(b.criadoEm) - new Date(a.criadoEm)) < 15000)); }],
    ['Reporte com a condição no título', (d) => bugsDe(d).some((b) => /lent|3g|rede/i.test(b.titulo) && /dobro|duplic|duas vezes|dois|2x/i.test(b.titulo))],
    ['Comece os passos pela rede lenta', (d) => bugsDe(d).some((b) => /dobro|duplic/i.test(b.titulo) && /lent|3g/i.test((b.passos || '').split('\n')[0]))],
    ['Diga a frequência', (d) => bugsDe(d).some((b) => /dobro|duplic/i.test(b.titulo) && /\d+\s*(de|em|\/)\s*\d+/i.test(textoBug(b) + ' ' + (b.tecnico || '')))],
  ] },
  { id: 'ep18', titulo: 'Tela ou servidor?', aula: 'EP18', conquista: 'Bug no lugar certo', nivel: 'QA júnior', link: 'chamados.html', itens: [
    ['Reporte o bug da busca com acento', (d) => bugsDe(d).some((b) => /acento|manuten/i.test(textoBug(b)))],
    ['Mostre que ele está no servidor', (d) => bugsDe(d).some((b) => /acento|manuten/i.test(textoBug(b)) && /servidor|resposta|api|back|\[\]/i.test(textoBug(b) + ' ' + (b.tecnico || '')))],
    ['Reporte o bug do emoji', (d) => bugsDe(d).some((b) => /emoji|🔥|carregando|urierror/i.test(textoBug(b) + ' ' + (b.tecnico || '')))],
    ['Cole o erro do Console', (d) => bugsDe(d).some((b) => /urierror|malformed/i.test((b.tecnico || '') + ' ' + textoBug(b)))],
  ] },
  { id: 'ep20', titulo: 'O rascunho que vaza', aula: 'EP20', conquista: 'Dado no navegador', nivel: 'QA júnior', link: 'novo-chamado.html', itens: [
    ['Faça o rascunho aparecer pra outra conta', () => vazouRascunho()],
    ['Reporte o bug do rascunho', (d) => bugsGlobais(d).some((b) => /rascunho/i.test(textoBug(b)))],
    ['Com prioridade alta', (d) => bugsGlobais(d).some((b) => /rascunho/i.test(textoBug(b)) && /alta|cr[ií]tica|urgente/i.test(b.prioridade || ''))],
    ['Com a chave do armazenamento em Console e Rede', (d) => bugsGlobais(d).some((b) => /rascunho/i.test(textoBug(b)) && /fd:rascunho|rascunho/i.test(b.tecnico || ''))],
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
function nivelAtual() { const d = dados() || {}; if ((d.conquistas || []).includes('d1')) return 'QA júnior'; const fe = MISSOES.filter((m) => (d.conquistas || []).includes(m.id)); return fe.length ? fe[fe.length - 1].nivel : 'QA estagiário'; }
function confereMissoes() {
  const d = dados(); d.conquistas = d.conquistas || []; let nova = false;
  MISSOES.forEach((m) => {
    if (d.conquistas.includes(m.id) || !progresso(m, d).every(Boolean)) return;
    d.conquistas.push(m.id); if (m.id === 'ep14' && d.chat.releases) d.chat.releases.push({ de: 'beatriz', tx: 'Sprint 16 aprovada. Sobe sexta 🚀', quando: agora() }); if (m.id === 'ep18' && d.chat.bugs) d.chat.bugs.push({ de: 'gabriela', tx: 'O seis eu corrijo hoje. O cinco é na API, vou chamar o Lucas.', quando: agora() }); salvar(); conquista(m); nova = true;
  });
  const el = $('#missaoSide'); if (el) el.outerHTML = cardMissao();
  if (!nova && !$('.conq-fundo')) refrescaCarreira();  // com conquista nova, a barra sobe quando o aluno fecha o aviso
}
// a barra de carreira do topo acompanha o XP na hora (com animação), sem precisar recarregar a página
function refrescaCarreira() {
  const velho = $('.barra [data-test=carreira]'); if (!velho) return;
  const d = dados(), antes = $$('.tb i', velho).map((i) => i.style.width);
  const tmp = document.createElement('div'); tmp.innerHTML = trilha(d); const novo = tmp.firstElementChild;
  const alvo = $$('.tb i', novo).map((i) => i.style.width);
  if (velho.outerHTML === novo.outerHTML) return;
  $$('.tb i', novo).forEach((i, k) => { i.style.width = antes[k] || '0%'; });
  velho.replaceWith(novo); void novo.offsetWidth;
  $$('.tb i', novo).forEach((i, k) => { i.style.width = alvo[k]; });
  const x = $('.barra [data-test=xp]'); if (x) x.textContent = `${xpDe(d)} / ${ehJunior(d) ? XP_PLENO : XP_JUNIOR} XP`;
}
function conquista(m) {
  const o = document.createElement('div'); o.className = 'conq-fundo'; o.setAttribute('data-test', 'conquista');
  const extra = m.id === 'ep12' ? '<div class="s2">A Gabriela já está corrigindo. Quando você voltar pro FlowDesk, a <b>Sprint 16</b> estará no ar.</div>' : m.id === 'ep14' ? '<div class="s2">Fim do módulo 2. A Sprint 16 foi aprovada e sobe sexta.</div>' : m.id === 'ep20' ? '<div class="s2">Fim do módulo 3. Três bugs que a tela sozinha não mostrava, e você achou onde cada um mora.</div>' : m.id === 'ep08' ? '<div class="s2">A Gabriela já está corrigindo. Quando você voltar pro FlowDesk, a <b>Sprint 15</b> estará no ar.</div>' : m.id === 'ep03' ? '<div class="s2">O <b>FlowChat</b> foi liberado: agora dá pra tirar dúvida com o time.</div>' : '';
  o.innerHTML = `<div class="conq"><div class="ci">${ico('trofeu')}</div><div class="k">CONQUISTA DESBLOQUEADA · +${m.itens.length * XP_ITEM + XP_CONQ} XP</div><div class="v" data-test="conquista-nome">${m.conquista}</div><div class="s">Nível atual: <b>${m.nivel}</b></div>${extra}<button class="btn" data-test="fechar-conquista">Continuar</button></div>`;
  // fica pendente até o aluno fechar: se a página recarregar antes (reteste, troca de tela), o aviso volta
  const d = dados(); d.conqPendente = m.id; salvar();
  document.body.appendChild(o); $('[data-test=fechar-conquista]', o).onclick = () => { o.remove(); delete dados().conqPendente; salvar(); setTimeout(refrescaCarreira, 250); };
  const nv = $('[data-test=nivel]'); if (nv) nv.textContent = m.nivel;
}
function cardMissao() {
  const m = missaoAtual();
  if (!m) return '<a class="missao-side feita" id="missaoSide" href="missoes.html" data-test="missao-atual"><div class="k">MISSÕES</div><div class="t">Tudo feito por agora</div><div class="p">A próxima chega na próxima prática</div></a>';
  const pr = progresso(m), n = pr.filter(Boolean).length;
  return `<a class="missao-side" id="missaoSide" href="missoes.html" data-test="missao-atual"><div class="k">MISSÃO DO ${m.aula.toUpperCase()}</div><div class="t">${m.titulo}</div><div class="bar"><i style="width:${n / pr.length * 100}%"></i></div><div class="p" data-test="missao-progresso">${n}/${pr.length}</div><div class="pop" data-test="missao-lista"><div class="k">SUA MISSÃO</div>${m.itens.map(([t], i) => `<div class="pit ${pr[i] ? 'on' : ''}"><b>${pr[i] ? '✓' : i + 1}</b>${t}</div>`).join('')}</div></a>`;
}

// ---------- carreira (XP vem das missões) ----------
// júnior vem com a efetivação (Desafio 1, no fim do módulo 2): a conquista 'd1' leva o XP pra 3000; daí em diante conta o XP do módulo 3 em diante
const XP_ITEM = 40, XP_CONQ = 60, XP_JUNIOR = 3000, XP_PLENO = 6000;
const M_JUNIOR = ['ep16', 'ep18', 'ep20'];
const ehJunior = (d = dados()) => xpDe(d) >= XP_JUNIOR;
const xpDe = (d = dados()) => { const f = d.conquistas || [], atual = MISSOES.find((m) => !f.includes(m.id)), efetivado = f.includes('d1');
  return (efetivado ? XP_JUNIOR : 0) + MISSOES.reduce((s, m) => (efetivado && !M_JUNIOR.includes(m.id)) ? s : s + (f.includes(m.id) ? m.itens.length * XP_ITEM + XP_CONQ : m === atual ? progresso(m, d).filter(Boolean).length * XP_ITEM : 0), 0); };
function trilha(d = dados()) {
  const xp = xpDe(d), jr = xp >= XP_JUNIOR;
  const a = jr ? 1 : Math.min(xp / XP_JUNIOR, .98), b = jr ? Math.min((xp - XP_JUNIOR) / (XP_PLENO - XP_JUNIOR), .98) : 0;
  const ok = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12l5 5 9-10"/></svg>';
  return `<div class="trilha" data-test="carreira"><span class="nv on">${ok}Estagiário</span><span class="tb"><i style="width:${a * 100}%"></i></span><span class="nv ${jr ? 'on' : ''}">${jr ? ok : ''}Júnior</span><span class="tb"><i style="width:${Math.max(b, 0) * 100}%"></i></span><span class="nv fut">Pleno</span></div>`;
}
const chatLiberado = (d = dados()) => (d.conquistas || []).includes('ep03');

// ---------- layout ----------
const avatar = (p) => p === 'voce' ? '<span class="vc">VC</span>' : `<img class="av" src="img/av_${p}.png" alt="">`;
const LOGO = '<span class="logo-anim" aria-hidden="true"><img src="img/anim/logo_part1.png?v=1794479423" alt=""><img class="sobe" src="img/anim/logo_part0.png?v=1794479423" alt=""></span>';
const MARCA = `<span class="marca">${LOGO}FlowDesk</span>`;
const pillVersao = () => `<span class="versao" data-test="versao-sistema"><b>Sprint ${VERSAO}</b> · homologação</span>`;
const SVG = (p, c = '') => `<svg class="${c}" viewBox="0 0 24 24" aria-hidden="true">${p}</svg>`;
const ICONE = {
  dashboard: '<path d="M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>',
  chamados: '<path d="M4 5h16v14H4z"/><path d="M4 10h16M9 15h6"/>',
  quadro: '<path d="M4 4h4v16H4zM10 4h4v10h-4zM16 4h4v13h-4z"/>',
  plano: '<path d="M9 5h11M9 12h11M9 19h11"/><path d="m3.5 5 1.5 1.5L7.5 4M3.5 12l1.5 1.5L7.5 11M3.5 19l1.5 1.5L7.5 18"/>',
  chat: '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>',
  caca: '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4M8 11h6M11 8v6"/>',
  configuracoes: '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1 7 17M17 7l2.1-2.1"/>',
  card: '<rect x="4" y="4" width="16" height="16" rx="3"/><path d="M8 9h8M8 13h5"/>',
  gherkin: '<path d="m8 8-4 4 4 4M16 8l4 4-4 4"/>',
  cadeado: '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
  bug: '<path d="M8 6a4 4 0 0 1 8 0v1H8zM6 10h12v4a6 6 0 0 1-12 0zM3 13h3M18 13h3M4 8l3 2M20 8l-3 2M12 10v10"/>',
  clipe: '<path d="M21 11.5 12.5 20a5 5 0 0 1-7-7L14 4.5a3.5 3.5 0 0 1 5 5L10.5 18a2 2 0 0 1-3-3L15 7.5"/>',
  trofeu: '<path d="M8 21h8M12 17v4M7 4h10v5a5 5 0 0 1-10 0zM7 6H4a3 3 0 0 0 3 4M17 6h3a3 3 0 0 1-3 4"/>',
  seta: '<path d="M5 12h14M13 6l6 6-6 6"/>',
  sino: '<path d="M18 8a6 6 0 1 0-12 0c0 7-3 8-3 8h18s-3-1-3-8"/><path d="M13.7 21a2 2 0 0 1-3.4 0"/>',
};
const ico = (k, c = '') => SVG(ICONE[k], c);
const placarCache = () => LS.get('fd:placar', null);
function casca(pagina, conteudo) {
  const c = contas()[sessao()] || { nome: '' }, d = dados();
  const [pg, aba] = pagina.split(':');
  const it = (h, n, k, extra = '') => `<a href="${h}" data-test="menu-${k}" class="${pg === k ? 'on' : ''}">${ico(k)}<span>${n}</span>${extra}</a>`;
  const sub = (h, n, k) => `<a href="${h}" class="${pg === 'card' && (aba || 'detalhes') === k ? 'on' : ''}" data-sub="${k}" data-test="sub-${k}">${n}</a>`;
  const pc = placarCache(), achados = pc ? pc.bugs.filter((b) => b.ganhador).length : 0;
  const naoLidas = chatLiberado(d) ? '' : `<span class="tranca" title="Libera depois da missão do EP04">${ico('cadeado')}</span>`;
  document.body.innerHTML = `<div class="app"><aside class="side">${MARCA}<nav aria-label="Menu">
    ${it('dashboard.html', 'Início', 'dashboard')}${it('quadro.html', 'Quadro', 'quadro')}
    <div class="sub-nav"><div class="sub-k">Seu card · FD-101</div>${sub('card.html?id=FD-101', 'Visão geral', 'detalhes')}${sub('card.html?id=FD-101&aba=plano', 'Plano de testes', 'plano')}${sub('card.html?id=FD-101&aba=gherkin', 'Gherkin', 'gherkin')}</div>
    ${it('chamados.html', 'Chamados', 'chamados')}${it('chat.html', 'FlowChat', 'chat', naoLidas)}${it('caca.html', 'Caça aos bugs', 'caca', `<span class="caca-n">${achados}/3</span>`)}</nav>
    <div class="side-fim">${cardMissao()}<nav class="sec-nav">${it('configuracoes.html', 'Configurações', 'configuracoes')}</nav>
    <div class="eu"><span class="vc">${esc((c.nome || 'VC').split(' ').map((x) => x[0]).slice(0, 2).join('').toUpperCase())}</span><div><b data-test="usuario-logado">${esc(c.nome)}</b><span data-test="nivel">${nivelAtual()}</span></div><button data-test="sair">Sair</button></div></div></aside>
    <main class="main"><header class="barra"><div class="barra-c"><span class="barra-k">CARREIRA</span>${trilha(d)}<span class="xp" data-test="xp">${xpDe(d)} / ${ehJunior(d) ? XP_PLENO : XP_JUNIOR} XP</span></div>${pillVersao()}</header><div class="conteudo">${conteudo}</div></main></div>`;
  $('[data-test=sair]').onclick = sair;
  mostraRecado(); setTimeout(() => { confereMissoes(); const pend = (dados() || {}).conqPendente, m = pend && MISSOES.find((x) => x.id === pend); if (m && !$('.conq-fundo')) conquista(m); }, 300);
  if (CACA_API && pg !== 'caca') fetch(`${CACA_API}/placar`).then((r) => r.json()).then((p) => LS.set('fd:placar', { bugs: p.bugs, temporada: p.temporada, encerrada: p.encerrada })).catch(() => {});
}
function sair() { LS.del('fd:sessao'); location.href = 'index.html'; }
const topo = (titulo, sub = '', crumb = '', acoes = '') => `<div class="topo"><div>${crumb ? `<div class="crumb">${crumb}</div>` : ''}<h2 data-test="titulo-pagina">${titulo}</h2>${sub ? `<div class="sub">${sub}</div>` : ''}</div>${acoes ? `<div class="topo-acoes">${acoes}</div>` : ''}</div>`;
// fala do mentor (balão)
const fala = (p, quem, tx, cls = '') => `<div class="fala ${cls}"><img src="img/av_${p}.png" alt="${PESSOAS[p].nome}"><div class="bal"><div class="bk">${quem}</div><div class="bt">${tx}</div></div></div>`;
const stClasse = (s) => 'st st-' + ({ 'Aberto': 'aberto', 'Em andamento': 'andamento', 'Resolvido': 'resolvido', 'Fechado': 'fechado' }[s] || 'aberto');
const erroCampo = (id, msg) => { const e = $('#' + id); e.classList.add('erro'); const m = document.createElement('div'); m.className = 'msg-erro'; m.setAttribute('data-test', 'erro-' + id); m.textContent = msg; (e.closest('.arquivo') || e).after(m); };
const limpaErros = () => { $$('.msg-erro').forEach((m) => m.remove()); $$('.erro').forEach((e) => e.classList.remove('erro')); };

// ---------- quem pode mover o quê ----------
// O QA só move os próprios cards: de Pronto pra QA pra Em teste (e de volta), e de Em teste pra Concluído quando todos os critérios estão marcados.
const MOVES_QA = { qa: ['teste'], teste: ['qa', 'concluido'] };
function critEstado(d, c) {
  const pl = d.planos[c.id];
  return c.criterios.map((t, i) => {
    if (!pl) return { t, cen: [], st: c.ok.includes(i) ? 'ok' : 'nada' };
    const cen = pl.map((x, j) => x.regras.includes(i) && !fraco(x) ? j : -1).filter((j) => j >= 0);
    const st = !cen.length ? 'nada' : cen.some((j) => pl[j].exec === 'falhou') ? 'falhou' : cen.every((j) => pl[j].exec === 'passou') ? 'ok' : 'testar';
    return { t, cen, st, bugs: cen.map((j) => pl[j].bug).filter(Boolean) };
  });
}
const critOk = (d, c) => critEstado(d, c).map((x, i) => x.st === 'ok' ? i : -1).filter((i) => i >= 0);
function podeMover(c, destino) {
  if (c.coluna === destino) return { ok: false, msg: '' };
  if (c.resp !== 'voce') return { ok: false, msg: `Esse card é ${c.resp === 'gabriela' || c.resp === 'beatriz' ? 'da' : 'do'} ${PESSOAS[c.resp].nome}. Só quem é responsável move.` };
  if (!(MOVES_QA[c.coluna] || []).includes(destino)) return { ok: false, msg: 'O QA não faz esse movimento. Daqui o card só vai pra ' + (MOVES_QA[c.coluna] || []).map((k) => COLUNAS.find((x) => x[0] === k)[1].toLowerCase()).join(' ou ') + '.' };
  if (destino === 'concluido' && c.criterios.length && critOk(dados(), c).length < c.criterios.length) return { ok: false, msg: 'Antes de concluir, todo critério de aceite precisa estar validado pelo plano de testes.' };
  return { ok: true };
}

// ---------- páginas ----------
const PAGINAS = {};

PAGINAS.login = () => {
  if (sessao() && contas()[sessao()]) return location.replace('dashboard.html');
  const seta = '<svg width="22" height="12" viewBox="0 0 22 12" aria-hidden="true"><path d="M1 6h18M15 1l5 5-5 5"/></svg>';
  document.body.innerHTML = `<div class="tela-login">
    <section class="lg-time"><div class="lg-marca">${LOGO}<span>FlowDesk</span></div>
      <div class="lg-tit"><h1>Seu primeiro dia como QA começa aqui.</h1><div class="lg-trilha"><span class="on">Estagiário</span>${seta}<span>Júnior</span>${seta}<span class="fut">Pleno</span></div></div>
      <div class="lg-palco"><div class="lg-luz" aria-hidden="true"></div><video src="img/anim/time_acena.webm?v=1794479423" poster="img/anim/time_acena.png?v=1794479423" autoplay muted loop playsinline aria-label="O time do FlowDesk acenando: Rafael, Gabriela, Vinícius, Lucas e Beatriz"></video></div></section>
    <section class="lg-form"><div class="login">
    <form id="fEntrar" novalidate><span class="lg-chip">SPRINT ${VERSAO} · HOMOLOGAÇÃO</span><h1>Bem-vindo de volta</h1><p class="sub">O time já está te esperando. Use dados de mentira: fica tudo salvo só neste navegador.</p>
      <div class="campo"><label for="email">E-mail</label><input class="in" id="email" type="email" data-test="login-email" autocomplete="username" placeholder="voce@empresa.com"></div>
      <div class="campo"><label for="senha">Senha</label><input class="in" id="senha" type="password" data-test="login-senha" autocomplete="current-password" placeholder="Sua senha"></div>
      ${contas()['lucas@flowdesk.com'] ? '<p class="conta-teste" data-test="conta-teste">Conta de teste do time: <b>lucas@flowdesk.com</b> · senha <b>123456</b></p>' : ''}
      <button class="btn cheio" data-test="login-entrar">Entrar</button>
      <div class="ou"><span></span>primeira vez?<span></span></div>
      <button type="button" class="btn sec cheio" data-test="ir-criar-conta">Criar minha conta</button></form>
    <form id="fCriar" novalidate hidden><span class="lg-chip">PRIMEIRO DIA</span><h1>Criar conta</h1><p class="sub">Seu primeiro acesso ao FlowDesk. Use dados de mentira: fica tudo salvo só neste navegador.</p>
      <div class="campo"><label for="nome">Seu nome</label><input class="in" id="nome" data-test="cadastro-nome" autocomplete="name"></div>
      <div class="campo"><label for="cemail">E-mail</label><input class="in" id="cemail" type="email" data-test="cadastro-email" autocomplete="username"></div>
      <div class="campo"><label for="csenha">Senha <small>(mínimo 6 caracteres)</small></label><input class="in" id="csenha" type="password" data-test="cadastro-senha" autocomplete="new-password"></div>
      <button class="btn cheio" data-test="cadastro-criar">Criar conta e entrar</button>
      <div class="troca">Já tem conta? <button type="button" data-test="ir-entrar">Entrar</button></div></form>
    <p class="aviso">Site de treino do curso <b>Vida de QA</b>.</p></div>
    <div class="lg-feat"><div>${ico('plano')}<b>Plano de testes</b><span>Do card ao cenário</span></div><div>${ico('gherkin')}<b>Gherkin</b><span>Dado, Quando, Então</span></div><div>${ico('caca')}<b>Bugs reais</b><span>Escondidos no sistema</span></div></div></section>
  </div>`;
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

const DICA_MISSAO = {
  ep03: 'Termina o plano do FD-101: cada regra do card precisa de pelo menos um cenário.',
  ep06: 'Agora passa os cenários pro Gherkin. Dado, Quando, Então, e um Quando por cenário.',
  ep08: 'Hora de executar o plano. Cenário que falhar vira bug, com passos e evidência.',
  ep10: 'A Gabriela corrigiu os bugs. Refaça os passos de cada um, na Sprint 15, e feche com o print.',
  ep12: 'Abra a rodada 2 só com o que a correção encosta, e execute com evidência.',
  ep14: 'Sprint 16 no ar: reteste o bug de regressão, rode a rodada 3 e deixe a suíte em dia.',
  ep16: 'A padaria diz que às vezes o chamado sai em dobro. Ache a condição com a aba Rede e reporte.',
  ep18: 'A busca falha com acento e com emoji. Descubra se cada bug está na tela ou no servidor.',
  ep20: 'Um rascunho aparece pra quem não escreveu. Ache onde ele mora e prove com outra conta.',
};
PAGINAS.dashboard = () => {
  const d = dados(), c = contas()[sessao()];
  const h = new Date().getHours(), oi = h < 12 ? 'Bom dia' : h < 18 ? 'Boa tarde' : 'Boa noite';
  const hoje = new Date().toLocaleDateString('pt-BR', { weekday: 'long', day: 'numeric', month: 'long' });
  const meus = d.cards.filter((x) => x.resp === 'voce');
  const m = missaoAtual(), pr = m ? progresso(m, d) : [], xp = xpDe(d), jr = xp >= XP_JUNIOR;
  const falta = (jr ? XP_PLENO : XP_JUNIOR) - xp;
  const msg = m ? `Faltam ${falta} XP pra ${jr ? 'pleno' : 'júnior'}. ${DICA_MISSAO[m.id] || ''}` : 'Mandou bem. A próxima missão chega na próxima prática do curso.';
  const okSvg = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12l5 5 9-10"/></svg>';
  const hero = m ? `<a class="hero" href="${m.link}" data-test="missao-hero"><div class="hk"><span>MISSÃO DO ${m.aula}</span><i>+${m.itens.length * XP_ITEM + XP_CONQ} XP</i></div><div class="ht">${m.titulo}</div>
      <div class="hl">${m.itens.map(([t], i) => `<div class="pit ${pr[i] ? 'on' : ''}"><b>${pr[i] ? okSvg : i + 1}</b>${t}</div>`).join('')}</div><div class="hb"><span class="btn ouro">Continuar a missão ${ico('seta')}</span><span class="hn">${pr.filter(Boolean).length} de ${pr.length} feitos</span></div>
      <svg class="hero-alvo" viewBox="0 0 220 220" aria-hidden="true"><circle cx="110" cy="110" r="90" stroke-dasharray="4 10"/><circle cx="110" cy="110" r="55"/><circle cx="110" cy="110" r="18" class="f"/></svg></a>`
    : `<div class="hero feita" data-test="missao-hero"><div class="hk"><span>MISSÕES</span></div><div class="ht">Tudo feito por agora</div><p class="dica">A próxima missão chega na próxima prática do curso.</p></div>`;
  const ultGabi = [...d.chat['time-produto']].reverse().find((x) => x.de === 'gabriela');
  const linhaTime = { rafael: 'Dúvida de regra é com ele', gabriela: ultGabi ? `“${ultGabi.tx.replace(/\s*\p{Extended_Pictographic}/gu, '')}”` : 'Desenvolve o FD-101', lucas: 'Daily às 9h15', beatriz: 'Review na sexta, 16h', vinicius: 'Seu mentor, pode perguntar' };
  const pc = placarCache(), bugs = pc ? pc.bugs : [1, 2, 3].map((n) => ({ n, ganhador: null }));
  const mesNome = new Date().toLocaleDateString('pt-BR', { month: 'long' }).toUpperCase();
  casca('dashboard', `<section class="saud"><div><div class="dia">${hoje.charAt(0).toUpperCase() + hoje.slice(1)}</div><h1 data-test="titulo-pagina">${oi}, ${esc(c.nome.split(' ')[0])}.</h1></div>
      ${fala('vinicius', 'VINÍCIUS · SEU MENTOR', msg)}</section>
    <div class="grade">
      <div class="g2">${hero}</div>
      <section class="painel"><div class="ph"><h3>Seu time</h3><a href="chat.html">FlowChat</a></div><div class="time" data-test="time">${TIME.filter(([p]) => p !== 'vinicius').map(([p]) => `<a class="pes" href="chat.html"><img src="img/av_${p}.png" alt=""><div><b>${PESSOAS[p].nome} <i>${PESSOAS[p].papel.toUpperCase()}</i></b><span>${esc(linhaTime[p])}</span></div></a>`).join('')}</div></section>
      <div class="g3"><section class="painel"><div class="ph"><h3>Sua semana</h3></div><div class="nums"><div><b>${(d.planos['FD-101'] || []).length}</b><span>cenários escritos</span></div><div><b class="r">${bugsDe(d).length}</b><span>bugs achados</span></div><div><b class="o">${(d.conquistas || []).length}</b><span>conquistas</span></div></div></section>
      <section class="painel"><div class="ph"><h3>Com você agora</h3></div>${meus.length ? meus.map(cardFace).join('') : '<p class="dica">Nenhum card com você agora.</p>'}</section>
      <a class="painel caca-mini" href="caca.html" data-test="caca-resumo"><div class="ck">CAÇA AOS BUGS · ${mesNome}</div><h3>3 bugs escondidos</h3><p>Os 3 primeiros a achar ganham o Vida de QA 2.</p><div class="cs">${bugs.map((b) => b.ganhador ? `<span class="on">#${b.n} ${esc(b.ganhador)}</span>` : `<span>#${b.n} livre</span>`).join('')}</div></a></div>
    </div>`);
};

const COR_CLIENTE = ['#3b2410|#fdba74', '#0f2e1e|#86efac', '#0f1a2e|#93c5fd', '#2e1430|#f0abfc', '#0f2a2e|#5eead4', '#2a2a10|#fde047', '#2e1018|#fda4af'];
const corCliente = (n) => { let h = 0; for (const ch of n) h = (h * 31 + ch.charCodeAt(0)) % 997; return COR_CLIENTE[h % COR_CLIENTE.length].split('|'); };
const COR_ST = { 'Aberto': '#a78bfa', 'Em andamento': '#f59e0b', 'Resolvido': '#22c55e', 'Fechado': '#6b6e86' };
function relativo(iso) {
  const min = Math.round((Date.now() - new Date(iso)) / 60000);
  if (min < 1) return 'agora'; if (min < 60) return `há ${min} min`;
  const h = Math.round(min / 60); if (h < 24) return `há ${h} h`;
  const d = Math.round(h / 24); return d === 1 ? 'ontem' : `há ${d} dias`;
}
PAGINAS.chamados = () => {
  const todos = dados().chamados, n = (st) => todos.filter((x) => !st || x.status === st).length;
  const meus = todos.filter((x) => x.criadoPor === 'Você');
  const dica = meus.length
    ? `Você já criou ${meus.length === 1 ? 'um chamado' : meus.length + ' chamados'} aqui. Abre o seu e confere: título, descrição, anexo e status ficaram do jeito que o card pede?`
    : 'Olha o #1008: título “ajuda” e descrição só com um ponto. Ninguém do suporte sabe o que fazer com isso. É esse problema que o FD-101 resolve, e é a tela de Novo chamado que você vai testar.';
  casca('chamados', `<div class="ch-topo"><div><h2 data-test="titulo-pagina">Chamados</h2><div class="sub">Pedidos de ajuda dos clientes do FlowDesk. É aqui que o suporte trabalha todo dia.</div></div>
      <a class="btn" href="novo-chamado.html" data-test="novo-chamado">+ Novo chamado</a></div>
    <a class="testa-aqui" href="card.html?id=FD-101"><span class="ta-ic">${ico('card')}</span><div><b>Você está testando a tela de Novo chamado</b><span>Card FD-101 · Criar chamado. Cada chamado que você cria aparece nesta lista.</span></div><i>Ver o card ${ico('seta')}</i></a>
    <div class="ch-filtros"><label class="busca">${SVG('<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>')}<input id="busca" type="search" placeholder="Buscar pelo título" data-test="busca-chamado" aria-label="Buscar pelo título"></label>
      <div class="chips" role="group" aria-label="Filtrar por status"><button type="button" class="chip on" data-st="">Todos <b>${n('')}</b></button>${STATUS.map((st) => `<button type="button" class="chip" data-st="${st}"><i style="background:${COR_ST[st]}"></i>${st} <b>${n(st)}</b></button>`).join('')}</div>
      <select class="exec-sel" id="filtro" data-test="filtro-status" aria-hidden="true" tabindex="-1"><option value="">Todos os status</option>${STATUS.map((st) => `<option>${st}</option>`).join('')}</select></div>
    <div class="ch-lista"><table class="tabela ch-tab"><thead><tr><th>Nº</th><th>Título</th><th>Cliente</th><th>Status</th><th>Criado</th></tr></thead><tbody id="linhas"></tbody></table></div>
    <div class="ch-dica">${fala('vinicius', 'DICA DO VINÍCIUS', dica)}</div>`);
  const pinta = () => {
    const b = (_c('busca') ? $('#busca').value.replace(/^\s+/, '') : $('#busca').value.trim()).toLowerCase(), f = $('#filtro').value;
    $$('.chips .chip').forEach((c) => c.classList.toggle('on', c.dataset.st === f));
    const l = [...dados().chamados].sort((a, c) => c.id - a.id).filter((x) => (!f || x.status === f || (_c('lista') && b.length > 0)) && x.titulo.toLowerCase().includes(b) && !(f === 'Fechado' && _c('fechado') && innerWidth <= 480));
    $('#linhas').innerHTML = l.length ? l.map((x) => { const [bg, cor] = corCliente(x.cliente);
      const chip = x.criadoPor === 'Você' ? '<span class="por-voce">criado por você</span>' : x.id === 1008 ? '<span class="exemplo">o problema do FD-101</span>' : '';
      return `<tr data-test="linha-chamado" data-href="chamado.html?id=${x.id}"><td class="num">#${x.id}</td><td><div class="tt"><a href="chamado.html?id=${x.id}" data-test="link-chamado">${esc(x.titulo) || '<i style="color:#5b5f78">(sem título)</i>'}</a>${chip}</div></td>
        <td><span class="cli"><span class="cli-i" style="background:${bg};color:${cor}">${esc(iniciais(x.cliente))}</span>${esc(x.cliente)}</span></td>
        <td><span class="stp" data-test="status" style="--c:${COR_ST[x.status] || '#a78bfa'}"><i></i>${x.status}</span></td><td class="quando" title="${dataBR(x.criadoEm)}">${relativo(x.criadoEm)}</td></tr>`; }).join('')
      : '<tr><td colspan="5" class="vazio" data-test="lista-vazia">Nenhum chamado encontrado</td></tr>';
    if (f && l.some((x) => x.status !== f)) _pv('lista');
    if (b && b !== b.trim() && _c('busca')) _pv('busca');
    if (f === 'Fechado' && !l.length && _c('fechado') && innerWidth <= 480) _pv('fechado');
    $$('#linhas tr[data-href]').forEach((tr) => { tr.onclick = (ev) => { if (!ev.target.closest('a')) location.href = tr.dataset.href; }; });
  };
  $$('.chips .chip').forEach((c) => { c.onclick = () => { $('#filtro').value = c.dataset.st; pinta(); }; });
  if (usaApi()) {
    let pedido = 0, tm = null;
    const desenha = (l) => { const f = $('#filtro').value; const filtra = l.filter((x) => !f || x.status === f); const ids = new Set(filtra.map((x) => x.id)); const todos2 = dados().chamados.filter((x) => ids.has(x.id)).sort((a, c) => c.id - a.id);
      $('#linhas').innerHTML = todos2.length ? todos2.map((x) => { const [bg, cor] = corCliente(x.cliente);
        return `<tr data-test="linha-chamado" data-href="chamado.html?id=${x.id}"><td class="num">#${x.id}</td><td><div class="tt"><a href="chamado.html?id=${x.id}" data-test="link-chamado">${esc(x.titulo) || '<i style="color:#5b5f78">(sem título)</i>'}</a>${x.criadoPor === 'Você' ? '<span class="por-voce">criado por você</span>' : ''}</div></td>
        <td><span class="cli"><span class="cli-i" style="background:${bg};color:${cor}">${esc(iniciais(x.cliente))}</span>${esc(x.cliente)}</span></td>
        <td><span class="stp" data-test="status" style="--c:${COR_ST[x.status] || '#a78bfa'}"><i></i>${x.status}</span></td><td class="quando" title="${dataBR(x.criadoEm)}">${relativo(x.criadoEm)}</td></tr>`; }).join('')
        : '<tr><td colspan="5" class="vazio" data-test="lista-vazia">Nenhum chamado encontrado</td></tr>';
      $$('#linhas tr[data-href]').forEach((tr) => { tr.onclick = (ev) => { if (!ev.target.closest('a')) location.href = tr.dataset.href; }; }); };
    const busca = async () => {
      const n = ++pedido, v = $('#busca').value.trim();
      if (!v) return pinta();
      $('#linhas').innerHTML = '<tr><td colspan="5" class="vazio" data-test="carregando">Carregando…</td></tr>';
      // Sprint 17: a busca corta em 30 posições, e um emoji ocupa duas: pode sobrar meio emoji
      const termo = BUG.buscaEmoji ? v.slice(0, 30) : Array.from(v).slice(0, 30).join('');
      const url = 'api/chamados?busca=' + encodeURIComponent(termo);
      await swPronto(); const r = await fetch(url); const l = await r.json();
      if (n === pedido) desenha(r.ok ? l : []);
    };
    $('#busca').oninput = () => { clearTimeout(tm); tm = setTimeout(busca, 350); }; $('#filtro').onchange = () => ($('#busca').value.trim() ? busca() : pinta()); pinta();
    return;
  }
  $('#busca').oninput = pinta; $('#filtro').onchange = pinta; pinta();
};

PAGINAS['novo-chamado'] = () => {
  casca('chamados', topo('Novo chamado', 'Registre uma nova solicitação de atendimento', '<a href="chamados.html">Chamados</a> / Novo') + `<div class="nc-grade">
    <form class="fcard" id="f" novalidate>
      <div class="campo"><label for="titulo">Título <i>*</i><span class="contador" data-test="contador-titulo" id="cont">0/100</span></label><input class="in" id="titulo" maxlength="100" data-test="titulo" placeholder="Resuma o problema em uma frase"></div>
      <div class="campo"><label for="descricao">Descrição <i>*</i></label><textarea class="in" id="descricao" data-test="descricao" placeholder="Descreva o problema…"></textarea></div>
      <div class="campo"><label for="cliente">Cliente</label><select class="in" id="cliente" data-test="cliente">${CLIENTES.map((c) => `<option>${c.nome}</option>`).join('')}</select></div>
      <div class="campo"><label>Anexo <small>(opcional · PDF, PNG ou JPG até 5 MB)</small></label>
        <label class="arquivo" for="anexo"><input type="file" id="anexo" data-test="anexo" accept=".pdf,.png,.jpg,.jpeg"><span class="btn sec peq">Escolher arquivo</span><span class="nome" id="nomeArq" data-test="nome-anexo">Nenhum arquivo escolhido</span><button type="button" class="icone" id="tiraArq" data-test="remover-anexo" hidden>Remover</button></label></div>
      <div class="fbtns"><a class="btn sec" href="chamados.html" data-test="cancelar">Cancelar</a><button class="btn" data-test="criar-chamado">Criar chamado</button></div>
    </form><aside class="nc-lado"><div class="nc-k">${ico('card', 'ic')}O QUE O FD-101 PEDE</div><ol>${(dados().cards.find((x) => x.id === 'FD-101') || { criterios: [] }).criterios.map((t) => `<li>${esc(t)}</li>`).join('')}</ol><a href="card.html?id=FD-101&aba=plano">Abrir o plano de testes ${ico('seta', 'ic')}</a></aside></div>`);
  let arquivo = null;
  if (VERSAO >= 17) {
    const rs = LS.get(RASCUNHO, null);
    if (rs && (rs.titulo || rs.descricao)) {
      $('#titulo').value = rs.titulo || ''; $('#descricao').value = rs.descricao || '';
      const d = dados(); if (d.meuRascunho !== (rs.titulo || '') + '|' + (rs.descricao || '')) { d.viuRascunhoAlheio = true; salvar(); }
      setTimeout(() => toast('Rascunho recuperado'), 50);
    }
    const guarda = () => { const v = { titulo: $('#titulo').value, descricao: $('#descricao').value }; LS.set(RASCUNHO, v); const d = dados(); d.meuRascunho = v.titulo + '|' + v.descricao; salvar(); };
    $('#titulo').addEventListener('input', guarda); $('#descricao').addEventListener('input', guarda);
  }
  if (_c('t80') && innerWidth <= 480) $('#titulo').maxLength = 80;
  $('#titulo').oninput = () => { $('#cont').textContent = $('#titulo').value.length + '/100'; if ($('#titulo').maxLength === 80 && $('#titulo').value.length >= 80) _pv('t80'); };
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
  $('#tiraArq').onclick = (ev) => { ev.preventDefault(); if (!(_c('anexo') && innerWidth <= 480)) arquivo = null; else arquivo.tirado = 1; $('#anexo').value = ''; $('#nomeArq').textContent = 'Nenhum arquivo escolhido'; $('#tiraArq').hidden = true; };
  $('#f').onsubmit = (ev) => {
    ev.preventDefault(); limpaErros();
    const t = $('#titulo').value, ds = $('#descricao').value;
    let ok = true;
    if (BUG.tituloSoEspacos ? t.length === 0 : t.trim().length === 0) { erroCampo('titulo', 'Título é obrigatório'); ok = false; }
    else if (BUG.titulo100 && t.trim().length >= 100) { erroCampo('titulo', 'Título deve ter até 100 caracteres'); ok = false; }
    if (ds.trim().length === 0) { erroCampo('descricao', 'Descrição é obrigatória'); ok = false; }
    if (!ok) return;
    if (usaApi()) {
      const btn = $('[data-test=criar-chamado]');
      if (!BUG.duplicado) btn.disabled = true;
      swPronto().then(() => fetch('api/chamados', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ titulo: t, descricao: ds, cliente: $('#cliente').value, anexo: arquivo }) }))
        .then((r) => r.json().then((j) => ({ ok: r.ok, j })))
        .then(({ ok: certo, j }) => {
          if (!certo) { btn.disabled = false; return toast(j.erro || 'Não deu pra criar o chamado', true); }
          LS.del(RASCUNHO);
          // a partir da Sprint 17 a tela fica no formulário (assim a aba Rede não perde o pedido) e já deixa criar o próximo
          toast(`Chamado #${j.id} criado com sucesso`); $('#titulo').value = ''; $('#descricao').value = ''; $('#cont').textContent = '0/100'; arquivo = null; $('#nomeArq').textContent = 'Nenhum arquivo escolhido'; $('#tiraArq').hidden = true; btn.disabled = false;
        })
        .catch(() => { btn.disabled = false; toast('Sem conexão. Tente de novo', true); });
      return;
    }
    const d = dados(), id = d.proximoChamado++;
    if (arquivo && arquivo.tirado) { _pv('anexo'); delete arquivo.tirado; }
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
    <div class="sec"><div class="k">Anexo</div>${x.anexo ? `<div class="v" data-test="chamado-anexo">${ico('clipe', 'ic')}${esc(x.anexo.nome)} <span style="color:var(--mut)">(${tamanho(x.anexo.tamanho)})</span></div>` : '<div class="v nada" data-test="chamado-anexo">Nenhum anexo</div>'}</div>
    <div class="sec"><div class="k">Mudar status</div><div style="display:flex;gap:10px;flex-wrap:wrap"><select class="in" id="novoSt" data-test="mudar-status" style="max-width:240px">${STATUS.map((s) => `<option ${s === x.status ? 'selected' : ''}>${s}</option>`).join('')}</select><button class="btn" id="salvaSt" data-test="salvar-status">Salvar status</button></div></div>
    <div class="sec"><div class="k">Histórico</div><div class="hist" data-test="historico">${x.historico.map((h) => `<div>${dataBR(h.quando)} · ${esc(h.tx)}</div>`).join('')}</div></div>`);
  $('#salvaSt').onclick = () => {
    const s = $('#novoSt').value; if (s === x.status) return toast('O chamado já está com esse status', true);
    x.historico.push({ quando: agora(), tx: `Status mudou de ${x.status} para ${s}` }); x.status = s; salvar();
    recado('Status atualizado para ' + s); location.reload();
  };
};

// ---------- quadro (estilo ferramenta de tarefas: status coloridos, etiquetas, prioridade, progresso) ----------
const COR_COLUNA = { afazer: '#6b6e86', dev: '#60a5fa', qa: '#a78bfa', teste: '#f59e0b', concluido: '#22c55e' };
const PRIOS = ['Baixa', 'Normal', 'Alta', 'Urgente'];
const prioDe = (c) => ({ 'Média': 'Normal', 'Crítica': 'Urgente' }[c.prioridade || c.severidade] || c.prioridade || c.severidade || 'Normal');
const flag = (p) => `<span class="flag f-${p.toLowerCase()}"><svg viewBox="0 0 24 24"><path d="M5 21V4h11l-1.5 4L16 12H5"/></svg>${p}</span>`;
const etiqueta = (c) => c.tipo === 'bug' ? '<span class="etq etq-bug">bug</span>' + (c.regressao ? '<span class="etq etq-reg" data-test="etiqueta-regressao">regressão</span>' : '') + (c.reaberto ? '<span class="etq etq-rea" data-test="etiqueta-reaberto">reaberto</span>' : '') : c.tipo === 'melhoria' ? '<span class="etq etq-mel">melhoria</span>' : '<span class="etq etq-story">história</span>';
const nomeColuna = (k) => COLUNAS.find((x) => x[0] === k)[1];
function cardFace(c) {
  const d = dados(), plano = d.planos[c.id], tot = c.criterios.length, ok = critOk(d, c).length;
  return `<a class="tk ${c.resp === 'voce' ? 'meu' : 'travado'} ${c.tipo === 'bug' ? 'e-bug' : ''}" href="card.html?id=${c.id}" draggable="${c.resp === 'voce'}" ${c.resp === 'voce' ? '' : `title="Card de ${PESSOAS[c.resp].nome}: só quem é responsável move"`} data-id="${c.id}" data-test="card-${c.id}">
    <div class="tk-etq">${etiqueta(c)}<span class="id">${c.id}</span></div><div class="t">${esc(c.titulo)}</div>
    <div class="tk-meta">${flag(prioDe(c))}${plano && plano.length ? `<span class="mini" title="Cenários no plano de testes">${ico('plano')}${plano.length}</span>` : ''}${c.comentarios.length ? `<span class="mini" title="Comentários">${ico('chat')}${c.comentarios.length}</span>` : ''}<span class="tk-av">${avatar(c.resp)}</span></div>
    ${tot ? `<div class="tk-prog" title="Critérios de aceite validados"><i style="width:${ok / tot * 100}%"></i></div><div class="tk-prog-n">${ok}/${tot} critérios</div>` : ''}</a>`;
}
PAGINAS.quadro = () => {
  const anda = [['rafael_anda', 0, ''], ['lucas_anda', -7.6, ''], ['beatriz_anda', -15.2, ''], ['vinicius_frente', -22.8, ''], ['gabriela_anda', -30.4, '']];
  casca('quadro', topo(`Sprint ${VERSAO}`, 'Objetivo: melhorar o fluxo de criar chamado') + `<div class="cols">${COLUNAS.map(([k, n]) => `<section class="col ${k === 'teste' ? 'destaque' : ''}" data-col="${k}" data-test="coluna-${k}" style="--cor:${COR_COLUNA[k]}">
      <div class="h"><h3>${n}</h3><span class="cnt" data-test="contagem-${k}"></span>${k === 'afazer' ? '<button class="mais" data-test="nova-tarefa" title="Nova tarefa" aria-label="Nova tarefa">+</button>' : ''}</div>
      <div class="cards"></div>${k === 'afazer' ? '<button class="add-tarefa" data-test="adicionar-tarefa">+ Adicionar tarefa</button>' : ''}</section>`).join('')}</div>
    <p class="dica" style="margin-top:12px">Você move os seus cards arrastando, ou pelo próprio card. Os cards dos outros ficam com eles.</p>
    <div class="desfile" aria-hidden="true"><div class="chao"></div>${anda.map(([v, atraso, cls]) => `<div class="anda ${cls}" style="animation-delay:${atraso}s"><video src="img/anim/${v}.webm?v=1794479423" poster="img/anim/${v}.png?v=1794479423" autoplay muted loop playsinline></video></div>`).join('')}</div>`);
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
    ${ctx ? `<p class="liga" data-test="bug-cenario">Ligado ao cenário ${ctx.n} do plano: <b>${esc(ctx.nome)}</b></p>` : ''}
    <div class="so-bug"><div class="campo"><label for="tPassos">Passos para reproduzir <i>*</i></label><textarea class="in" id="tPassos" data-test="bug-passos" placeholder="1. …&#10;2. …&#10;3. …"></textarea></div>
      <div class="linha2"><div class="campo"><label for="tEsp">Resultado esperado <i>*</i></label><input class="in" id="tEsp" data-test="bug-esperado"></div><div class="campo"><label for="tObt">Resultado obtido <i>*</i></label><input class="in" id="tObt" data-test="bug-obtido"></div></div>
      ${VERSAO >= 17 ? `<div class="campo"><label for="tTec">Console e Rede <small>(opcional · erro do Console, pedido e resposta da Rede, chave do armazenamento)</small></label><textarea class="in" id="tTec" data-test="bug-tecnico" placeholder="Ex.: GET api/chamados?busca=... respondeu [] · URIError: URI malformed"></textarea></div>` : ''}
      <div class="campo"><label for="tEvid">Evidência <i>*</i> <small>(print ou vídeo do que aconteceu)</small></label><label class="arquivo ${ctx && ctx.evid ? 'tem' : ''}" for="tEvid" id="tEvidBox"><input type="file" id="tEvid" data-test="bug-evidencia"><span class="btn sec peq">${ctx && ctx.evid ? 'Trocar arquivo' : 'Escolher arquivo'}</span><span class="nome" id="nomeEv" data-test="bug-evidencia-nome">${ctx && ctx.evid ? `${esc(ctx.evid)} <em>· veio do cenário ${ctx.n}</em>` : 'Nenhum arquivo escolhido'}</span></label></div>
      ${VERSAO >= 15 ? `<label class="cr reg-ck" data-test="bug-regressao"><input type="checkbox" id="tReg"> É regressão: funcionava antes e parou</label>
      <div class="linha2" id="tRegC" hidden><div class="campo"><label for="tFun">Funcionava em</label><select class="in" id="tFun" data-test="bug-funcionava">${[13, 14, 15].filter((v) => v < VERSAO).map((v) => `<option value="${v}" ${v === VERSAO - 1 ? 'selected' : ''}>Sprint ${v}</option>`).join('')}</select></div><div class="campo"><label for="tQue">Quebrou em</label><select class="in" id="tQue" data-test="bug-quebrou"><option value="${VERSAO}">Sprint ${VERSAO}</option></select></div></div>` : ''}</div>
    <div class="so-mel" hidden><div class="campo"><label for="tDesc">Descrição <i>*</i></label><textarea class="in" id="tDesc" data-test="melhoria-descricao" placeholder="O que poderia ser melhor, e por quê"></textarea></div></div>
    <p class="dica" id="tDest">O bug vai pra coluna A fazer, com a Gabriela.</p>
    <div class="fbtns"><button type="button" class="btn sec" data-fecha>Cancelar</button><button class="btn" data-test="criar-tarefa">Criar tarefa</button></div></form>`;
  document.body.appendChild(o);
  const fecha = () => o.remove();
  $$('[data-fecha]', o).forEach((b) => { b.onclick = fecha; });
  o.onclick = (e) => { if (e.target === o) fecha(); };
  const tipo = () => $('input[name=tipo]:checked', o).value;
  $$('input[name=tipo]', o).forEach((r) => { r.onchange = () => { const bug = tipo() === 'bug'; $('.so-bug', o).hidden = !bug; $('.so-mel', o).hidden = bug; $('#tDest').textContent = bug ? 'O bug vai pra coluna A fazer, com a Gabriela.' : 'A melhoria vai pra coluna A fazer, com o Rafael, que decide se entra na sprint.'; limpaErros(); }; });
  $('#tEvid').onchange = () => { const f = $('#tEvid').files[0]; if (f) $('#nomeEv').textContent = f.name; else if (!(ctx && ctx.evid)) $('#nomeEv').textContent = 'Nenhum arquivo escolhido'; };
  if ($('#tReg')) $('#tReg').onchange = () => { $('#tRegC').hidden = !$('#tReg').checked; if ($('#tReg').checked && $('#tPrio').value === 'Normal') $('#tPrio').value = 'Alta'; };
  $('#tTitulo').focus();
  $('#fT').onsubmit = (ev) => {
    ev.preventDefault(); limpaErros(); let ok = true; const v = (i) => $('#' + i).value.trim(), bug = tipo() === 'bug';
    const obrig = [['tTitulo', 'Dê um título pra tarefa']].concat(bug ? [['tPassos', 'Escreva os passos pra reproduzir'], ['tEsp', 'Escreva o resultado esperado'], ['tObt', 'Escreva o resultado obtido']] : [['tDesc', 'Descreva a melhoria']]);
    obrig.forEach(([i, m]) => { if (!(i === 'tTitulo' && bug && _c('bugtit') ? $('#' + i).value : v(i))) { erroCampo(i, m); ok = false; } });
    if (bug && !$('#tEvid').files[0] && !(ctx && ctx.evid)) { erroCampo('tEvidBox', 'Anexe o print ou o vídeo: sem evidência, o dev não vê o que você viu'); ok = false; }
    if (!ok) return;
    let id;
    if (bug) {
      id = 'BUG-' + String(d.proximoBug++).padStart(2, '0'); const f = $('#tEvid').files[0];
      if (!v('tTitulo')) _pv('bugtit');
      d.cards.push({ id, titulo: v('tTitulo'), coluna: 'afazer', resp: 'gabriela', tipo: 'bug', prioridade: v('tPrio'), relacionado: v('tCard'), cenario: ctx ? ctx.nome : '', passos: v('tPassos'), esperado: v('tEsp'), obtido: v('tObt'), evidencia: f ? f.name : (ctx && ctx.evid) || '', ...($('#tReg') && $('#tReg').checked ? { regressao: true, funcionava: +$('#tFun').value, quebrou: +$('#tQue').value } : {}), ...($('#tTec') && $('#tTec').value.trim() ? { tecnico: $('#tTec').value.trim() } : {}), criterios: [], ok: [], comentarios: [], criadoEm: agora() });
      d.chat.bugs.push({ de: 'voce', tx: `Abri o ${id}: ${v('tTitulo')}`, quando: agora() });
    } else {
      d.proximoMelhoria = d.proximoMelhoria || 1; id = 'MEL-' + d.proximoMelhoria++;
      d.cards.push({ id, titulo: v('tTitulo'), coluna: 'afazer', resp: 'rafael', tipo: 'melhoria', prioridade: v('tPrio'), relacionado: v('tCard'), descricao: v('tDesc'), criterios: [], ok: [], comentarios: [], criadoEm: agora() });
    }
    if (bug && ctx) { const l = d.planos[ctx.card] || []; if (l[ctx.i]) l[ctx.i].bug = id; }
    salvar(); fecha(); toast(`${id} criado${bug ? ' e enviado pra Gabriela' : ''}`); if (depois) depois(id); confereMissoes();
  };
}

// ---------- reteste do bug ----------
function retesteHtml(c) {
  const ult = [...c.comentarios].reverse().find((m) => m.de === 'gabriela');
  const hist = (c.retestes || []).length ? `<div class="rt-h" data-test="reteste-historico">${c.retestes.map((r) => `<div class="rt-l ${r.res}"><b>${r.res === 'passou' ? '✓ Passou' : '✕ Falhou'}</b><span>Sprint ${r.versao} · ${dataBR(r.quando)}</span><span class="rt-ev">${ico('clipe')}${esc(r.evid)}</span>${r.com ? `<span class="rt-c">${esc(r.com)}</span>` : ''}</div>`).join('')}</div>` : '';
  let corpo;
  if (c.coluna === 'qa') corpo = `${ult ? fala('gabriela', 'Gabriela · Dev', esc(ult.tx)) : ''}<p class="dica">Refaça os passos abaixo, do mesmo jeito do report, e registre o resultado com o print.</p><button class="btn" id="abreRt" data-test="retestar">Retestar</button>
    <form id="fRt" class="rt-f" hidden novalidate><div class="linha2"><div class="campo"><label for="rtV">Versão em que você testou</label><select class="in" id="rtV" data-test="reteste-versao">${[14, 15, 16].filter((v) => v <= VERSAO).map((v) => `<option value="${v}" ${v === VERSAO ? 'selected' : ''}>Sprint ${v}</option>`).join('')}</select></div>
      <div class="campo"><label>Resultado</label><div class="seg" id="rtSeg"><label data-test="reteste-passou"><input type="radio" name="rtR" value="passou"><span>Passou</span></label><label data-test="reteste-falhou"><input type="radio" name="rtR" value="falhou"><span>Falhou</span></label></div></div></div>
      <div class="campo"><label for="rtE">Evidência <i>*</i> <small>(o print do reteste)</small></label><label class="arquivo" for="rtE" id="rtBox"><input type="file" id="rtE" data-test="reteste-evidencia"><span class="btn sec peq">Escolher arquivo</span><span class="nome" id="rtN">Nenhum arquivo escolhido</span></label></div>
      <div class="campo"><label for="rtC">Comentário <small>(opcional)</small></label><input class="in" id="rtC" data-test="reteste-comentario" placeholder="Ex.: testei também com 1 espaço e com espaço antes do texto"></div>
      <div class="fbtns"><button type="button" class="btn sec" id="rtX">Cancelar</button><button class="btn" data-test="salvar-reteste">Registrar reteste</button></div></form>`;
  else if (c.coluna === 'concluido') corpo = '<p class="dica" data-test="bug-fechado">Bug fechado depois do reteste.</p>';
  else corpo = `<p class="dica">${c.reaberto ? 'Reaberto: voltou pra Gabriela com o print do reteste.' : 'Esperando a correção da Gabriela.'}</p>`;
  return `<div class="sec rt" data-test="reteste"><div class="k">Reteste</div>${corpo}${hist}</div>`;
}
function ligaReteste(c) {
  if (!$('#abreRt')) return;
  $('#abreRt').onclick = () => { $('#fRt').hidden = false; $('#abreRt').hidden = true; };
  $('#rtX').onclick = () => { $('#fRt').hidden = true; $('#abreRt').hidden = false; limpaErros(); };
  $('#rtE').onchange = () => { const f = $('#rtE').files[0]; $('#rtN').textContent = f ? f.name : 'Nenhum arquivo escolhido'; };
  $('#fRt').onsubmit = (ev) => {
    ev.preventDefault(); limpaErros(); let ok = true;
    const v = +$('#rtV').value, r = ($('input[name=rtR]:checked') || {}).value, f = $('#rtE').files[0];
    if (c.corrigidoEm && v < c.corrigidoEm) { erroCampo('rtV', `A correção entrou na Sprint ${c.corrigidoEm}. Retestar na ${v} não prova nada.`); ok = false; }
    if (!r) { erroCampo('rtSeg', 'Diga se passou ou falhou'); ok = false; }
    if (!f) { erroCampo('rtBox', 'Anexe o print do reteste: ele fecha o bug do mesmo jeito que o print do erro abriu'); ok = false; }
    if (!ok) return;
    const d = dados();
    c.retestes = c.retestes || []; c.retestes.push({ quando: agora(), versao: v, res: r, evid: f.name, com: $('#rtC').value.trim() });
    c.comentarios.push({ tx: `Reteste na Sprint ${v}: ${r}. Evidência: ${f.name}${$('#rtC').value.trim() ? '. ' + $('#rtC').value.trim() : ''}`, quando: agora() });
    if (r === 'passou') { c.coluna = 'concluido'; c.reaberto = false; c.comentarios.push({ de: 'gabriela', tx: 'Valeu pelo reteste! 🙌', quando: agora() }); }
    else { c.coluna = 'afazer'; c.reaberto = true; c.comentarios.push({ de: 'gabriela', tx: 'Vixe. Vou olhar de novo, obrigada pelo print.', quando: agora() }); d.chat.bugs.push({ de: 'voce', tx: `Reabri o ${c.id}: o reteste na Sprint ${v} falhou.`, quando: agora() }); }
    salvar(); recado(r === 'passou' ? `${c.id} fechado` : `${c.id} reaberto e devolvido pra Gabriela`); confereMissoes(); setTimeout(() => location.reload(), 300);
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
  casca(c.id === 'FD-101' ? 'card:' + aba : 'quadro', `<div class="topo"><div><div class="crumb"><a href="quadro.html">Quadro</a> / Sprint ${VERSAO}</div>
      <h2 data-test="titulo-pagina">${etiqueta(c)} <span style="color:var(--acc2)">${c.id}</span> · <span data-test="card-titulo" style="color:var(--txt)">${esc(c.titulo)}</span></h2></div></div>
    <div class="meta">
      <div class="mi"><div class="k">Status</div><div class="v">${c.resp === 'voce' ? `<select class="in" id="mover" data-test="mover-card" style="height:32px;font-size:14px;min-width:190px">${COLUNAS.filter(([k]) => k === c.coluna || (MOVES_QA[c.coluna] || []).includes(k)).map(([k, n]) => `<option value="${k}" ${k === c.coluna ? 'selected' : ''}>${n}</option>`).join('')}</select>` : `<span class="pill-st" style="--cor:${COR_COLUNA[c.coluna]}" data-test="coluna-card"><i></i>${c.tipo === 'bug' && c.coluna === 'concluido' ? 'Fechado' : nomeColuna(c.coluna)}</span>`}</div></div>
      <div class="mi"><div class="k">Responsável</div><div class="v">${avatar(c.resp)}${PESSOAS[c.resp].nome}</div></div>
      <div class="mi"><div class="k">Prioridade</div><div class="v" data-test="card-prioridade">${flag(prioDe(c))}</div></div>
      ${tot ? `<div class="mi"><div class="k">Critérios validados</div><div class="v" id="critN">${critOk(d, c).length}/${tot}</div></div>` : ''}</div>
    <nav class="abas">${abas.map(([k, n]) => `<button class="${k === aba ? 'on' : ''}" data-aba="${k}" data-test="aba-${k}">${n}<span class="n" id="n-${k}"></span></button>`).join('')}</nav>
    <div id="abaConteudo"></div>`);
  const contagens = () => { if ($('#n-plano')) $('#n-plano').textContent = d.planos[c.id].length || ''; if ($('#n-gherkin')) $('#n-gherkin').textContent = revisaGherkin(gherkinDe(dados(), c.id)).cenarios.length || ''; $('#n-comentarios').textContent = c.comentarios.length || ''; };
  const campo = (k, v) => `<div class="sec"><div class="k">${k}</div>${v ? `<div class="v">${esc(v)}</div>` : '<div class="v nada">Nada informado.</div>'}</div>`;
  const ST_CRIT = { ok: ['Validado', 'ok'], falhou: ['Falhou', 'falhou'], testar: ['A testar', 'testar'], nada: ['Sem cenário', 'nada'] };
  const critHtml = () => {
    if (!tot) return '<div class="sec"><div class="k">Critérios de aceite</div><div class="v nada">Nenhum critério definido.</div></div>';
    const es = critEstado(dados(), c);
    if (!temPlano) return `<div class="sec" id="sCrit"><div class="k">Critérios de aceite</div>${es.map((e, i) => `<label class="cr"><input type="checkbox" data-i="${i}" data-test="criterio" ${e.st === 'ok' ? 'checked' : ''}>${esc(e.t)}</label>`).join('')}</div>`;
    return `<div class="sec" id="sCrit"><div class="k">Critérios de aceite <span class="k2">o plano de testes valida cada um</span></div>${es.map((e, i) => `<div class="crit c-${ST_CRIT[e.st][1]}" data-test="criterio-linha"><span class="ci">${e.st === 'ok' ? '✓' : e.st === 'falhou' ? '✕' : i + 1}</span><div class="ct"><div>${esc(e.t)}</div><div class="cc">${e.cen.length ? e.cen.map((j2) => `<button type="button" class="chipc" data-cen="${j2}">Cenário ${j2 + 1}</button>`).join('') : '<span class="semc">Nenhum cenário cobre essa regra ainda</span>'}${(e.bugs || []).map((b) => `<a class="chipb" href="card.html?id=${b}">${ico('bug')}${b}</a>`).join('')}</div></div><span class="cst" data-test="criterio-status">${ST_CRIT[e.st][0]}</span></div>`).join('')}</div>`;
  };
  const mostra = (k) => {
    aba = k; $$('.abas button').forEach((b) => b.classList.toggle('on', b.dataset.aba === k));
    if (c.id === 'FD-101') $$('[data-sub]').forEach((a) => a.classList.toggle('on', a.dataset.sub === k));
    history.replaceState(null, '', `card.html?id=${c.id}${k === 'detalhes' ? '' : '&aba=' + k}`);
    const A = $('#abaConteudo');
    if (k === 'detalhes') {
      A.innerHTML = c.tipo === 'bug'
        ? retesteHtml(c) + `<div class="sec"><div class="k">Card relacionado</div><div class="v">${c.relacionado ? `<a href="card.html?id=${c.relacionado}">${c.relacionado}</a>` : '—'}</div></div>` + campo('Passos para reproduzir', c.passos) + campo('Resultado esperado', c.esperado) + campo('Resultado obtido', c.obtido) + campo('Evidência', c.evidencia || '') + (c.regressao ? campo('Funcionava em', c.funcionava ? 'Sprint ' + c.funcionava : '') + campo('Quebrou em', c.quebrou ? 'Sprint ' + c.quebrou : '') : '')
        : campo('Descrição', c.descricao) + (c.tipo === 'melhoria' ? '' : critHtml());
      if (c.tipo !== 'bug') {
        const pl = d.planos[c.id] || [], ex = pl.filter((x) => x.exec === 'passou' || x.exec === 'falhou').length, fal = pl.filter((x) => x.exec === 'falhou' || (_c('falha') && x.jaFalhou)).length, _f = pl.some((x) => x.exec !== 'falhou' && x.jaFalhou) && _c('falha') && _pv('falha'), bugs = pl.filter((x) => x.bug).length;
        const linha = (n, l, cor) => `<div class="rs-l"><span>${l}</span><b${cor ? ` style="color:${cor}"` : ''}>${n}</b></div>`;
        const pessoa = (p, papel) => `<div class="rs-p">${avatar(p)}<div><b>${PESSOAS[p].nome}</b><span>${papel}</span></div></div>`;
        A.innerHTML = `<div class="det"><div class="det-e">${A.innerHTML}</div><aside class="rs" data-test="resumo-card">
          <div class="rs-k">Pessoas do card</div>${pessoa('rafael', 'PO · escreveu a história')}${pessoa(c.resp === 'voce' ? 'gabriela' : c.resp, 'Dev · fez a entrega')}${pessoa('voce', 'QA · está testando')}
          ${temPlano ? `<div class="rs-k" style="margin-top:18px">Andamento do teste</div>${linha(pl.length, 'Cenários no plano')}${linha(`${ex}/${pl.length}`, 'Executados')}${linha(fal, 'Falharam', fal ? '#fca5a5' : '')}${linha(bugs, 'Bugs ligados', bugs ? '#c4b5fd' : '')}<div class="rs-bar"><i style="width:${pl.length ? ex / pl.length * 100 : 0}%"></i></div>
          <button class="btn cheio" data-test="abrir-plano" id="abrePlano" style="margin-top:16px">Abrir plano de testes</button>` : ''}</aside></div>`;
      }
      $$('[data-test=criterio]').forEach((k2) => { k2.onchange = () => { const i = +k2.dataset.i; c.ok = k2.checked ? [...new Set([...c.ok, i])] : c.ok.filter((x) => x !== i); salvar(); if ($('#critN')) $('#critN').textContent = `${c.ok.length}/${tot}`; }; });
      $$('[data-cen]').forEach((b) => { b.onclick = () => mostra('plano'); });
      if (c.tipo === 'bug') ligaReteste(c);
      if ($('#abrePlano')) $('#abrePlano').onclick = () => mostra('plano');
    } else if (k === 'plano') {
      montaPlano(A, c);
    } else if (k === 'gherkin') {
      montaGherkin(A, c, contagens);
    } else {
      A.innerHTML = `<div class="sec"><div id="coms">${c.comentarios.map((m) => `<div class="coment">${avatar(m.de || 'voce')}<div class="bx"><b>${m.de ? PESSOAS[m.de].nome : 'Você'}</b><small>${dataBR(m.quando)}</small><div>${esc(m.tx)}</div></div></div>`).join('') || '<div class="v nada" style="font-size:15px">Nenhum comentário ainda.</div>'}</div>
        <div style="display:flex;gap:10px;margin-top:12px"><input class="in" id="com" placeholder="Escreva um comentário…" data-test="comentario"><button class="btn" id="enviaCom" data-test="enviar-comentario">Comentar</button></div></div>`;
      $('#enviaCom').onclick = () => { const t = _c('com') ? $('#com').value.replace(/^\n+|\n+$/g, '') : $('#com').value.trim(); if (!t) return; if (!t.trim()) _pv('com'); c.comentarios.push({ tx: t, quando: agora() }); salvar(); contagens(); mostra('comentarios'); };
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
    <aside><div class="rafa"><div class="rafa-b"><div class="bk">RAFAEL · PO</div><div class="bt">Escreve do jeito que eu leio: <b>Dado</b> o contexto, <b>Quando</b> a ação, <b>Então</b> o que eu vejo.</div></div><video src="img/anim/rafael_fala.webm?v=1794479423" poster="img/anim/rafael_fala.png?v=1794479423" autoplay muted loop playsinline aria-hidden="true"></video></div><div class="cov" id="gkRev" data-test="revisao-gherkin"></div></aside></div>`;
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

// ---------- arquivos de teste: abrem de verdade e têm o tamanho exato ----------
function arquivoTeste(nome, b) {
  const ext = extensao(nome);
  if (ext === 'pdf') {
    const txt = (y, t, s) => `BT /F1 ${t} Tf 72 ${y} Td (${s.replace(/[()\\]/g, '')}) Tj ET\n`;
    const cont = txt(740, 30, 'FlowDesk') + txt(700, 16, 'Arquivo de teste: ' + nome) + txt(674, 16, 'Tamanho: ' + b + ' bytes') + txt(630, 12, 'Gerado pelo FlowDesk para testar o anexo do chamado.');
    const corpo = ['<< /Type /Catalog /Pages 2 0 R >>', '<< /Type /Pages /Kids [3 0 R] /Count 1 >>', '<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>', `<< /Length ${cont.length} >>\nstream\n${cont}endstream`, '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>'];
    const monta = (P) => {
      let s = '%PDF-1.4\n'; const pos = [];
      corpo.forEach((o, i) => { pos.push(s.length); s += `${i + 1} 0 obj\n${o}\nendobj\n`; });
      pos.push(s.length); const ini = s + `6 0 obj\n<< /Length ${P} >>\nstream\n`, fimObj = '\nendstream\nendobj\n';
      const xr = ini.length + P + fimObj.length;
      const fim = fimObj + `xref\n0 7\n0000000000 65535 f \n${pos.map((p) => String(p).padStart(10, '0') + ' 00000 n \n').join('')}trailer\n<< /Size 7 /Root 1 0 R >>\nstartxref\n${xr}\n%%EOF\n`;
      return [ini, fim];
    };
    let P = Math.max(0, b - 600), ini, fim;
    for (let k = 0; k < 6; k++) { [ini, fim] = monta(P); const tot = ini.length + P + fim.length; if (tot === b) break; P = Math.max(0, P + b - tot); }
    return new Blob([ini, new Uint8Array(P).fill(32), fim], { type: 'application/pdf' });
  }
  if (ext === 'png' || ext === 'jpg') {
    const cv = document.createElement('canvas'); cv.width = 480; cv.height = 270; const g = cv.getContext('2d');
    g.fillStyle = '#17132b'; g.fillRect(0, 0, 480, 270); g.fillStyle = '#8b5cf6'; g.fillRect(0, 0, 480, 8);
    g.fillStyle = '#fff'; g.font = 'bold 34px sans-serif'; g.fillText('FlowDesk', 28, 80); g.font = '18px sans-serif'; g.fillStyle = '#c4b5fd'; g.fillText('Arquivo de teste', 28, 122); g.fillStyle = '#e5e7eb'; g.fillText(nome + ' · ' + tamanho(b), 28, 152);
    const bin = atob(cv.toDataURL(ext === 'png' ? 'image/png' : 'image/jpeg', 0.85).split(',')[1]), base = Uint8Array.from(bin, (ch) => ch.charCodeAt(0));
    if (base.length + 12 > b) return new Blob([base], { type: ext === 'png' ? 'image/png' : 'image/jpeg' });
    if (ext === 'png') {  // enche com um bloco extra (ignorado por quem abre) antes do IEND
      const L = b - base.length - 12, bloco = new Uint8Array(L + 12), dv = new DataView(bloco.buffer);
      dv.setUint32(0, L); bloco.set([102, 100, 80, 100], 4);
      let c = -1; for (let i = 4; i < L + 8; i++) { c ^= bloco[i]; for (let k = 0; k < 8; k++) c = c & 1 ? (c >>> 1) ^ 0xEDB88320 : c >>> 1; }
      dv.setUint32(L + 8, (c ^ -1) >>> 0);
      return new Blob([base.slice(0, base.length - 12), bloco, base.slice(base.length - 12)], { type: 'image/png' });
    }
    const corte = 4 + ((base[4] << 8) | base[5]), partes = [base.slice(0, corte)]; let R = b - base.length;  // blocos de comentário depois do cabeçalho
    while (R > 0) { let seg = Math.min(R, 65537); if (R - seg > 0 && R - seg < 4) seg -= 4; if (seg < 4) break; const x = new Uint8Array(seg); x[0] = 255; x[1] = 254; x[2] = (seg - 2) >> 8; x[3] = (seg - 2) & 255; partes.push(x); R -= seg; }
    partes.push(base.slice(corte)); if (R > 0) partes.push(new Uint8Array(R));
    return new Blob(partes, { type: 'image/jpeg' });
  }
  const bytes = new Uint8Array(b); bytes[0] = 77; bytes[1] = 90; return new Blob([bytes]);  // .exe: não é pra abrir mesmo
}

function montaPlano(A, card) {
  const d = dados(), id = card.id, lista = d.planos[id];
  const TIPOS = { P: ['POSITIVO', 'tP'], N: ['NEGATIVO', 'tN'], L: ['VALOR LIMITE', 'tL'] };
  A.innerHTML = `<div class="plano-barra"><p class="dica">Cada cenário: uma situação, os passos e o resultado esperado.</p></div><div class="pop-wrap arq-flut"><div class="arqs pop-arq" id="arqPop" hidden><h3>Arquivos de teste</h3><p class="dica">Gerados na hora, no tamanho exato, pra testar o anexo.</p>${[['documento-5MB-exato.pdf', LIMITE_ANEXO], ['documento-5,1MB.pdf', Math.floor(5.1 * 1048576)], ['documento-1MB.pdf', 1048576], ['print-da-tela.png', 48 * 1024], ['foto.jpg', 220 * 1024], ['programa.exe', 12 * 1024]].map(([n, b]) => `<a href="#" data-arq="${n}" data-b="${b}" data-test="arquivo-teste">${n}<small>${tamanho(b)}</small></a>`).join('')}</div></div>
    <div class="plano"><div class="esq">
      <div class="xres" id="xres" data-test="resumo-execucao"></div>
      <table class="tabela"><thead><tr><th style="width:40px">#</th><th>Cenário</th><th style="width:196px">Execução</th><th style="width:76px"></th></tr></thead><tbody id="linhas"></tbody></table>
      <button type="button" class="${missaoAtual() && missaoAtual().id === 'ep03' ? 'btn' : 'link-add'}" id="abreForm" data-test="novo-cenario">+ ${missaoAtual() && missaoAtual().id === 'ep03' ? 'Novo cenário' : 'Adicionar cenário'}</button>
      <form class="fcard" id="f" novalidate style="margin-top:14px;max-width:none"><h3 style="font-size:18px;margin-bottom:14px" id="fTit">Novo cenário</h3>
        <div style="display:flex;gap:14px;flex-wrap:wrap"><div class="campo" style="flex:2;min-width:240px"><label for="cNome">Cenário <i>*</i></label><input class="in" id="cNome" data-test="cenario-nome" placeholder="Ex.: Criar sem título"></div>
          <div class="campo" style="flex:1;min-width:170px"><label for="cTipo">Tipo</label><select class="in" id="cTipo" data-test="cenario-tipo"><option value="P">Positivo</option><option value="N">Negativo</option><option value="L">Valor limite</option></select></div></div>
        <div class="campo"><label for="cPassos">Passos</label><textarea class="in" id="cPassos" data-test="cenario-passos" placeholder="1. Abrir a tela Novo chamado&#10;2. …"></textarea></div>
        <div class="campo"><label for="cEsp">Resultado esperado <i>*</i></label><input class="in" id="cEsp" data-test="cenario-esperado" placeholder="Seja específico: o que aparece, onde, e o que acontece com o chamado"></div>
        <div class="campo"><label>Quais regras esse cenário cobre?</label><div class="regras-check">${REGRAS.map((r, i) => `<label class="cr"><input type="checkbox" value="${i}" data-test="cenario-regra">${r}</label>`).join('')}</div></div>
        <div class="fbtns"><button type="button" class="btn sec" id="cancela" hidden data-test="cancelar-edicao">Cancelar</button><button class="btn" data-test="salvar-cenario" id="salva">Adicionar cenário</button></div>
      </form></div>
      <aside><div class="cov" id="cov" data-test="cobertura"><div class="hd">Cobertura das regras<span class="cnt" id="cnt" data-test="cobertura-contagem">0/${REGRAS.length}</span></div><div class="bar"><i id="bar"></i></div>
        ${REGRAS.map((r, i) => `<div class="rl" id="u${i}" data-test="regra"><b>✓</b>${r}<span class="q" id="q${i}" hidden></span></div>`).join('')}<div class="ex" id="ex" hidden></div><div class="gabi-b" id="gabiB" data-test="recado-gabriela"><b>GABRIELA · DEV</b><span id="gabiT"></span></div><div class="gabi" aria-hidden="true"><video src="img/anim/gabriela_quadro.webm?v=1794479423" poster="img/anim/gabriela_quadro.png?v=1794479423" autoplay muted loop playsinline></video></div></div></aside></div>`;
  let editando = null; const abertos = new Set();
  d.rodadas = d.rodadas || {};
  const rod = () => d.rodadas[id] || null;
  const naRodada = (i) => !rod() || rod().sel.includes(i);
  const gabi = (tom, tx) => { $('#gabiB').className = 'gabi-b ' + tom; $('#gabiT').textContent = tx; };
  { const ruim = lista.map((c) => revisaCenario(c)).findIndex((r) => r[0] === 'ruim');
    if (!lista.length) gabi('', 'Sou eu que vou ler esse plano. Começa pelo caminho feliz e depois pensa: e se o usuário fizer errado?');
    else if (ruim >= 0) gabi('ruim', `Cenário ${ruim + 1}: ${revisaCenario(lista[ruim])[1]}`);
    else if (VERSAO >= 16 && lista.some((c) => c.regras.includes(6)) && /^\s*Cen[aá]rio:.*espa[çc]o/im.test(gherkinDe(d))) gabi('ok', 'Agora, se esse bug voltar, a gente fica sabendo antes de todo mundo.');
    else gabi('', 'Li seus cenários. Qualquer coisa que eu não entender, eu aviso aqui.'); }
  const mostraForm = (on) => { $('#f').hidden = !on; $('#abreForm').hidden = on; };
  mostraForm(lista.length === 0);
  $('#abreForm').onclick = () => { mostraForm(true); $('#cNome').focus(); };
  addEventListener('scroll', () => { const pop = $('#arqPop'); if (pop && Date.now() - (+pop.dataset.t || 0) > 600) pop.hidden = true; }, { passive: true });
  document.addEventListener('click', (ev) => {
    const b = ev.target.closest('[data-arqbtn]'), pop = $('#arqPop'); if (!pop) return;
    if (b) { const r = b.getBoundingClientRect(); pop.style.top = Math.min(r.bottom + 6, innerHeight - 330) + 'px'; pop.style.left = Math.min(r.left, innerWidth - 340) + 'px'; pop.hidden = !pop.hidden; pop.dataset.t = Date.now(); return; }
    if (!ev.target.closest('.arq-flut')) pop.hidden = true;
  });
  const pinta = () => {
    $('#linhas').innerHTML = lista.length ? lista.map((c, i) => {
      const fora = !c.regras.length, t = TIPOS[c.tipo];
      const dentro = naRodada(i), hist = (c.hist || []).length ? `<div class="hist-r" data-test="historico-rodadas">${c.hist.map((h) => `<span class="hr ${h.exec}" title="Rodada ${h.r} · Sprint ${h.v}">R${h.r} · S${h.v} ${h.exec === 'passou' ? '✓' : h.exec === 'falhou' ? '✕' : '–'}</span>`).join('')}${rod() && dentro ? `<span class="hr atual ${c.exec}">R${rod().n} · S${rod().versao} ${c.exec === 'passou' ? '✓' : c.exec === 'falhou' ? '✕' : '…'}</span>` : ''}</div>` : '';
      return `<tr class="${fora ? 'fora' : ''} ${dentro ? '' : 'fora-rod'} st-${dentro ? c.exec || 'nao' : 'nao'}" data-test="linha-cenario"><td class="num"><span>${i + 1}</span></td><td><div class="cn">${esc(c.nome)}</div><div class="tgs"><span class="tg ${t[1]}">${t[0]}</span>${fora ? `<span class="tg tX">FORA DAS REGRAS</span>` : ''}${fraco(c) ? `<span class="tg tF" data-test="cenario-fraco">NÃO CONTA NA COBERTURA</span>` : ''}${c.exec && c.exec !== 'nao' && !c.evid ? `<span class="tg tF" data-test="sem-evidencia">SEM EVIDÊNCIA</span>` : ''}</div>${c.passos ? `<button type="button" class="link" data-ps="${i}" data-test="ver-passos">${abertos.has(i) ? 'Esconder passos' : 'Ver passos'}</button><div class="passos" ${abertos.has(i) ? '' : 'hidden'}>${esc(c.passos)}</div>` : ''}<div class="res"><small>Resultado esperado</small>${esc(c.esperado)}</div>${hist}${c.regras.includes(3) ? `<button type="button" class="link arq-btn" data-arqbtn data-test="abrir-arquivos">${ico('clipe')}Arquivos de teste</button>` : ''}</td>
        <td>${dentro ? '' : `<div class="xfora" data-test="fora-da-rodada">Fora da rodada ${rod().n}</div>`}<div class="xcel" ${dentro ? '' : 'hidden'}><div class="xseg"><button type="button" class="sg ok ${c.exec === 'passou' ? 'on' : ''}" data-x="${i}" data-v="passou" data-test="marcar-passou">✓ Passou</button><button type="button" class="sg nok ${c.exec === 'falhou' ? 'on' : ''}" data-x="${i}" data-v="falhou" data-test="marcar-falhou">✕ Falhou</button></div><select class="exec-sel" data-i="${i}" data-test="execucao" aria-label="Execução do cenário ${i + 1}"><option value="nao" ${c.exec === 'passou' || c.exec === 'falhou' ? '' : 'selected'}>Não executado</option><option value="passou" ${c.exec === 'passou' ? 'selected' : ''}>Passou</option><option value="falhou" ${c.exec === 'falhou' ? 'selected' : ''}>Falhou</option></select><div class="xlinks">${c.exec === 'falhou' ? (c.bug ? `<a class="bugchip" href="card.html?id=${c.bug}" data-test="bug-ligado">${ico('bug')}${c.bug}</a>` : `<button type="button" class="xl bug" data-bug="${i}" data-test="reportar-bug">${ico('bug')}Reportar bug</button>`) : ''}${c.exec && c.exec !== 'nao' ? `<label class="xl ev ${c.evid ? 'tem' : ''}" title="Print ou vídeo da execução"><input type="file" data-ev="${i}" data-test="evidencia-cenario" accept="image/*,video/*,.pdf" hidden>${ico('clipe')}${c.evid ? esc(c.evid) : 'Anexar evidência'}</label>` : ''}</div></div></td>
        <td><div class="acoes"><button class="icone" data-ed="${i}" data-test="editar-cenario" title="Editar cenário"><svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg></button><button class="icone rm" data-rm="${i}" data-test="excluir-cenario" title="Excluir cenário"><svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M8 6V4h8v2"/><path d="M19 6l-1 14H6L5 6"/></svg></button></div></td></tr>`;
    }).join('') : '<tr><td colspan="4" class="vazio" data-test="plano-vazio">Nenhum cenário ainda</td></tr>';
    let n = 0;
    REGRAS.forEach((r, i) => { const quem = lista.map((c, j) => c.regras.includes(i) && !fraco(c) ? j + 1 : 0).filter(Boolean); const on = quem.length > 0; if (on) n++; $('#u' + i).classList.toggle('on', on); $('#q' + i).hidden = !on; $('#q' + i).textContent = quem.length === 1 ? 'CENÁRIO ' + quem[0] : quem.join(' · '); });
    setTimeout(confereMissoes, 400);
    $('#cnt').textContent = n + '/' + REGRAS.length; $('#bar').style.width = (n / REGRAS.length * 100) + '%'; $('#cov').classList.toggle('done', n === REGRAS.length);
    const fora = lista.map((c, j) => c.regras.length ? 0 : j + 1).filter(Boolean);
    $('#ex').hidden = !fora.length; $('#ex').textContent = `+ Cenário ${fora.join(', ')}: fora das regras`;
    const daRod = lista.filter((c, i) => naRodada(i)), ok = daRod.filter((c) => c.exec === 'passou').length, nok = daRod.filter((c) => c.exec === 'falhou').length, tot = daRod.length;
    $('#xres').hidden = !lista.length;
    const R = rod(), nR = R ? R.n : 1, vR = R ? R.versao : 14;
    $('#xres').innerHTML = `<div class="xrod" data-test="rodada-atual"><span class="xr-n">Rodada ${nR}</span><span class="xr-v">Sprint ${vR}${R ? ' · ' + dataHora(R.data) : ''}</span>${VERSAO >= 15 ? `<button type="button" class="btn sec peq" id="novaRod" data-test="nova-rodada">Nova rodada</button>` : ''}</div><div class="xtop"><span class="xt">Execução</span><span class="xn"><b>${ok + nok}</b> de ${tot} executados</span></div><div class="xb"><i style="width:${tot ? ok / tot * 100 : 0}%"></i><i class="f" style="width:${tot ? nok / tot * 100 : 0}%"></i></div><div class="xleg"><span class="xp"><i></i>${ok} passou</span><span class="xf"><i></i>${nok} falhou</span><span class="xz"><i></i>${tot - ok - nok} a executar</span></div>`;
    if ($('#n-plano')) $('#n-plano').textContent = lista.length || '';
    $$('[data-test=execucao]').forEach((s) => { s.onchange = () => { lista[+s.dataset.i].exec = s.value; if (s.value === 'falhou') lista[+s.dataset.i].jaFalhou = true; salvar(); pinta(); }; });
    $$('[data-x]').forEach((b) => { b.onclick = () => { const i = +b.dataset.x, c = lista[i]; c.exec = c.exec === b.dataset.v ? 'nao' : b.dataset.v; if (c.exec === 'falhou') c.jaFalhou = true; salvar(); pinta();
      if (c.exec !== 'nao' && !c.evid) gabi('ruim', `Cenário ${i + 1}: marcou “${c.exec}”, mas sem evidência. Se alguém perguntar “tem certeza?”, o que você mostra? Anexa o print.`); }; });
    $$('[data-ev]').forEach((f) => { f.onchange = () => { const x = f.files[0]; if (!x) return; const i = +f.dataset.ev; lista[i].evid = x.name; salvar(); pinta(); toast('Evidência anexada ao cenário ' + (i + 1)); gabi('ok', `Cenário ${i + 1} com evidência. Agora ninguém precisa acreditar na sua palavra.`); }; });
    $$('[data-bug]').forEach((b) => { b.onclick = () => { const i = +b.dataset.bug; novaTarefa(() => pinta(), { card: card.id, i, n: i + 1, nome: lista[i].nome, evid: lista[i].evid || '' }); }; });
    $$('[data-ed]').forEach((b) => { b.onclick = () => edita(+b.dataset.ed); });
    $$('[data-ps]').forEach((b) => { b.onclick = () => { const i = +b.dataset.ps; abertos.has(i) ? abertos.delete(i) : abertos.add(i); pinta(); }; });
    $$('[data-rm]').forEach((b) => { b.onclick = () => { const k = +b.dataset.rm; lista.splice(k, 1); if (rod()) rod().sel = rod().sel.filter((x) => x !== k).map((x) => x > k ? x - 1 : x); salvar(); pinta(); toast('Cenário excluído'); }; });
    if ($('#novaRod')) $('#novaRod').onclick = novaRodada;
  };
  // nova rodada: a execução atual vira histórico e só os cenários escolhidos voltam pra executar
  const novaRodada = () => {
    const R = rod(), n = (R ? R.n : 1) + 1, mudou = { 15: 'a validação do título e o limite do anexo', 16: 'a validação do título' }[VERSAO];
    const o = document.createElement('div'); o.className = 'modal-fundo'; o.setAttribute('data-test', 'modal-rodada');
    o.innerHTML = `<form class="modal" id="fR" novalidate><div class="modal-h"><h3>Rodada ${n} · Sprint ${VERSAO}</h3><button type="button" class="icone" data-fecha>✕</button></div>
      <p class="dica">Escolha os cenários pelo que mudou nesta versão. Rodar tudo sempre não cabe no tempo de um sistema de verdade.</p>
      ${mudou ? `<p class="liga">O que mudou na Sprint ${VERSAO}: <b>${mudou}</b>.</p>` : ''}
      <div class="rod-l">${lista.map((c, i) => `<label class="cr" data-test="rodada-cenario"><input type="checkbox" value="${i}" checked><span><b>${i + 1}.</b> ${esc(c.nome)}</span></label>`).join('')}</div>
      <div class="fbtns"><button type="button" class="btn sec" data-fecha>Cancelar</button><button class="btn" data-test="comecar-rodada">Começar rodada ${n}</button></div></form>`;
    document.body.appendChild(o);
    const fecha = () => o.remove(); $$('[data-fecha]', o).forEach((b) => { b.onclick = fecha; }); o.onclick = (e) => { if (e.target === o) fecha(); };
    $('#fR').onsubmit = (ev) => {
      ev.preventDefault(); const sel = $$('#fR input:checked').map((k) => +k.value);
      if (!sel.length) return toast('Escolha pelo menos um cenário', true);
      lista.forEach((c, i) => { if (naRodada(i)) { c.hist = c.hist || []; c.hist.push({ r: R ? R.n : 1, v: R ? R.versao : 14, exec: c.exec || 'nao', evid: c.evid || '', ...(c.bug ? { bug: c.bug } : {}) }); } if (sel.includes(i)) { c.exec = 'nao'; delete c.evid; delete c.bug; } });
      d.rodadas[id] = { n, versao: VERSAO, data: agora(), sel }; salvar(); fecha(); pinta(); toast(`Rodada ${n} aberta na Sprint ${VERSAO}`);
      const feliz = lista.findIndex(cenFeliz);
      if (sel.length === lista.length) gabi('ruim', `Rodar tudo funciona com ${lista.length} cenários. Com novecentos, não. O que a correção mexeu?`);
      else if (feliz >= 0 && !sel.includes(feliz)) gabi('ruim', 'Caminho feliz fora? Sempre passou não quer dizer que vai passar hoje.');
      else gabi('ok', `Rodada ${n} com ${sel.length} cenários. Escolheu pelo que mudou, boa.`);
    };
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
    if (editando !== null) { c.exec = lista[editando].exec; if (lista[editando].bug && !_c('edita')) c.bug = lista[editando].bug; else if (lista[editando].bug) _pv('edita'); if (lista[editando].jaFalhou) c.jaFalhou = true; c.hist = lista[editando].hist; c.evid = lista[editando].evid; lista[editando] = c; toast('Cenário salvo'); } else { lista.push(c); if (rod()) rod().sel.push(lista.length - 1); toast('Cenário adicionado'); }
    gabi(...revisaCenario(c));
    salvar(); limpa(); pinta();
  };
  $('#cancela').hidden = !lista.length;
  $$('[data-arq]').forEach((a) => {
    a.onclick = (ev) => {
      ev.preventDefault();
      const n = a.dataset.arq, b = +a.dataset.b;
      const url = URL.createObjectURL(arquivoTeste(n, b)); const l = document.createElement('a'); l.href = url; l.download = n; document.body.appendChild(l); l.click(); l.remove(); setTimeout(() => URL.revokeObjectURL(url), 2000);
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
    return `<div class="missao ${ok ? 'ok' : ''}" data-test="missao-${m.id}"><div class="k">${ok ? 'CONQUISTA DESBLOQUEADA' : 'MISSÃO'} · ${m.aula.toUpperCase()}</div><div class="v">${m.titulo}</div>
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
  const reg = d.cards.find((c) => c.tipo === 'bug' && c.regressao && c.coluna !== 'concluido');
  if (VERSAO === 15 && reg && /regress|release|segur|recomend|subir|quebr/.test(t)) return R('beatriz', `Segura a release então. Gabi, prioridade no ${reg.id}.`, `Obrigada por avisar antes. Release segurada até o ${reg.id} sair.`);
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
// perguntas prontas do FlowChat: cada uma traz uma informação que só a pessoa certa tem
const PERGUNTAS = {
  'time-produto': [
    ['rafael', 'Rafael, título só com espaços pode?', 'Não pode! Título só com espaço é a mesma coisa que vazio: tem que aparecer "Título é obrigatório". Esqueci de escrever isso no card, valeu por perguntar.'],
    ['rafael', 'Rafael, o anexo de exatamente 5 MB passa?', 'Passa. A regra é "até 5 MB", então 5 MB certinho tem que ser aceito. Só acima disso que recusa.'],
    ['gabriela', 'Gabriela, o FD-101 já está pronto pra testar?', `Tá sim, subi na Sprint ${VERSAO}. Pode testar à vontade, e se achar bug me manda com os passos.`],
    ['lucas', 'Lucas, o que eu falo na daily?', 'Três coisas: o que você fez ontem, o que vai fazer hoje e se tem algo te travando. Curto e direto.'],
  ],
  bugs: [
    ['gabriela', 'Gabriela, como você prefere receber um bug?', 'Com passos numerados, resultado esperado, resultado obtido e um print. Assim eu reproduzo sem precisar te chamar.'],
    ['vinicius', 'Vinícius, quando eu abro bug e quando é melhoria?', 'Bug é quando o sistema não faz o que a regra diz. Melhoria é quando faz, mas podia ser melhor. Na dúvida, pergunta pro Rafael.'],
  ],
  releases: [['beatriz', 'Beatriz, quando sai a próxima release?', 'Sexta, depois da review. Se tiver bug que segura a entrega, me avisa antes, tá?']],
  geral: [['beatriz', 'Beatriz, o que acontece na review?', 'A gente mostra pro time o que ficou pronto na sprint. QA ajuda a dizer o que foi testado e o que ficou de fora.']],
};
PAGINAS.chat = () => {
  const d = dados();
  if (!chatLiberado(d)) {
    return casca('chat', topo('FlowChat') + `<div class="trancado" data-test="chat-bloqueado"><div class="tr-ic">${ico('cadeado')}</div><h3>O FlowChat libera depois da missão do EP04</h3><p>Primeiro você monta o plano de testes do FD-101. Quando terminar, o time te chama aqui pra tirar as dúvidas que o card não responde.</p><a class="btn" href="card.html?id=FD-101&aba=plano">Ir pro plano de testes</a>${fala('vinicius', 'VINÍCIUS', 'No trabalho é igual: antes de perguntar, lê o card. Aí sua pergunta fica muito melhor.')}</div>`);
  }
  const canal = d.chat[qs.get('canal')] ? qs.get('canal') : 'time-produto', l = d.chat[canal];
  d.perguntadas = d.perguntadas || [];
  const msgHtml = (m) => `<div class="msg ${m.de === 'voce' ? 'eu' : ''}" data-test="mensagem">${m.de === 'voce' ? '<span class="vc">VC</span>' : `<img src="img/av_${m.de}.png" alt="">`}<div><div class="who">${PESSOAS[m.de].nome}<i>${PESSOAS[m.de].papel}</i><small>${hora(m.quando)}</small></div><div class="tx">${esc(m.tx)}</div></div></div>`;
  const prontas = () => (PERGUNTAS[canal] || []).map((q, i) => d.perguntadas.includes(canal + i) ? '' : `<button type="button" class="pq" data-pq="${i}" data-test="pergunta-pronta"><img src="img/av_${q[0]}.png" alt="">${esc(q[1])}</button>`).join('');
  casca('chat', `<div class="chatv"><div class="chan">
      <div class="t">Canais</div>${Object.keys(d.chat).map((k) => `<a href="chat.html?canal=${k}" class="${k === canal ? 'on' : ''}" data-test="canal-${k}"><span>#</span> ${k}</a>`).join('')}</div>
    <div class="msgs"><div class="chead"><b># ${canal}</b><span class="avs">${TIME.map(([p]) => `<img src="img/av_${p}.png" alt="${PESSOAS[p].nome}" title="${PESSOAS[p].nome}">`).join('')}</span><span class="mem">6 membros</span></div><div class="lista" id="lista" data-test="mensagens">${l.map(msgHtml).join('')}</div>
      <div class="digitando" id="dig" data-test="digitando" hidden></div>
      <div class="prontas" id="prontas"><span class="pk">Perguntas que valem a pena</span><div id="pqs">${prontas()}</div></div>
      <form class="composer" id="f"><input class="in" id="tx" placeholder="Mensagem em #${canal}" data-test="mensagem-texto" autocomplete="off"><button class="btn" data-test="enviar-mensagem">Enviar</button></form></div>
    <aside class="quem"><div class="t">Quem é quem</div>${TIME.map(([p, tx]) => `<div class="pes"><img src="img/av_${p}.png" alt=""><div><b>${PESSOAS[p].nome} <i>${PESSOAS[p].papel}</i></b><span>${tx}</span></div></div>`).join('')}</aside></div>`);
  const desce = () => { $('#lista').scrollTop = 1e9; };
  const pintaProntas = () => { const h = prontas(); $('#pqs').innerHTML = h; $('#prontas').hidden = !h.trim(); ligaProntas(); };
  const conversa = (t, r) => {
    const m = { de: 'voce', tx: t, quando: agora() }; l.push(m); salvar(); $('#lista').insertAdjacentHTML('beforeend', msgHtml(m)); desce();
    setTimeout(() => { $('#dig').hidden = false; $('#dig').textContent = `${PESSOAS[r.de].nome} está digitando…`; }, 700);
    setTimeout(() => { $('#dig').hidden = true; const rm = { ...r, quando: agora() }; l.push(rm); salvar(); $('#lista').insertAdjacentHTML('beforeend', msgHtml(rm)); desce(); confereMissoes(); }, 2400);
  };
  const ligaProntas = () => $$('[data-pq]').forEach((b) => { b.onclick = () => { const i = +b.dataset.pq, q = PERGUNTAS[canal][i]; d.perguntadas.push(canal + i); salvar(); pintaProntas(); conversa(q[1], { de: q[0], tx: q[2] }); }; });
  pintaProntas(); desce();
  $('#f').onsubmit = (ev) => { ev.preventDefault(); const t = $('#tx').value.trim(); if (!t) return; $('#tx').value = ''; conversa(t, respostaDoTime(t, canal)); };
};

PAGINAS.configuracoes = () => {
  const cs = contas(), c = cs[sessao()];
  casca('configuracoes', topo('Configurações') + `
    <div class="fcard"><div class="campo"><label for="cfNome">Seu nome</label><div style="display:flex;gap:10px"><input class="in" id="cfNome" value="${esc(c.nome)}" data-test="config-nome"><button class="btn" id="salvaNome" data-test="salvar-nome">Salvar</button></div></div>
      <div class="campo"><label>E-mail</label><input class="in" value="${esc(sessao())}" disabled></div>
      <div class="campo" style="margin-bottom:0"><label>Sua carreira</label>${trilha()}<div class="dica">${xpDe()} XP · ${nivelAtual()}. O XP vem das missões de cada prática.</div></div></div>
    <div class="fcard sprint-auto" style="margin-top:18px" data-test="sprint-atual"><div class="sa-n">${VERSAO}</div><div><h3>Sprint ${VERSAO} · homologação</h3><p class="dica">${VERSAO === 14 ? 'A sprint muda sozinha: quando você terminar a missão do EP08, a Gabriela sobe a <b>Sprint 15</b> com as correções.' : VERSAO === 15 ? 'Você está na Sprint 15, com as correções da Gabriela. Quando terminar a missão do EP12, sobe a <b>Sprint 16</b>.' : 'Você está na Sprint 16, com a correção da regressão.'}</p></div></div>
    <div class="fcard" style="margin-top:18px"><h3 style="font-size:17px;margin-bottom:6px">Carregar save do curso</h3><p class="dica" style="margin-bottom:12px">Perdeu o progresso, trocou de computador ou pulou uma aula? Carregue o ponto do curso em que você está. O FlowDesk fica do jeito que o vídeo espera. <b>Isso substitui o que você tem agora.</b></p>
      <div class="saves" id="saves">${SAVES.map((x, i) => `<button type="button" class="sv ${i === 0 ? 'on' : ''}" data-sv="${x.id}" data-test="save-${x.id}"><span class="sv-ep">${(x.nome.match(/EP\d+/) || ['EP00'])[0]}</span><b>${i === 0 ? x.nome : x.quando}</b><span>${i === 0 ? x.quando : x.nome}</span></button>`).join('')}</div>
      <select class="exec-sel" id="cfSave" data-test="save-episodio" aria-label="Save do curso">${SAVES.map((x) => `<option value="${x.id}">${x.nome} · ${x.quando}</option>`).join('')}</select>
      <button class="btn sec" id="carregaSave" data-test="carregar-save" style="margin-top:14px">Carregar este save</button>
      <div id="confSave" hidden style="margin-top:12px"><b>Tem certeza?</b> O que você fez até agora vai ser trocado pelo save. <button class="btn peq" id="saveSim" data-test="confirmar-save">Sim, carregar</button> <button class="btn sec peq" id="saveNao">Cancelar</button></div></div>
    <div class="fcard" style="margin-top:18px"><h3 style="font-size:17px;margin-bottom:6px">Levar o progresso pra outro computador</h3><p class="dica" style="margin-bottom:12px">Baixe um arquivo com tudo o que você fez. No outro computador, crie a conta e importe o arquivo.</p>
      <div style="display:flex;gap:10px;flex-wrap:wrap"><button class="btn sec" id="exporta" data-test="exportar-progresso">Exportar progresso</button><label class="btn sec" for="importa" style="cursor:pointer">Importar progresso<input type="file" id="importa" accept=".json,application/json" data-test="importar-progresso" hidden></label></div></div>
    <div class="fcard" style="margin-top:18px;border-color:#5b1d24"><h3 style="font-size:17px;margin-bottom:6px">Recomeçar do zero</h3><p class="dica" style="margin-bottom:12px">Apaga os chamados, cards, cenários e mensagens que você criou e volta tudo pro começo do curso. A sua conta continua.</p>
      <button class="btn perigo" id="zera" data-test="recomecar">Recomeçar do zero</button>
      <div id="conf" hidden style="margin-top:12px"><b>Tem certeza?</b> Isso não tem volta. <button class="btn perigo peq" id="zeraSim" data-test="confirmar-recomecar">Sim, apagar tudo</button> <button class="btn sec peq" id="zeraNao">Cancelar</button></div></div>`);
  $('#salvaNome').onclick = () => { const n = $('#cfNome').value.trim(); if (!n) return toast('O nome não pode ficar vazio', true); c.nome = n; LS.set('fd:contas', cs); recado('Nome salvo'); location.reload(); };
  const marcaSave = () => $$('[data-sv]').forEach((b) => b.classList.toggle('on', b.dataset.sv === $('#cfSave').value));
  $$('[data-sv]').forEach((b) => { b.onclick = () => { $('#cfSave').value = b.dataset.sv; marcaSave(); }; });
  $('#cfSave').addEventListener('change', marcaSave);
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

// ---------- caça aos bugs ----------
// Os reports vão pro Worker da Cloudflare (CACA_API). Cada envio entra na linha do tempo pública na hora, com um recibo:
// assim todo mundo vê quem mandou primeiro. O professor aprova no painel e o placar atualiza.
const iniciais = (n) => n.split(/\s+/).filter(Boolean).map((x) => x[0]).slice(0, 2).join('').toUpperCase();
const dataHora = (iso) => new Date(iso).toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' });
PAGINAS.caca = () => {
  const c = contas()[sessao()], mes = new Date().toLocaleDateString('pt-BR', { month: 'long' });
  const aberta = !!CACA_API;
  const meus = LS.get('fd:caca-envios', []);
  casca('caca', `<section class="caca-hero"><div class="ch-t"><div class="ch-k"><span id="tNum">TEMPORADA 1 DE 3</span><b class="${aberta ? 'ab' : ''}">${aberta ? 'ABERTA' : 'EM BREVE'}</b>${aberta ? '<i id="tFim">quando os 3 forem achados, a próxima temporada abre sozinha</i>' : ''}</div>
      <h1 data-test="titulo-pagina">3 bugs escondidos no FlowDesk.</h1><p>Quem achar e reportar primeiro ganha o <b>Vida de QA 2</b> de graça quando lançar. Preste atenção nas aulas.</p></div>
      <video src="img/anim/vinicius_lupa_v2.webm?v=1794479423" poster="img/anim/vinicius_lupa_v2.png?v=1794479423" autoplay muted loop playsinline aria-label="Vinícius com uma lupa procurando bugs"></video></section>
    <div class="caca-bugs" id="placar">${[1, 2, 3].map((n) => `<article class="cb"><div class="cb-h"><span>#${n}</span><b>LIVRE</b></div><div class="cb-v">Ninguém achou ainda.</div></article>`).join('')}</div>
    <div class="caca-grade"><section class="painel caca-form"><h2>Reportar um bug da caça</h2><p class="dica">A confirmação é automática. Vale o primeiro report confirmado de cada bug.</p>
      <form id="fc" novalidate>${aberta ? '' : '<div class="aviso-caca" data-test="caca-fechada">A primeira temporada ainda não abriu. Quando abrir, este formulário passa a funcionar e o aviso sai daqui.</div>'}
        <div class="campo"><label for="cNomeU">Seu nome na Udemy <i>*</i></label><input class="in" id="cNomeU" data-test="caca-nome" value="${esc(c.nome)}"></div>
        <div class="campo"><label>Bug que você reproduziu <i>*</i></label><div id="qual" data-test="caca-qual"></div></div>
        <div class="campo"><label for="cPas">Passos para reproduzir <i>*</i></label><textarea class="in" id="cPas" data-test="caca-passos" placeholder="1. Abrir…&#10;2. …"></textarea></div>
        <div class="linha2"><div class="campo"><label for="cEspC">Resultado esperado <i>*</i></label><input class="in" id="cEspC" data-test="caca-esperado"></div><div class="campo"><label for="cObtC">Resultado obtido <i>*</i></label><input class="in" id="cObtC" data-test="caca-obtido"></div></div>
        <div class="campo"><label for="cEvi">Evidência <small>(link do print ou do vídeo: Drive, Imgur, YouTube…)</small></label><input class="in" id="cEvi" data-test="caca-evidencia" placeholder="https://"></div>
        <div class="campo"><label for="cAmb">Ambiente <small>(navegador, celular ou computador)</small></label><input class="in" id="cAmb" data-test="caca-ambiente" placeholder="Ex.: Chrome no Android"></div>
        <button class="btn" data-test="caca-enviar" ${aberta ? '' : 'disabled'}>Enviar report</button></form>
      ${meus.length ? `<div class="meus"><h3>Seus envios</h3>${meus.map((e) => `<div class="me" data-recibo="${e.id}"><span>Bug #${e.bug}</span><span>${dataHora(e.quando)}</span><span>recibo <b>${e.id.slice(-8)}</b></span><span class="est">conferindo…</span></div>`).join('')}</div>` : ''}</section>
      <aside class="caca-lado"><section class="painel"><h2>Como funciona</h2><ol class="passos-c"><li>Teste o FlowDesk como no curso. Os bugs estão em telas que você já conhece.</li><li>Reproduziu um? O FlowDesk reconhece e mostra o número dele no formulário. Você não precisa adivinhar qual é.</li><li>Reporte com passos, esperado, obtido e evidência.</li><li>Seu envio entra na linha do tempo na hora, com um recibo. Todo mundo vê quem mandou primeiro.</li><li>Só vale bug que você reproduziu aqui no FlowDesk, neste navegador, e explicou nos passos. Confirmado, seu nome entra no placar na hora.</li><li>Ganhou? Aparece um código de vitória aqui. Mande ele por mensagem pro professor na Udemy e receba o cupom do Vida de QA 2.</li></ol></section>
        ${fala('vinicius', 'VINÍCIUS', 'Bug que ninguém consegue reproduzir não conta. No trabalho é igual.')}
        <section class="painel" id="hallBox" hidden><h2>Hall dos caçadores</h2><div id="hall"></div></section>
        <section class="painel"><h2>Linha do tempo</h2><p class="dica">Todo envio aparece aqui na hora em que chega, em ordem.</p><div id="linha" class="linha-t" data-test="caca-linha"><p class="dica">${aberta ? 'Carregando…' : 'Nenhum envio ainda.'}</p></div></section></aside></div>`);
  let qual = 0;
  // o aluno não escolhe número no escuro: o FlowDesk mostra só os bugs que ele reproduziu neste navegador
  const montaQual = (bugs) => {
    const T = (LS.get('fd:placar', {}) || {}).temporada || 1, pr = LS.get('fd:caca-prova', {});
    const ach = [1, 2, 3].filter((n) => pr[`${T}-${n}`]), tem = (n) => (bugs || []).some((b) => b.n === n && b.ganhador);
    $('#qual').innerHTML = ach.length ? `<div class="seg-b">${ach.map((n) => `<button type="button" data-qual="${n}" data-test="caca-bug-${n}" ${tem(n) ? 'disabled' : ''}>Bug #${n}${tem(n) ? ' · já achado' : ` · reproduzido em ${dataHora(pr[`${T}-${n}`].q)}`}</button>`).join('')}</div>`
      : '<p class="qual-vazio" data-test="caca-sem-prova">Você ainda não reproduziu nenhum bug da caça neste navegador. Quando reproduzir, ele aparece aqui sozinho, já com o número.</p>';
    const livres = $$('[data-qual]').filter((b) => !b.disabled);
    $$('[data-qual]').forEach((b) => { b.onclick = () => { if (b.disabled) return; qual = +b.dataset.qual; $$('[data-qual]').forEach((x) => x.classList.toggle('on', x === b)); }; });
    if (!livres.some((b) => +b.dataset.qual === qual)) qual = 0;
    if (livres.length === 1) livres[0].onclick(); else livres.forEach((b) => b.classList.toggle('on', +b.dataset.qual === qual));
  };
  montaQual();
  const pinta = (p) => {
    LS.set('fd:placar', { bugs: p.bugs, temporada: p.temporada, encerrada: p.encerrada });
    $('#tNum').textContent = p.encerrada ? 'CAÇA ENCERRADA' : `TEMPORADA ${p.temporada} DE ${p.total || 3}`;
    if (p.encerrada) { $('.caca-hero h1').textContent = 'A caça terminou.'; $('.caca-hero p').innerHTML = 'Foram 3 temporadas e 9 caçadores. Os nomes ficam aqui pra sempre.'; if ($('#tFim')) $('#tFim').remove(); $$('#fc input, #fc textarea, #fc button').forEach((x) => { x.disabled = true; }); }
    const passadas = (p.hall || []).filter((h) => h.bugs.some((b) => b.ganhador));
    if (passadas.length) { $('#hallBox').hidden = false; $('#hall').innerHTML = passadas.map((h) => `<div class="hall-t"><b>Temporada ${h.temporada}</b>${h.bugs.map((b) => `<span class="${b.ganhador ? 'on' : ''}">#${b.n} ${b.ganhador ? esc(b.ganhador) : 'livre'}</span>`).join('')}</div>`).join(''); }
    $('#placar').innerHTML = p.bugs.map((b) => b.ganhador ? `<article class="cb on"><div class="cb-h"><span>#${b.n}</span><b>ENCONTRADO</b></div><div class="cb-g"><span class="ini">${esc(iniciais(b.ganhador))}</span><div><b>${esc(b.ganhador)}</b><small>achou em ${dataHora(b.quando)}</small></div></div></article>` : `<article class="cb"><div class="cb-h"><span>#${b.n}</span><b>LIVRE</b></div><div class="cb-v">Ninguém achou ainda.</div></article>`).join('');
    montaQual(p.bugs);
    const est = { pendente: 'conferindo', aprovado: 'aprovado', recusado: 'recusado' };
    $('#linha').innerHTML = (p.envios || []).length ? [...p.envios].reverse().map((e) => `<div class="lt ${e.estado}"><span class="ini">${esc(iniciais(e.nome))}</span><div><b>${esc(e.nome)}</b> mandou o bug #${e.bug}<small>${dataHora(e.quando)} · recibo ${esc(e.recibo)}</small></div><i>${est[e.estado] || e.estado}</i></div>`).join('') : '<p class="dica">Nenhum envio ainda. Pode ser você o primeiro.</p>';
  };
  const confereMeus = () => $$('[data-recibo]').forEach(async (el) => {
    try { const r = await (await fetch(`${CACA_API}/recibo?id=${encodeURIComponent(el.dataset.recibo)}`)).json(); if (!r.ok) return;
      $('.est', el).innerHTML = r.ganhou ? `<b class="vit" data-test="codigo-vitoria">Você ganhou! Código: ${esc(r.codigo)}</b>` : ({ pendente: 'conferindo…', aprovado: 'aprovado, mas alguém chegou antes', recusado: 'recusado' }[r.estado] || r.estado);
    } catch (e) { /* sem internet */ }
  });
  if (aberta) { fetch(`${CACA_API}/placar`).then((r) => r.json()).then(pinta).catch(() => { $('#linha').innerHTML = '<p class="dica">Não deu pra carregar agora. Tenta de novo daqui a pouco.</p>'; }); confereMeus(); }
  $('#fc').onsubmit = async (ev) => {
    ev.preventDefault(); limpaErros(); if (!aberta) return;
    const v = (i) => $('#' + i).value.trim(); let ok = true;
    if (!v('cNomeU')) { erroCampo('cNomeU', 'Escreva seu nome na Udemy'); ok = false; }
    if (!qual) { toast('Primeiro reproduza um bug da caça aqui no FlowDesk', true); ok = false; }
    if (v('cPas').length < 15) { erroCampo('cPas', 'Escreva os passos pra reproduzir'); ok = false; }
    if (!v('cEspC')) { erroCampo('cEspC', 'Escreva o resultado esperado'); ok = false; }
    if (!v('cObtC')) { erroCampo('cObtC', 'Escreva o resultado obtido'); ok = false; }
    if (!ok) return;
    try {
      const r = await (await fetch(`${CACA_API}/envio`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ nome: v('cNomeU'), bug: qual, passos: v('cPas'), esperado: v('cEspC'), obtido: v('cObtC'), evidencia: v('cEvi'), ambiente: v('cAmb'), prova: LS.get('fd:caca-prova', {})[`${(LS.get('fd:placar', {}) || {}).temporada || 1}-${qual}`] || null }) })).json();
      if (!r.ok) return toast(r.erro || 'Não deu pra enviar', true);  // inclui recusado sem prova
      meus.push({ id: r.id, bug: qual, quando: r.quando }); LS.set('fd:caca-envios', meus);
      recado(r.ganhou ? `Confirmado! Você achou o bug #${qual}. Seu código: ${r.codigo}` : `Report enviado. Recibo ${r.recibo}`); location.reload();
    } catch (e) { toast('Sem conexão com o servidor da caça. Tenta de novo.', true); }
  };
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
