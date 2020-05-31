/// <reference types="cypress" />

context('Machines panel', () => {
  before(() => {
    cy.login();
  });

  it('Go to machines panel', () => {
    cy.getCookie('ipm-token').should('be.not.equal', null);
    cy.visit('http://localhost:4200/deploy');
  });

  it('check if main card exists', () => {
    cy.get('mat-card').contains('Deploy').should('exist');
  });

  it('check that main buttons exists', () => {
    cy.get('[mattooltip="Run containers"] > .mat-button-wrapper > .ng-fa-icon > .svg-inline--fa > path').should('exist');
    cy.get('[mattooltip="Refresh data"] > .mat-button-wrapper > .ng-fa-icon > .svg-inline--fa').should('exist');
    cy.get('.mat-warn > .mat-button-wrapper > .ng-fa-icon > .svg-inline--fa > path').should('exist');
  });

  it('check that filter exists', () => {
    cy.get('mat-label').contains('Filter').should('exist');
    cy.get('[icon="times"]').should('exist');
  });

  it('check that columns selector exists', () => {
    cy.get('mat-label').contains('Columns').should('exist');
    cy.get('mat-select').should('exist');
  });

  it('ensure that there are no containers', () => {
    // Remove any possible second user
    cy.get('.mat-warn').click();
    cy.get('.mat-dialog-actions > .mat-warn').click();
    cy.wait(500);
  });

  it('check images buttons and go back containers', () => {
    // Remove any possible second user
    cy.get('#mat-tab-label-0-1').click();
    cy.wait(500);

    cy.get('[mattooltip="Search and pull images"] > .mat-button-wrapper > .ng-fa-icon > .svg-inline--fa > path').should('exist');
    cy.get('[mattooltip="Refresh data"] > .mat-button-wrapper > .ng-fa-icon > .svg-inline--fa').should('exist');
    cy.get('.imageButtons > .mat-warn > .mat-button-wrapper > .ng-fa-icon > .svg-inline--fa > path').should('exist');

    cy.get('#mat-tab-label-0-0').click();
  });

  it('download image and run it, after that go back to containers', () => {
    // Remove any possible second user
    cy.get('#mat-tab-label-0-1').click();
    cy.wait(500);

    cy.get('[mattooltip="Search and pull images"] > .mat-button-wrapper > .ng-fa-icon > .svg-inline--fa').click();
    cy.get('#searchTerm').type('harvestcore{enter}');
    cy.get('.table > app-ipmtable.ng-star-inserted > .mat-table > tbody > :nth-child(1) > .cdk-column-actions > div.ng-star-inserted > .mat-focus-indicator > .mat-button-wrapper > .ng-fa-icon > .svg-inline--fa').click();
    cy.wait(5000);
    cy.get('.mat-dialog-actions > .mat-focus-indicator > .mat-button-wrapper').click();

    cy.get('#mat-tab-label-0-0').click();
    cy.wait(500);
    cy.get('#mat-tab-label-0-1').click();
    cy.wait(500);
    cy.get('.cdk-column-tags > .mat-sort-header-container > .mat-sort-header-button').click();
    cy.wait(100);
    cy.get(':nth-child(1) > .cdk-column-actions > div.ng-star-inserted > .mat-accent').click();

    cy.get('#mat-tab-label-0-0').click();
    cy.wait(500);
  });

  it('manage container', () => {
    cy.get('td').contains('running').should('exist');
    cy.get('.cdk-column-image_tag > .mat-sort-header-container > .mat-sort-header-button').click();
    cy.get(':nth-child(1) > .cdk-column-actions > div.ng-star-inserted > .mat-focus-indicator').click();

    cy.get('button').contains('Pause').click();
    cy.wait(1000);
    cy.get('button').contains('Unpause').click();
    cy.wait(1000);
    cy.get('button').contains('Kill').click();
    cy.wait(1000);
    cy.get('button').contains('Restart').click();
    cy.wait(1000);
    cy.get('button').contains('Stop').click();
    cy.wait(10000);
    cy.get('button').contains('Restart').click();
    cy.get('button').contains('Restart').click();
    cy.wait(1000);
    cy.get('button').contains('Close').click();
    cy.wait(500);
  });

  it('rename container', () => {
    cy.get('#mat-tab-label-0-1').click();
    cy.wait(500);
    cy.get('#mat-tab-label-0-0').click();
    cy.wait(500);
    cy.get('td').contains('running').should('exist');
    cy.get('.cdk-column-image_tag > .mat-sort-header-container > .mat-sort-header-button').click();
    cy.wait(500);
    cy.get(':nth-child(1) > .cdk-column-actions > div.ng-star-inserted > .mat-focus-indicator').click();
    cy.wait(500);
    cy.get('#mat-expansion-panel-header-4 > .mat-content > .mat-expansion-panel-header-title').click();
    cy.get('#name').clear();
    cy.get('#name').type('testing_container');
    cy.get('[icon="check"]').click();
    cy.wait(250);
    cy.get('#mat-dialog-title-3').contains('testing_container').should('exist');
    cy.get('button').contains('Close').click();
    cy.wait(250);
  });

  it('kill container and prune', () => {
    cy.get('#mat-tab-label-0-1').click();
    cy.wait(500);
    cy.get('#mat-tab-label-0-0').click();
    cy.wait(500);
    cy.get('td').contains('running').should('exist');
    cy.get('.cdk-column-image_tag > .mat-sort-header-container > .mat-sort-header-button').click();
    cy.wait(500);
    cy.get(':nth-child(1) > .cdk-column-actions > div.ng-star-inserted > .mat-focus-indicator').click();
    cy.wait(500);
    cy.get('button').contains('Kill').click();
    cy.wait(1000);
    cy.get('button').contains('Close').click();
    cy.wait(250);
    cy.get('.mat-warn').click();
    cy.get('.mat-dialog-actions > .mat-warn').click();
    cy.wait(500);
  });
});
