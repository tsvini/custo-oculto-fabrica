import { test, expect } from '@playwright/test';

const lojinha = 'https://tsvini.github.io/custo-oculto-fabrica/loja/';

test('aula 67: a tela de login não mudou', async ({ page }) => {
  await page.goto(lojinha);
  await expect(page).toHaveScreenshot('login.png');
});
