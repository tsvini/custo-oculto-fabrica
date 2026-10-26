import { test as base } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { ProdutosPage } from '../pages/ProdutosPage';

export const test = base.extend({
  loginPage: async ({ page }, use) => {
    await use(new LoginPage(page));
  },
  produtosPage: async ({ page }, use) => {
    await use(new ProdutosPage(page));
  },
});

export { expect } from '@playwright/test';
