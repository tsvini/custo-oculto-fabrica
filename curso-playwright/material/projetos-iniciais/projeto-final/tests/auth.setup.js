import { test as setup, expect } from '@playwright/test';

const arquivoLogin = 'playwright/.auth/usuario.json';

setup('faz login uma vez', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('username').fill(process.env.SAUCE_USER);
  await page.getByTestId('password').fill(process.env.SAUCE_PASSWORD);
  await page.getByTestId('login-button').click();
  await expect(page.getByTestId('title')).toHaveText('Products');
  await page.context().storageState({ path: arquivoLogin });
});
