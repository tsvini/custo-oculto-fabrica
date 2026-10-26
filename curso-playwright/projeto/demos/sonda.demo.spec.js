import { test, expect } from '@playwright/test';

// dados reais do site pras telas das aulas (XPath completo, classes, tempo do usuário lento)
test('sonda', async ({ page }) => {
  await page.goto('https://www.saucedemo.com/');
  const xp = await page.locator('#user-name').evaluate((el) => {
    const parte = (e) => { if (e === document.documentElement) return '/html'; const irmaos = [...e.parentNode.children].filter((x) => x.tagName === e.tagName); const i = irmaos.length > 1 ? '[' + (irmaos.indexOf(e) + 1) + ']' : ''; return parte(e.parentNode) + '/' + e.tagName.toLowerCase() + i; };
    return parte(el);
  });
  console.log('SONDA xpath=' + xp);
  console.log('SONDA xpath_conta=' + (await page.locator('xpath=' + xp).count()));
  console.log('SONDA classe_login=' + (await page.locator('#login-button').getAttribute('class')));
  console.log('SONDA attrs_user=' + JSON.stringify(await page.locator('#user-name').evaluate((e) => [...e.attributes].map((a) => [a.name, a.value]))));
  await page.getByPlaceholder('Username').fill('performance_glitch_user');
  await page.getByPlaceholder('Password').fill('secret_sauce');
  const t0 = Date.now();
  await page.getByRole('button', { name: 'Login' }).click();
  await expect(page).toHaveURL(/inventory/, { timeout: 20000 });
  console.log('SONDA glitch_ms=' + (Date.now() - t0));
  console.log('SONDA botoes_produtos=' + (await page.getByRole('button').count()));
  await expect(page.locator('xpath=' + xp)).toHaveCount(0);
});
