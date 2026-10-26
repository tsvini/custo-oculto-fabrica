import { test, expect } from '@playwright/test';

test.describe('Login', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('aula 24: entra com usuário e senha', async ({ page }) => {
    await page.getByTestId('username').fill(process.env.SAUCE_USER);
    await page.getByTestId('password').fill(process.env.SAUCE_PASSWORD);
    await page.getByTestId('login-button').click();
    await expect(page).toHaveURL(/inventory/);
    await expect(page.getByText('Products')).toBeVisible();
    await expect(page.getByText('Sauce Labs Backpack')).toContainText('Backpack');
    await expect(page.getByRole('button', { name: 'Add to cart' })).toHaveCount(6);
  });

  test('aula 24: mostra erro para usuário bloqueado', async ({ page }) => {
    await page.getByTestId('username').fill('locked_out_user');
    await page.getByTestId('password').fill(process.env.SAUCE_PASSWORD);
    await page.getByTestId('login-button').click();
    await expect(page.getByText('locked out')).toBeVisible();
  });
});
