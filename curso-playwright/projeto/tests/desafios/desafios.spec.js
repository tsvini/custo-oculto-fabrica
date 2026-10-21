const { test, expect } = require('@playwright/test');

test.describe('Desafios', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('desafio 1: senha errada mostra erro', async ({ page }) => {
    await page.getByTestId('username').fill('standard_user');
    await page.getByTestId('password').fill('senha_errada');
    await page.getByTestId('login-button').click();
    await expect(page.getByTestId('error')).toContainText('do not match');
  });

  test('desafio 2: campos vazios', async ({ page }) => {
    await page.getByTestId('login-button').click();
    await expect(page.getByTestId('error')).toContainText('Username is required');
  });

  test.describe('logado', () => {
    test.use({ storageState: 'playwright/.auth/usuario.json' });

    test.beforeEach(async ({ page }) => {
      await page.goto('/inventory.html');
    });

    test('desafio 3: remove do carrinho', async ({ page }) => {
      await page.getByTestId('add-to-cart-sauce-labs-backpack').click();
      await expect(page.getByTestId('shopping-cart-badge')).toHaveText('1');
      await page.getByTestId('remove-sauce-labs-backpack').click();
      await expect(page.getByTestId('shopping-cart-badge')).toHaveCount(0);
    });

    test('desafio 4: ordena do menor para o maior preço', async ({ page }) => {
      await page.getByTestId('product-sort-container').selectOption('lohi');
      await expect(page.getByTestId('inventory-item-price').first()).toHaveText('$7.99');
    });

    test('desafio 5: logout', async ({ page }) => {
      await page.getByRole('button', { name: 'Open Menu' }).click();
      await page.getByTestId('logout-sidebar-link').click();
      await expect(page.getByTestId('login-button')).toBeVisible();
    });

    test('desafio final: compra com dois produtos', async ({ page }) => {
      await page.getByTestId('add-to-cart-sauce-labs-backpack').click();
      await page.getByTestId('add-to-cart-sauce-labs-bike-light').click();
      await expect(page.getByTestId('shopping-cart-badge')).toHaveText('2');
      await page.getByTestId('shopping-cart-link').click();
      await page.getByTestId('checkout').click();
      await page.getByTestId('firstName').fill('Maria');
      await page.getByTestId('lastName').fill('Silva');
      await page.getByTestId('postalCode').fill('88000-000');
      await page.getByTestId('continue').click();
      await expect(page.getByTestId('total-label')).toContainText('$43.18');
      await page.getByTestId('finish').click();
      await expect(page.getByTestId('complete-header')).toHaveText('Thank you for your order!');
    });
  });
});
