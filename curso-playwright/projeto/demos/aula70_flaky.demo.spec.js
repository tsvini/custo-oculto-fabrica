import { test, expect } from '@playwright/test';

// o jeito errado: tempo fixo. Às vezes os produtos já apareceram, às vezes não.
test('usuário lento, com tempo fixo', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('username').fill('performance_glitch_user');
  await page.getByTestId('password').fill('secret_sauce');
  await page.getByTestId('login-button').click();
  await page.waitForTimeout(4500);
  const produtos = page.getByTestId('inventory-item');
  expect(await produtos.count()).toBe(6);
});
