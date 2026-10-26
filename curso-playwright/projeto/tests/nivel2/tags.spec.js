import { test, expect } from '../../fixtures/paginas';

test('aula 69: login funciona', { tag: '@smoke' }, async ({ page, loginPage }) => {
  await page.goto('/');
  await loginPage.entrar('standard_user', 'secret_sauce');
  await expect(page).toHaveURL(/inventory/);
});

test('aula 69: mostra erro para usuário bloqueado', async ({ page, loginPage }) => {
  await page.goto('/');
  await loginPage.entrar('locked_out_user', 'secret_sauce');
  await expect(loginPage.erro).toContainText('locked out');
});
