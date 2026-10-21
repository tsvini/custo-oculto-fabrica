const { test, expect } = require('@playwright/test');

const usuarios = ['standard_user', 'problem_user', 'performance_glitch_user', 'visual_user'];

for (const usuario of usuarios) {
  test(`login funciona para ${usuario}`, async ({ page }) => {
    await page.goto('/');
    await page.getByTestId('username').fill(usuario);
    await page.getByTestId('password').fill(process.env.SAUCE_PASSWORD);
    await page.getByTestId('login-button').click();
    await expect(page.getByTestId('title')).toHaveText('Products');
  });
}
