import { test, expect } from '@playwright/test';

test('entra com usuário e senha', async ({ page }) => {
  await page.goto('https://www.saucedemo.com/');
  await page.getByPlaceholder('Username').fill('standard_user');
  await page.getByPlaceholder('Password').fill('secret_sauce');
  await page.getByRole('button', { name: 'Login' }).click();
  await expect(page).toHaveURL(/inventory/);
  await expect(page.getByText('Products')).toBeVisible();
  await expect(page.getByText('Sauce Labs Backpack')).toContainText('Backpack');
  await expect(page.getByRole('button', { name: 'Add to cart' })).toHaveCount(6);
});
