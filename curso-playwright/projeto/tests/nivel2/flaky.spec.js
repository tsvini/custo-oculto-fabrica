import { test, expect } from '../../fixtures/paginas';

test('aula 70: usuário lento, esperando o que importa', async ({ page, loginPage }) => {
  await page.goto('/');
  await loginPage.entrar('performance_glitch_user', 'secret_sauce');
  const produtos = page.getByTestId('inventory-item');
  await expect(produtos.first()).toBeVisible({ timeout: 10000 });
});
