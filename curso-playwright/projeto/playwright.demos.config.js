// só pras demonstrações de erro e sondas do curso (não faz parte do projeto do aluno)
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './demos',
  testMatch: /.*\.demo\.spec\.js/,
  reporter: 'list',
  use: { baseURL: 'https://www.saucedemo.com', testIdAttribute: 'data-test' },  // igual ao projeto do aluno a partir da aula 23
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
});
