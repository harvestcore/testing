/// <reference types="cypress" />

context('Login', () => {
  beforeEach(() => {
    Cypress.Cookies.debug(true);
    Cypress.Cookies.preserveOnce('ipm-token');
  })

  it('Go home', () => {
    cy.visit('http://localhost:4200/login');
  });

  it('type wrong username', () => {
    cy.get('#username').type('test').should('have.value', 'test');
  });

  it('type wrong password', () => {
    cy.get('#password').type('test').should('have.value', 'test');
  });

  it('perform wrong login', () => {
    cy.contains('Login').click();
  });

  it('check feedback', () => {
    cy.get('mat-card-footer').contains('Login failed, please try again');
  });

  it('get token from backend and store it in cookies', () => {
    cy.request({
      url: 'http://localhost:5000/api/login',
      headers: {
        'Authorization': 'Basic YWRtaW46YWRtaW4='
      }
    })
    .then((response) => {
      expect(response).property('status').to.equal(200)
      expect(response).property('body').to.include.keys('token')

      cy.setCookie('ipm-token', response.body.token);
    });

  });

  it('check cookie', () => {
    cy.getCookie('ipm-token').should('be.not.equal', null);
  });

})
