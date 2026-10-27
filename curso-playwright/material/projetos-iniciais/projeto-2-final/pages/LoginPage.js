export class LoginPage {
  constructor(page) {
    this.page = page;
    this.usuario = page.getByTestId('usuario');
    this.senha = page.getByTestId('senha');
    this.botaoEntrar = page.getByTestId('entrar');
    this.erro = page.getByTestId('erro');
  }

  async abrir() {
    const v = process.env.LOJA_VERSAO;
    await this.page.goto(v ? `index.html?versao=${v}` : 'index.html');
  }

  async entrar(usuario, senha) {
    await this.usuario.fill(usuario);
    await this.senha.fill(senha);
    await this.botaoEntrar.click();
  }
}
