export class LoginPage {
  constructor(page) {
    this.page = page;
    this.usuario = page.getByTestId('username');
    this.senha = page.getByTestId('password');
    this.botaoLogin = page.getByTestId('login-button');
    this.erro = page.getByTestId('error');
  }

  async abrir() {
    await this.page.goto('/');
  }

  async entrar(usuario, senha) {
    await this.usuario.fill(usuario);
    await this.senha.fill(senha);
    await this.botaoLogin.click();
  }
}

