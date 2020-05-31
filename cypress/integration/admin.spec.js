/// <reference types="cypress" />

context('Admin panel', () => {
  before(() => {
    cy.login();
  });

  it('Go to admin panel', () => {
    cy.getCookie('ipm-token').should('be.not.equal', null);
    cy.visit('http://localhost:4200/admin');
  });

  it('check if main card exists', () => {
    cy.get('mat-card').contains('Users').should('exist');
  });

  it('check that main buttons exists', () => {
    cy.get('[icon="plus"]').should('exist');
    cy.get('[icon="sync"]').should('exist');
  });

  it('check that filter exists', () => {
    cy.get('mat-label').contains('Filter').should('exist');
    cy.get('[icon="times"]').should('exist');
  });

  it('check that columns selector exists', () => {
    cy.get('mat-label').contains('Columns').should('exist');
    cy.get('mat-select').should('exist');
  });

  it('check that current user exists', () => {
    cy.get('td').contains('admin').should('exist');
  });

  it('edit current user', () => {
    cy.get(':nth-child(1) > .cdk-column-actions > div.ng-star-inserted > .mat-primary').click();

    // check all fields
    cy.get('mat-label').contains('Type').should('exist');
    cy.get('mat-label').contains('Username').should('exist');
    cy.get('#username').should('have.value', 'admin');
    cy.get('mat-label').contains('Email').should('exist');
    cy.get('mat-label').contains('Public ID').should('exist');
    cy.get('#public_id').should('have.be', 'readonly');
    cy.get('mat-label').contains('First name').should('exist');
    cy.get('mat-label').contains('Last name').should('exist');

    // Update first name and last name
    cy.get('#first_name').clear();
    cy.get('#last_name').clear();
    cy.get('#password').clear();

    cy.get('#first_name').type('Admin name');
    cy.get('#last_name').type('Admin last name');
    cy.get('#password').type('admin');

    cy.get('#first_name').should('have.value', 'Admin name');
    cy.get('#last_name').should('have.value', 'Admin last name');
    cy.get('#password').should('have.value', 'admin');

    cy.get('button').contains('Save').click();
    cy.wait(500)

    // Check that the user is updated
    cy.get('td').contains('Admin name').should('exist');
    cy.get('td').contains('Admin last name').should('exist');
  });

  it('create user', () => {
    cy.get('[icon="plus"]').click();

    // check all fields
    cy.get('mat-label').contains('Type').should('exist');
    cy.get('mat-label').contains('Username').should('exist');
    cy.get('mat-label').contains('Email').should('exist');
    cy.get('mat-label').contains('First name').should('exist');
    cy.get('mat-label').contains('Last name').should('exist');

    cy.get('#type').click();
    cy.get('mat-option').contains('ADMIN').click();
    cy.get('#username').type('testing');
    cy.get('#password').type('testing');
    cy.get('#email').type('testing@testing.com');
    cy.get('#first_name').type('Test name');
    cy.get('#last_name').type('Test last name');

    cy.get('button').contains('Create').click();
    cy.wait(500);

    // Check that the user is updated
    cy.get('td').contains('Test name').should('exist');
    cy.get('td').contains('Test last name').should('exist');
  });

  it('remove user', () => {
    // Remove any possible second user
    cy.get(':nth-child(2) > .cdk-column-actions > div.ng-star-inserted > .mat-warn').click();
    cy.get('.mat-dialog-actions > .mat-warn').click();
    cy.wait(500);

    // Check that the user is deleted
    cy.get('td').contains('Test name').should('not.exist');
  });
});
