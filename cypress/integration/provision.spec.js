/// <reference types="cypress" />

context('Provision panel', () => {
  before(() => {
    cy.login();
  });

  it('Go to provision panel', () => {
    cy.getCookie('ipm-token').should('be.not.equal', null);
    cy.visit('http://localhost:4200/provision');
  });

  it('check if main card exists', () => {
    cy.get('mat-card').contains('Provision').should('exist');
  });

  it('check that main buttons exists', () => {
    cy.get('[icon="plus"]').should('exist');
    cy.get('[icon="sync"]').should('exist');
  });

  it('create host group', () => {
    cy.get('#mat-tab-label-0-2 > .mat-tab-label-content').click();
    cy.wait(500);

    cy.get('[icon="plus"]').click();

    // check all fields
    cy.get('mat-label').contains('Name').should('exist');
    cy.get('mat-label').contains('IP').should('exist');

    // set data
    cy.get('#name').type('aaaa-testing-host-group');

    cy.get('button').contains('Create').click();
    cy.get('.mat-select-placeholder').click();
    cy.get('span').contains('t1').click();
    cy.wait(150);

    cy.get('h4').contains('Selected IPs: 1').should('exist');
    cy.get('button').contains('Create').click();

    // Check that the user is updated
    cy.wait(250);
    cy.get('td').contains('aaaa-testing-host-group').should('exist');
  });

  it('edit host group', () => {
    cy.get('.cdk-column-name > .mat-sort-header-container > .mat-sort-header-button').click();
    cy.wait(150);
    cy.get(':nth-child(1) > .cdk-column-actions > div.ng-star-inserted > .mat-primary').click();
    cy.wait(250);

    cy.get('#name').clear();
    cy.get('#name').type('aaaa-aa-testing-host-group');
    cy.wait(150);

    cy.get('button').contains('Save').click();
  });

  it('create playbook', () => {
    cy.get('#mat-tab-label-0-0').click();
    cy.wait(500);

    cy.get('[icon="plus"]').click();
    cy.wait(500);

    cy.get('.view-line').type('---\n' +
        '- name: Testing playbook\n' +
        '  hosts: all\n' +
        'tasks:\n' +
        '  - name: Show msg\n' +
        '  debug:\n' +
        'msg: "This is a test"');


    cy.get('[icon="save"]').click();
    cy.wait(150);

    cy.get('#name').type('a-testing-playbook');
    cy.get('.mat-select-placeholder').click();
    cy.get('span').contains('aaaa-testing-host-group').click();
    cy.get('button').contains('Create').click();
    cy.wait(250);
  });

  it('run playbook', () => {
    cy.get('#mat-tab-label-0-0').click();
    cy.wait(500);

    cy.get('.cdk-column-name > .mat-sort-header-container > .mat-sort-header-button').click();
    cy.wait(150);

    cy.get(':nth-child(1) > .cdk-column-actions > div.ng-star-inserted > .mat-accent').click();
    cy.wait(150);

    cy.get('h3').contains('Running playbook').should('exist');
    cy.wait(1000);

    cy.get('button').contains('Ok').click();
    cy.wait(250);
  });
});
