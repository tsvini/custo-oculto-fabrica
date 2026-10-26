import { test, expect } from '@playwright/test';
import { ProdutosPage } from '../../pages/ProdutosPage';
import { CheckoutPage } from '../../pages/CheckoutPage';

test.use({ storageState: 'playwright/.auth/usuario.json' });

test('aula 42: compra uma mochila do começo ao fim', async ({ page }) => {
  const produtos = new ProdutosPage(page);
  const checkout = new CheckoutPage(page);

  await test.step('adiciona a mochila no carrinho', async () => {
    await page.goto('/inventory.html');
    await produtos.adicionar('sauce-labs-backpack');
    await expect(produtos.contadorCarrinho).toHaveText('1');
  });

  await test.step('abre o carrinho', async () => {
    await produtos.irParaCarrinho();
    await expect(page.getByText('Sauce Labs Backpack')).toBeVisible();
  });

  await test.step('preenche os dados de entrega', async () => {
    await checkout.botaoCheckout.click();
    await checkout.preencherDados('Maria', 'Silva', '88000-000');
  });

  await test.step('finaliza a compra', async () => {
    await checkout.botaoFinalizar.click();
    await expect(checkout.mensagemFinal).toHaveText('Thank you for your order!');
  });
});
