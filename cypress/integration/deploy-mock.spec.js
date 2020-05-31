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
  });
  