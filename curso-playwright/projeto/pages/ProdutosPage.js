class ProdutosPage {
  constructor(page) {
    this.page = page;
    this.titulo = page.getByTestId('title');
    this.iconeCarrinho = page.getByTestId('shopping-cart-link');
    this.contadorCarrinho = page.getByTestId('shopping-cart-badge');
  }

  async abrir() {
    await this.page.goto('/inventory.html');
  }

  async adicionar(produto) {
    await this.page.getByTestId(`add-to-cart-${produto}`).click();
  }

  async irParaCarrinho() {
    await this.iconeCarrinho.click();
  }
}

module.exports = { ProdutosPage };
