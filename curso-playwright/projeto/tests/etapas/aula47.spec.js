import { test, expect } from '@playwright/test';

test('aula 47: busca um post', async ({ request }) => {
  const resposta = await request.get('https://jsonplaceholder.typicode.com/posts/1');
  expect(resposta.status()).toBe(200);
  const post = await resposta.json();
  expect(post.id).toBe(1);
});
