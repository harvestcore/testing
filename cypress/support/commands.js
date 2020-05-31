Cypress.Commands.add('login', () => {
    Cypress.Cookies.debug(true);
    Cypress.Cookies.preserveOnce('ipm-token');

    cy.request({
      url: 'http://localhost:5000/api/login',
      headers: {
        'Authorization': 'Basic YWRtaW46YWRtaW4='
      }
    })
    .then((response) => {
      cy.setCookie('ipm-token', response.body.token);
    });
});
