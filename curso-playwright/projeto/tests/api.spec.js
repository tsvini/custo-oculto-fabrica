const { test, expect } = require('@playwright/test');

const api = 'https://jsonplaceholder.typicode.com';

test.describe('API de posts', () => {
  test('busca um post', async ({ request }) => {
    const resposta = await request.get(`${api}/posts/1`);
    expect(resposta.status()).toBe(200);
    const post = await resposta.json();
    expect(post.id).toBe(1);
  });

  test('cria um post', async ({ request }) => {
    const resposta = await request.post(`${api}/posts`, {
      data: { title: 'Meu primeiro post', body: 'Criado pelo Playwright', userId: 1 },
    });
    expect(resposta.status()).toBe(201);
    const post = await resposta.json();
    expect(post.title).toBe('Meu primeiro post');
  });

  test('apaga um post', async ({ request }) => {
    const resposta = await request.delete(`${api}/posts/1`);
    expect(resposta.status()).toBe(200);
  });
});
