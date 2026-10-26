import { test, expect } from '@playwright/test';

const lojinha = 'https://tsvini.github.io/custo-oculto-fabrica/loja/';
const api = '**/api/produtos.json';

test.beforeEach(async ({ page }) => {
  await page.goto(lojinha);
  await page.getByTestId('usuario').fill('cliente');
  await page.getByTestId('senha').fill('leigo123');
  await page.getByTestId('entrar').click();
  await expect(page.getByTestId('produto').first()).toBeVisible();
});

test('aula 66: servidor fora do ar', async ({ page }) => {
  await page.route(api, (route) => route.abort());
  await page.reload();
  await expect(page.getByTestId('erro-carregar')).toBeVisible();
});

test('aula 66: lista vazia', async ({ page }) => {
  await page.route(api, (route) => route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: '[]',
  }));
  await page.reload();
  await expect(page.getByTestId('vazio')).toBeVisible();
});
