export class CheckoutPage {
  constructor(page) {
    this.page = page;
    this.botaoCheckout = page.getByTestId('checkout');
    this.nome = page.getByTestId('firstName');
    this.sobrenome = page.getByTestId('lastName');
    this.cep = page.getByTestId('postalCode');
    this.botaoContinuar = page.getByTestId('continue');
    this.botaoFinalizar = page.getByTestId('finish');
    this.mensagemFinal = page.getByTestId('complete-header');
  }

  async preencherDados(nome, sobrenome, cep) {
    await this.nome.fill(nome);
    await this.sobrenome.fill(sobrenome);
    await this.cep.fill(cep);
    await this.botaoContinuar.click();
  }
}

