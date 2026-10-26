import { test, expect } from '@playwright/test';

test.describe('Compra', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.getByTestId('username').fill(process.env.SAUCE_USER);
    await page.getByTestId('password').fill(process.env.SAUCE_PASSWORD);
    await page.getByTestId('login-button').click();
  });

  test('aula 36: compra uma mochila do começo ao fim', async ({ page }) => {
    await page.getByTestId('add-to-cart-sauce-labs-backpack').click();
    await expect(page.getByTestId('shopping-cart-badge')).toHaveText('1');
    await page.getByTestId('shopping-cart-link').click();
    await page.getByTestId('checkout').click();
    await page.getByTestId('firstName').fill('Maria');
    await page.getByTestId('lastName').fill('Silva');
    await page.getByTestId('postalCode').fill('88000-000');
    await page.getByTestId('continue').click();
    await page.getByTestId('finish').click();
    await expect(page.getByTestId('complete-header')).toHaveText('Thank you for your order!');
  });
});
