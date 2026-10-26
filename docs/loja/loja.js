// Lojinha do Leigo: loja de treino do curso Playwright para Leigos.
// ?versao=1 abre a versão antiga, com o bug na ordenação por preço (compara o preço como texto). Sem o parâmetro: a versão corrigida.
const VERSAO = (() => {
  const p = new URLSearchParams(location.search).get('versao');
  if (p) sessionStorage.setItem('versao', p);
  return sessionStorage.getItem('versao') === '1' ? 1 : 2;
})();
const USUARIOS = { cliente: { senha: 'leigo123' }, bloqueado: { senha: 'leigo123', bloqueado: true } };
const real = (v) => 'R$ ' + v.toFixed(2).replace('.', ',');
const MARCA = (img = true) => `<span class="marca">${img ? '<img src="img/logo.svg" alt="">' : ''}<span class="palavra"><span class="l1">lojinha</span><span class="l2"><small>do</small>leigo</span></span></span>`;
function cabecalho(categorias) {
  const u = sessionStorage.getItem('usuario') || '';
  document.body.insertAdjacentHTML('afterbegin', `<header><div class="topo">${MARCA()}<span class="versao" data-test="versao">versão ${VERSAO}</span>
    <label class="busca"><input data-test="busca" placeholder="O que você procura hoje?" aria-label="Buscar produtos"><span>🔍</span></label>
    <div class="acoes"><span class="ola"><small>Olá,</small><span data-test="usuario-logado">${u}</span></span>
    <span class="carrinho" title="Carrinho">🛒<span class="contador" data-test="contador-carrinho" hidden>0</span></span><button data-test="sair">Sair</button></div></div>
    <nav class="categorias"><div>${['Todos', ...categorias].map((c, i) => `<button data-test="categoria" class="${i ? '' : 'ativa'}">${c}</button>`).join('')}</div></nav></header>`);
}
