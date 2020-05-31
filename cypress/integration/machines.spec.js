/// <reference types="cypress" />

context('Machines panel', () => {
  before(() => {
    cy.login();
  });

  it('Go to machines panel', () => {
    cy.getCookie('ipm-token').should('be.not.equal', null);
    cy.visit('http://localhost:4200/machines');
  });

  it('check if main card exists', () => {
    cy.get('mat-card').contains('Machines').should('exist');
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

  it('create machine', () => {
    cy.get('[icon="plus"]').click();

    // check all fields
    cy.get('mat-label').contains('Name').should('exist');
    cy.get('mat-label').contains('Type').should('exist');
    cy.get('mat-label').contains('Description').should('exist');
    cy.get('mat-label').contains('IPv4').should('exist');
    cy.get('mat-label').contains('IPv6').should('exist');
    cy.get('mat-label').contains('MAC').should('exist');
    cy.get('mat-label').contains('Gateway').should('exist');
    cy.get('mat-label').contains('Broadcast').should('exist');
    cy.get('mat-label').contains('Network').should('exist');
    cy.get('mat-label').contains('Netmask').should('exist');

    // set data
    cy.get('#name').type('aaaa-testing machine');
    cy.get('#type').click();
    cy.get('mat-option').contains('LOCAL').click();
    cy.get('#description').type('testing description');
    cy.get('#ipv4').type('192.168.1.10');
    cy.get('#ipv6').type('2001:db8:a0b:12f0::1');
    cy.get('#mac').type('00:0a:95:9d:68:16');
    cy.get('#gateway').type('192.168.1.1');
    cy.get('#broadcast').type('192.168.1.255');
    cy.get('#network').type('192.168.1.0');
    cy.get('#netmask').type('255.255.255.0');

    cy.get('button').contains('Create').click();
    cy.wait(500);

    // Check that the user is updated
    cy.get('td').contains('aaaa-testing machine').should('exist');
  });


  it('edit current machine', () => {
    cy.get('.cdk-column-name > .mat-sort-header-container > .mat-sort-header-button').click();
    cy.wait(500);
    cy.get(':nth-child(1) > .cdk-column-actions > div.ng-star-inserted > .mat-primary').click();

    // set data
    cy.get('#type').click();
    cy.get('mat-option').contains('REMOTE').click();
    cy.get('#gateway').clear();
    cy.get('#gateway').type('192.168.1.2');

    cy.get('button').contains('Save').click();
    cy.wait(500);

    cy.get('td').contains('remote').should('exist');
    cy.get('td').contains('192.168.1.2').should('exist');
  });

  it('remove machine', () => {
    cy.get('.cdk-column-name > .mat-sort-header-container > .mat-sort-header-button').click();
    cy.wait(500);

    // Remove any possible second user
    cy.get(':nth-child(1) > .cdk-column-actions > div.ng-star-inserted > .mat-warn').click();
    cy.get('.mat-dialog-actions > .mat-warn').click();
    cy.wait(500);
  });

  it('create machines', () => {
    cy.get('[icon="plus"]').click();

    // set data
    cy.get('#name').type('t1');
    cy.get('#type').click();
    cy.get('mat-option').contains('LOCAL').click();
    cy.get('#description').type('t1');
    cy.get('#ipv4').type('192.168.1.10');
    cy.get('#ipv6').type('2001:db8:a0b:12f0::1');
    cy.get('#mac').type('00:0a:95:9d:68:16');
    cy.get('#gateway').type('192.168.1.1');
    cy.get('#broadcast').type('192.168.1.255');
    cy.get('#network').type('192.168.1.0');
    cy.get('#netmask').type('255.255.255.0');

    cy.get('button').contains('Create').click();
    cy.wait(500);

    cy.get('[icon="plus"]').click();

    // set data
    cy.get('#name').type('t2');
    cy.get('#type').click();
    cy.get('mat-option').contains('LOCAL').click();
    cy.get('#description').type('t2');
    cy.get('#ipv4').type('192.168.1.20');
    cy.get('#ipv6').type('2001:db8:a0b:12f0::1');
    cy.get('#mac').type('00:0a:95:9d:68:16');
    cy.get('#gateway').type('192.168.1.1');
    cy.get('#broadcast').type('192.168.1.255');
    cy.get('#network').type('192.168.1.0');
    cy.get('#netmask').type('255.255.255.0');

    cy.get('button').contains('Create').click();
    cy.wait(500);
  });
});
