// só pras demonstrações de erro e sondas do curso (não faz parte do projeto do aluno)
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './demos',
  testMatch: /.*\.demo\.spec\.js/,
  reporter: 'list',
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
});
