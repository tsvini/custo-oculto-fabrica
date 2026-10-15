// Aulas 9 a 14, 20 e 21
describe('Login', () => {
  beforeEach(() => {
    cy.visit('https://www.saucedemo.com')
  })

  it('entra com usuário e senha', () => {
    cy.get('[data-test="username"]').type('standard_user')
    cy.get('[data-test="password"]').type('secret_sauce')
    cy.get('[data-test="login-button"]').click()
    cy.contains('Products').should('be.visible')
  })

  it('mostra erro para usuário bloqueado', () => {
    cy.get('[data-test="username"]').type('locked_out_user')
    cy.get('[data-test="password"]').type('secret_sauce')
    cy.get('[data-test="login-button"]').click()
    cy.get('[data-test="error"]')
      .should('contain', 'locked out')
  })

  // Desafio 1 (aula 20)
  it('mostra erro com senha errada', () => {
    cy.get('[data-test="username"]').type('standard_user')
    cy.get('[data-test="password"]').type('senha_errada')
    cy.get('[data-test="login-button"]').click()
    cy.get('[data-test="error"]')
      .should('contain', 'do not match')
  })

  // Desafio 2 (aula 21)
  it('pede o usuário quando os campos estão vazios', () => {
    cy.get('[data-test="login-button"]').click()
    cy.get('[data-test="error"]')
      .should('contain', 'Username is required')
  })
})
