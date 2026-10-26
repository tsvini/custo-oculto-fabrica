import { test, expect } from '@playwright/test';
import { LoginPage } from '../../pages/LoginPage';

test.describe('Login', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('aula 39: entra com usuário e senha', async ({ page }) => {
    const login = new LoginPage(page);
    await login.entrar(process.env.SAUCE_USER, process.env.SAUCE_PASSWORD);
    await expect(page).toHaveURL(/inventory/);
    await expect(page.getByTestId('title')).toHaveText('Products');
  });

  test('aula 39: mostra erro para usuário bloqueado', async ({ page }) => {
    const login = new LoginPage(page);
    await login.entrar('locked_out_user', process.env.SAUCE_PASSWORD);
    await expect(login.erro).toContainText('locked out');
  });
});
