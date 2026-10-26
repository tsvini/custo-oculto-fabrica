export class LoginPage {
  constructor(page) {
    this.page = page;
    this.usuario = page.getByTestId('usuario');
    this.senha = page.getByTestId('senha');
    this.botaoEntrar = page.getByTestId('entrar');
    this.erro = page.getByTestId('erro');
  }

  async abrir() {
    const versao = process.env.LOJA_VERSAO ? `?versao=${process.env.LOJA_VERSAO}` : '';
    await this.page.goto(`index.html${versao}`);
  }

  async entrar(usuario, senha) {
    await this.usuario.fill(usuario);
    await this.senha.fill(senha);
    await this.botaoEntrar.click();
  }
}
