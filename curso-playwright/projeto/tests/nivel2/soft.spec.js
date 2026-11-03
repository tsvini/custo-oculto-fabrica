import { test, expect } from '@playwright/test';

const lojinha = 'https://tsvini.github.io/custo-oculto-fabrica/loja/';

// a aula 68 mostra primeiro com Login e sem o not (erradas de propósito); este é o arquivo já corrigido
test('aula 68: os textos da tela de login', async ({ page }) => {
  await page.goto(lojinha);
  await expect.soft(page.getByTestId('entrar')).toHaveText('Entrar');
  await expect.soft(page.getByTestId('usuario')).toBeVisible();
  await expect.soft(page.getByTestId('senha')).toBeEmpty();
  await expect.soft(page.getByTestId('erro')).not.toBeVisible();
});
