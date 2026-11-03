// Testes da própria Lojinha do Leigo (não fazem parte do curso): tudo o que as aulas 66 a 80 usam, e mais um pouco.
const { defineConfig, devices } = require('@playwright/test');
module.exports = defineConfig({
  testDir: './tests',
  fullyParallel: true,
  retries: 0,
  reporter: [['list']],
  use: { baseURL: process.env.LOJA || 'https://tsvini.github.io/custo-oculto-fabrica/loja/', testIdAttribute: 'data-test' },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    { name: 'pixel7', use: { ...devices['Pixel 7'] } },
    { name: 'iphone13', use: { ...devices['iPhone 13'] } },
  ],
});
