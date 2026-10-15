// Aulas 17 e 18, e os desafios 3 a 6 (aulas 22 a 25)
describe('Compra', () => {
  beforeEach(() => {
    cy.visit('https://www.saucedemo.com')
    cy.get('[data-test="username"]').type('standard_user')
    cy.get('[data-test="password"]').type('secret_sauce')
    cy.get('[data-test="login-button"]').click()
  })

  it('adiciona a mochila no carrinho', () => {
    cy.get('[data-test="add-to-cart-sauce-labs-backpack"]').click()
    cy.get('[data-test="shopping-cart-badge"]')
      .should('have.text', '1')
  })

  it('finaliza a compra', () => {
    cy.get('[data-test="add-to-cart-sauce-labs-backpack"]').click()
    cy.get('[data-test="shopping-cart-link"]').click()
    cy.get('[data-test="checkout"]').click()
    cy.get('[data-test="firstName"]').type('Maria')
    cy.get('[data-test="lastName"]').type('Silva')
    cy.get('[data-test="postalCode"]').type('88000-000')
    cy.get('[data-test="continue"]').click()
    cy.get('[data-test="finish"]').click()
    cy.contains('Thank you for your order!')
      .should('be.visible')
  })

  // Desafio 3 (aula 22)
  it('remove a mochila do carrinho', () => {
    cy.get('[data-test="add-to-cart-sauce-labs-backpack"]').click()
    cy.get('[data-test="remove-sauce-labs-backpack"]').click()
    cy.get('[data-test="shopping-cart-badge"]')
      .should('not.exist')
  })

  // Desafio 4 (aula 23)
  it('ordena do menor para o maior preço', () => {
    cy.get('[data-test="product-sort-container"]').select('lohi')
    cy.get('[data-test="inventory-item-price"]')
      .first()
      .should('have.text', '$7.99')
  })

  // Desafio 5 (aula 24)
  it('sai da conta', () => {
    cy.get('#react-burger-menu-btn').click()
    cy.get('[data-test="logout-sidebar-link"]').click()
    cy.get('[data-test="login-button"]').should('be.visible')
  })

  // Desafio 6 (aula 25)
  it('compra dois produtos', () => {
    cy.get('[data-test="add-to-cart-sauce-labs-backpack"]').click()
    cy.get('[data-test="add-to-cart-sauce-labs-bike-light"]').click()
    cy.get('[data-test="shopping-cart-badge"]').should('have.text', '2')
    cy.get('[data-test="shopping-cart-link"]').click()
    cy.get('[data-test="checkout"]').click()
    cy.get('[data-test="firstName"]').type('Maria')
    cy.get('[data-test="lastName"]').type('Silva')
    cy.get('[data-test="postalCode"]').type('88000-000')
    cy.get('[data-test="continue"]').click()
    cy.get('[data-test="finish"]').click()
    cy.contains('Thank you for your order!').should('be.visible')
  })
})
