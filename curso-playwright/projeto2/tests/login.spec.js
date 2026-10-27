import { test, expect } from '../fixtures/paginas';
import casos from '../dados/login.json';

test.describe('Login', () => {
  test.beforeEach(async ({ loginPage }) => {
    await loginPage.abrir();
  });

  const smoke = { tag: '@smoke' };
  test('entra com usuário válido', smoke, async ({ page, loginPage, produtosPage }) => {
    await loginPage.entrar(process.env.LOJA_USUARIO, process.env.LOJA_SENHA);
    await expect(page).toHaveURL(/produtos/);
    await expect(produtosPage.titulo).toHaveText('Produtos');
  });

  for (const caso of casos) {
    test(`mostra erro: ${caso.cenario}`, async ({ loginPage }) => {
      await loginPage.entrar(caso.usuario, caso.senha);
      await expect(loginPage.erro).toHaveText(caso.mensagem);
    });
  }
});
