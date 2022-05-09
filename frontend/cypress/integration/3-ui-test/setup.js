describe('Logging into the system', () => {
    before(function() {
        // create a fabricated user from a fixture
        cy.fixture('user.json')
            .then((user) => {
                cy.request({
                    method: 'POST',
                    url: 'http://localhost:5000/users/create',
                    form: true,
                    body: user
                }).then((response) => {
                    this.uid = response.body._id.$oid

                    // create one fabricated task for that user
                    cy.fixture('task.json')
                        .then((task) => {
                            // add the user id to the data of the task object
                            task.userid = this.uid
                            cy.request({
                                method: 'POST',
                                url: 'http://localhost:5000/tasks/create',
                                form: true,
                                body: task
                            }).then((response) => {
                                this.tid = response.body
                            })
                        })
                })
            })
        cy.visit('http://localhost:3000/')

        // alternative, imperative way of detecting that input field
        cy.get('.inputwrapper #email')
        .type('mon.doe@gmail.com')

        // submit the form on this page
        cy.get('form')
            .submit()
        
        // view task in detail mode
        cy.get(".title-overlay")
        .first()
        .click()
    })

    it('view task in detail mode', () => {
        cy.get('.popup').should('be.visible')
      })


    after(function() {
        // clean up by deleting the user from the database
        cy.request({
            method: 'DELETE',
            url: `http://localhost:5000/users/${this.uid}`
        }).then((response) => {
            cy.log(response.body)
        })
    })
})
