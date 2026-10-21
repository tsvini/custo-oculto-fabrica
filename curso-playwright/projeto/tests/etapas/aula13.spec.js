import { test, expect } from '@playwright/test';

test('aula 13: entra com usuário e senha', async ({ page }) => {
  await page.goto('https://www.saucedemo.com/');
});
