import { test, expect } from '@playwright/test';

const usuarios = ['standard_user', 'problem_user', 'performance_glitch_user', 'visual_user'];

for (const usuario of usuarios) {
  test(`aula 32: login funciona para ${usuario}`, async ({ page }) => {
    await page.goto('/');
    await page.getByTestId('username').fill(usuario);
    await page.getByTestId('password').fill(process.env.SAUCE_PASSWORD);
    await page.getByTestId('login-button').click();
    // o performance_glitch_user é lento de propósito: damos 10 segundos em vez de 5
    await expect(page.getByTestId('title')).toHaveText('Products', { timeout: 10000 });
  });
}
