# Projeto 2 · Testes da Lojinha do Leigo

Testes de ponta a ponta da história **LOJA-87: ordenar os produtos**, na Lojinha do Leigo.

## Cenários
- Login: usuário válido, senha errada, usuário bloqueado, usuário vazio, senha vazia
- Ordenação: nome de A a Z, de Z a A, preço do menor pro maior e do maior pro menor
- Produto esgotado: aparece, mas não dá pra comprar
- Fora do escopo: pagamento

## O bug que eu achei
Na versão 1, ordenar por preço comparava o preço como texto: R$ 12,50 e R$ 129,90 vinham antes de R$ 7,99.
Achei testando na mão, antes de automatizar. Na versão 2 foi corrigido, e os testes de ordenação ficam de guarda.

## Tecnologias
Playwright, JavaScript, Page Object, fixtures, dados em JSON, GitHub Actions

## Rodando
npm install
npx playwright install
npx playwright test
npx playwright test --grep @smoke
