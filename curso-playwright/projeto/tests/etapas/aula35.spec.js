import { test, expect } from '@playwright/test';

test.describe('Compra', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.getByTestId('username').fill(process.env.SAUCE_USER);
    await page.getByTestId('password').fill(process.env.SAUCE_PASSWORD);
    await page.getByTestId('login-button').click();
  });

  test('aula 35: compra uma mochila do começo ao fim', async ({ page }) => {
    await page.getByTestId('add-to-cart-sauce-labs-backpack').click();
    await expect(page.getByTestId('shopping-cart-badge')).toHaveText('1');
  });
});
