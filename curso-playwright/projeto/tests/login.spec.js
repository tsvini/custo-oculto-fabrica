const { test, expect } = require('@playwright/test');
const { LoginPage } = require('../pages/LoginPage');

test.describe('Login', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('entra com usuário e senha', async ({ page }) => {
    const login = new LoginPage(page);
    await login.entrar(process.env.SAUCE_USER, process.env.SAUCE_PASSWORD);
    await expect(page).toHaveURL(/inventory/);
    await expect(page.getByTestId('title')).toHaveText('Products');
  });

  test('mostra erro para usuário bloqueado', async ({ page }) => {
    const login = new LoginPage(page);
    await login.entrar('locked_out_user', process.env.SAUCE_PASSWORD);
    await expect(login.erro).toContainText('locked out');
  });
});
