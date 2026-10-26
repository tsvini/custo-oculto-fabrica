import { test, expect } from '@playwright/test';
import { LoginPage } from '../../pages/LoginPage';
import { ProdutosPage } from '../../pages/ProdutosPage';
import { CheckoutPage } from '../../pages/CheckoutPage';

test.describe('Compra', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    const login = new LoginPage(page);
    await login.entrar(process.env.SAUCE_USER, process.env.SAUCE_PASSWORD);
  });

  test('aula 40: compra uma mochila do começo ao fim', async ({ page }) => {
    const produtos = new ProdutosPage(page);
    const checkout = new CheckoutPage(page);

    await produtos.adicionar('sauce-labs-backpack');
    await expect(produtos.contadorCarrinho).toHaveText('1');
    await produtos.irParaCarrinho();
    await checkout.botaoCheckout.click();
    await checkout.preencherDados('Maria', 'Silva', '88000-000');
    await checkout.botaoFinalizar.click();
    await expect(checkout.mensagemFinal).toHaveText('Thank you for your order!');
  });
});
