import { test, expect } from '@playwright/test';

// SONDA TEMPORÁRIA: o Practice Software Testing (Toolshop) serve pro curso?
test.describe('sonda toolshop', () => {
  test('home, data-test e login', async ({ page }) => {
    await page.goto('https://practicesoftwaretesting.com/');
    await expect(page.locator('[data-test="product-name"]').first()).toBeVisible({ timeout: 20000 });
    const home = await page.$$eval('[data-test]', (els) => [...new Set(els.map((e) => e.getAttribute('data-test').replace(/-01[A-Z0-9]+$/, '-ID')))].slice(0, 60));
    console.log('HOME data-test:', home.join(' | '));
    await page.goto('https://practicesoftwaretesting.com/auth/login');
    const login = await page.$$eval('[data-test]', (els) => els.map((e) => e.getAttribute('data-test')));
    console.log('LOGIN data-test:', login.join(' | '));
    await page.getByTestId('email').fill('customer@practicesoftwaretesting.com');
    await page.getByTestId('password').fill('welcome01');
    await page.getByTestId('login-submit').click();
    await expect(page.getByTestId('page-title')).toBeVisible({ timeout: 15000 });
    console.log('LOGADO:', await page.getByTestId('page-title').innerText(), page.url());
  });
  test('api', async ({ request }) => {
    const r = await request.get('https://api.practicesoftwaretesting.com/products');
    console.log('API products status', r.status());
    expect(r.ok()).toBeTruthy();
    const b = await r.json(); console.log('API keys', Object.keys(b).join(','), 'total', b.total);
    const l = await request.post('https://api.practicesoftwaretesting.com/users/login', { data: { email: 'customer@practicesoftwaretesting.com', password: 'welcome01' } });
    console.log('API login status', l.status());
  });
});
