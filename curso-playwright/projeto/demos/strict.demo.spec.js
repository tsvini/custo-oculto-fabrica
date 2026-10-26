import { test } from '@playwright/test';

// aula 18: erro de propósito (strict mode violation). Roda só com playwright.demos.config.js
test('clica no botão', async ({ page }) => {
  await page.goto('https://www.saucedemo.com/');
  await page.getByPlaceholder('Username').fill('standard_user');
  await page.getByPlaceholder('Password').fill('secret_sauce');
  await page.getByRole('button', { name: 'Login' }).click();
  await page.getByRole('button').click();
});
