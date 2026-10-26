import { test, expect } from '@playwright/test';

const site = 'https://the-internet.herokuapp.com';

test('aula 56: checkbox e dropdown', async ({ page }) => {
  await page.goto(`${site}/checkboxes`);
  const primeira = page.getByRole('checkbox').first();
  await primeira.check();
  await expect(primeira).toBeChecked();
  await primeira.uncheck();
  await expect(primeira).not.toBeChecked();

  await page.goto(`${site}/dropdown`);
  const lista = page.locator('#dropdown');
  await lista.selectOption('2');
  await expect(lista).toHaveValue('2');
});

test('aula 57: upload de arquivo', async ({ page }) => {
  await page.goto(`${site}/upload`);
  await page.locator('#file-upload')
    .setInputFiles('arquivos/exemplo.txt');
  await page.locator('#file-submit').click();
  await expect(page.locator('#uploaded-files'))
    .toContainText('exemplo.txt');
});

test('aula 58: alerta do navegador', async ({ page }) => {
  await page.goto(`${site}/javascript_alerts`);
  page.on('dialog', async (dialog) => {
    await dialog.accept();
  });
  await page.getByRole('button', { name: 'Click for JS Alert' })
    .click();
  await expect(page.locator('#result'))
    .toHaveText('You successfully clicked an alert');
});

test('aula 59: nova aba', async ({ page }) => {
  await page.goto(`${site}/windows`);
  const promessa = page.waitForEvent('popup');
  await page.getByRole('link', { name: 'Click Here' }).click();
  const novaAba = await promessa;
  const titulo = novaAba.getByRole('heading', { name: 'New Window' });
  await expect(titulo).toBeVisible();
});

test('aula 60: iframe', async ({ page }) => {
  await page.goto(`${site}/iframe`);
  const editor = page.frameLocator('#mce_0_ifr');
  await expect(editor.locator('body'))
    .toContainText('Your content goes here.');
});

test('aula 61: hover', async ({ page }) => {
  await page.goto(`${site}/hovers`);
  const usuario = page.locator('.figure').first();
  const nome = usuario.getByText('name: user1');
  await expect(nome).not.toBeVisible();
  await usuario.hover();
  await expect(nome).toBeVisible();
});

test('aula 62: arrastar e soltar', async ({ page }) => {
  await page.goto(`${site}/drag_and_drop`);
  const caixaA = page.locator('#column-a');
  const caixaB = page.locator('#column-b');
  await caixaA.dragTo(caixaB);
  await expect(page.locator('#column-a header'))
    .toHaveText('B');
});

test('aula 63: tabela pelo conteúdo', async ({ page }) => {
  await page.goto(`${site}/tables`);
  const linha = page.locator('#table1')
    .getByRole('row')
    .filter({ hasText: 'Conway' });
  await expect(linha.getByRole('cell').nth(3))
    .toHaveText('$50.00');
});
