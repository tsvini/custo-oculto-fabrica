import { test, expect } from '../../fixtures/paginas';
import usuarios from '../../dados/usuarios.json';

const lojinha = 'https://tsvini.github.io/custo-oculto-fabrica/loja';

test('aula 64: o loginPage chega pronto', async ({ page, loginPage }) => {
  await page.goto('/');
  await loginPage.entrar(process.env.SAUCE_USER, process.env.SAUCE_PASSWORD);
  await expect(page.getByTestId('title')).toHaveText('Products');
});

for (const { usuario, resultado } of usuarios) {
  test(`aula 65: ${usuario} - ${resultado}`, async ({ page, loginPage }) => {
    await page.goto('/');
    await loginPage.entrar(usuario, process.env.SAUCE_PASSWORD);
    if (resultado === 'sucesso') {
      await expect(page.getByTestId('title')).toHaveText('Products');
    } else {
      await expect(loginPage.erro).toContainText('locked out');
    }
  });
}

test.describe('aula 66: mock na Lojinha do Leigo', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(`${lojinha}/`);
    await page.getByTestId('usuario').fill('cliente');
    await page.getByTestId('senha').fill('leigo123');
    await page.getByTestId('entrar').click();
    await expect(page.getByTestId('produto').first()).toBeVisible();
  });

  test('servidor fora do ar', async ({ page }) => {
    await page.route('**/api/produtos.json', (route) => route.abort());
    await page.reload();
    await expect(page.getByTestId('erro-carregar')).toBeVisible();
  });

  test('lista vazia', async ({ page }) => {
    await page.route('**/api/produtos.json', (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: '[]' }));
    await page.reload();
    await expect(page.getByTestId('vazio')).toHaveText('Nenhum produto encontrado.');
  });
});

test('aula 67: teste visual', async ({ page }) => {
  await page.goto(`${lojinha}/`);
  await expect(page).toHaveScreenshot('login.png', { maxDiffPixelRatio: 0.02 });
});

test('aula 68: soft assertions', async ({ page }) => {
  test.fail(); // duas conferências erradas de propósito: o teste falha, mas mostra as duas
  await page.goto(`${lojinha}/`);
  await expect.soft(page.getByTestId('entrar')).toHaveText('Login');
  await expect.soft(page.getByTestId('usuario')).toHaveAttribute('placeholder', 'Seu usuário');
  await expect.soft(page.getByTestId('senha')).toHaveAttribute('placeholder', 'Password');
});

test('aula 69: login funciona', { tag: '@smoke' }, async ({ page, loginPage }) => {
  await page.goto('/');
  await loginPage.entrar(process.env.SAUCE_USER, process.env.SAUCE_PASSWORD);
  await expect(page).toHaveURL(/inventory/);
});

test('aula 70: usuário lento, esperando o que importa', async ({ page, loginPage }) => {
  await page.goto('/');
  await loginPage.entrar('performance_glitch_user', process.env.SAUCE_PASSWORD);
  await expect(page.getByTestId('inventory-item').first()).toBeVisible({ timeout: 15000 });
});
