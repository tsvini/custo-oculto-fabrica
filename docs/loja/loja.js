// Loja do Leigo: loja de treino do curso Playwright para Leigos.
// ?versao=1 abre a versão antiga, com o bug na ordenação por preço (compara o preço como texto). Sem o parâmetro: a versão corrigida.
const VERSAO = (() => {
  const p = new URLSearchParams(location.search).get('versao');
  if (p) sessionStorage.setItem('versao', p);
  return sessionStorage.getItem('versao') === '1' ? 1 : 2;
})();
const USUARIOS = { cliente: { senha: 'leigo123' }, bloqueado: { senha: 'leigo123', bloqueado: true } };
const real = (v) => 'R$ ' + v.toFixed(2).replace('.', ',');
function cabecalho(logado) {
  document.body.insertAdjacentHTML('afterbegin', `<header><div><h1>🛒 Loja do Leigo</h1><span class="versao" data-test="versao">versão ${VERSAO}</span></div>${logado ? '<div><span>Carrinho<span class="contador" data-test="contador-carrinho" hidden>0</span></span> <button data-test="sair">Sair</button></div>' : ''}</header>`);
}
