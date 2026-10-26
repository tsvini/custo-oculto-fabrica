import { test, expect } from '../../fixtures/paginas';

test('aula 64: o loginPage chega pronto', async ({ page, loginPage }) => {
  await page.goto('/');
  await loginPage.entrar('standard_user', 'secret_sauce');
  await expect(page.getByTestId('title')).toHaveText('Products');
});
