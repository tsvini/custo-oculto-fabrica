import { test, expect } from '../../fixtures/paginas';
import usuarios from '../../dados/usuarios.json';

for (const { usuario, resultado } of usuarios) {
  test(`aula 65: ${usuario} - ${resultado}`, async ({ page, loginPage }) => {
    await page.goto('/');
    await loginPage.entrar(usuario, 'secret_sauce');
    if (resultado === 'sucesso') {
      await expect(page).toHaveURL(/inventory/);
    } else {
      await expect(loginPage.erro).toContainText('locked out');
    }
  });
}
