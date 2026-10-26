import { test, expect } from '../fixtures/paginas';
import ordenacoes from '../dados/ordenacao.json';

test.describe('Produtos', () => {
  test.beforeEach(async ({ loginPage, produtosPage }) => {
    await loginPage.abrir();
    await loginPage.entrar(process.env.LOJA_USUARIO, process.env.LOJA_SENHA);
    await expect(produtosPage.produtos.first()).toBeVisible();
  });

  for (const o of ordenacoes) {
    test(`ordena por ${o.nome}`, { tag: o.opcao === 'menor' ? ['@smoke'] : [] }, async ({ produtosPage }) => {
      await produtosPage.ordenarPor(o.opcao);
      const naTela = o.campo === 'preco' ? await produtosPage.lerPrecos() : await produtosPage.lerNomes();
      const esperado = [...naTela].sort((a, b) => (o.campo === 'preco' ? a - b : a.localeCompare(b)));
      if (o.sentido === 'decrescente') esperado.reverse();
      expect(naTela).toEqual(esperado);
    });
  }

  test('produto esgotado aparece, mas não dá pra comprar', async ({ produtosPage }) => {
    const camiseta = produtosPage.produto('Camiseta Passou no CI');
    await expect(camiseta.getByTestId('esgotado')).toBeVisible();
    await expect(camiseta.getByTestId('adicionar')).toBeDisabled();
  });
});
