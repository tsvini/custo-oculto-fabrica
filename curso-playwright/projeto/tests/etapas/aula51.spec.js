import { test, expect } from '@playwright/test';

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
  });
});
