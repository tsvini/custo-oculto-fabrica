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
});
