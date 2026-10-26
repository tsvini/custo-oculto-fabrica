// Lojinha do Leigo: loja de treino do curso Playwright para Leigos.
// ?versao=1 abre a versão antiga, com o bug na ordenação por preço (compara o preço como texto). Sem o parâmetro: a versão corrigida.
const VERSAO = (() => {
  const p = new URLSearchParams(location.search).get('versao');
  if (p) sessionStorage.setItem('versao', p);
  return sessionStorage.getItem('versao') === '1' ? 1 : 2;
})();
const USUARIOS = { cliente: { senha: 'leigo123' }, bloqueado: { senha: 'leigo123', bloqueado: true } };
const real = (v) => 'R$ ' + v.toFixed(2).replace('.', ',');
const MARCA = (img = true) => `<span class="marca">${img ? '<img src="img/mascote-pequeno.jpg" alt="">' : ''}<span class="palavra"><span class="l1">lojinha</span><span class="l2"><small>do</small>leigo</span></span></span>`;
function cabecalho() {
  document.body.insertAdjacentHTML('afterbegin', `<header><div style="display:flex;align-items:center">${MARCA()}<span class="versao" data-test="versao">versão ${VERSAO}</span></div><div class="acoes"><span class="carrinho">🛒 Carrinho <span class="contador" data-test="contador-carrinho" hidden>0</span></span><button data-test="sair">Sair</button></div></header>`);
}
