export class ProdutosPage {
  constructor(page) {
    this.page = page;
    this.titulo = page.getByTestId('titulo');
    this.ordenar = page.getByTestId('ordenar');
    this.produtos = page.getByTestId('produto');
    this.precos = page.getByTestId('preco');
    this.nomes = page.getByTestId('nome');
  }

  async ordenarPor(opcao) {
    await this.ordenar.selectOption(opcao);
  }

  // "R$ 1.234,56" vira 1234.56
  async lerPrecos() {
    const textos = await this.precos.allTextContents();
    return textos.map((t) => Number(
      t.replace('R$', '').replace(/\./g, '').replace(',', '.').trim(),
    ));
  }

  async lerNomes() {
    return this.nomes.allTextContents();
  }

  produto(nome) {
    return this.produtos.filter({ hasText: nome });
  }
}
