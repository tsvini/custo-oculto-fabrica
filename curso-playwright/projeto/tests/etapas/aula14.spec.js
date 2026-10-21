import { test, expect } from '@playwright/test';

test('aula 14: entra com usuário e senha', async ({ page }) => {
  await page.goto('https://www.saucedemo.com/');
  await page.getByPlaceholder('Username').fill('standard_user');
  await page.getByPlaceholder('Password').fill('secret_sauce');
});
