/// <reference types="cypress" />

context('Status', () => {
  before(() => {
    cy.login();
  });

  it('Go home', () => {
    cy.getCookie('ipm-token').should('be.not.equal', null);
    cy.visit('http://localhost:4200');
  });

  it('check that docker card exists', () => {
    cy.get('mat-card').contains('Docker service').should('exist');
  });

  it('check that mongo card exists', () => {
    cy.get('mat-card').contains('Mongo service').should('exist');
  });

  it('check that mongo card has its fields', () => {
    cy.get('mat-list-item').contains('Customers').should('exist');
    cy.get('mat-list-item').contains('Users in current customer').should('exist');
    cy.get('mat-list-item').contains('Databases').should('exist');
  });

  it('check that docker card exists', () => {
    cy.get('mat-card').contains('Docker service').should('exist');
  });

  it('check that the user button exists', () => {
    cy.get('button').contains('admin (').should('exist');
  });

  it('check that the logout button exists', () => {
    cy.get('button').contains('admin (').click();
    cy.get('button').contains('Logout').should('exist');
  });

  it('check that the admin user button exists', () => {
    cy.get('button').contains('Admin').should('exist');
  });

  it('check that the home button exists', () => {
    cy.get('button').contains('IPManager').should('exist');
  });

  it('check that the deploy button exists', () => {
    cy.get('button').contains('Deploy').should('exist');
  });

  it('check that the provision button exists', () => {
    cy.get('button').contains('Provision').should('exist');
  });

  it('check that the machines button exists', () => {
    cy.get('button').contains('Machines').should('exist');
  });
})
