/// <reference types="cypress" />

context('Logout', () => {
  before(() => {
    cy.login();
  });

  it('Go home', () => {
    cy.getCookie('ipm-token').should('be.not.equal', null);
    cy.visit('http://localhost:4200');
  });

  it('click logout button', () => {
    cy.get('button').contains('admin (').click();
    cy.get('button').contains('Logout').click();
  });

  it('check that the cookie is removed', () => {
    cy.getCookie('ipm-token').should('be.equal', null);
  });

  it('check that there is no user button', () => {
    cy.get('button').contains('admin (').should('not.exist');
  });
})
