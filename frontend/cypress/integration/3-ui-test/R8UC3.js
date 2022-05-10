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
                                this.tid = response.body[0]._id.$oid
                            })
                            cy.fixture('todo.json')
                            .then((todo) => {
                                // add the task id to the data of the todo object
                                todo.taskid = this.tid
                                cy.request({
                                    method: 'POST',
                                    url: 'http://localhost:5000/todos/create',
                                    form: true,
                                    body: todo
                                }).then((response) => {
                                    cy.log(response.body[0])
                                })
                            })
                        })
                })
            })
        cy.visit('http://localhost:3000/')

        cy.contains('div', 'Email Address')
            .find('input[type=text]')
            .type('mon.doe@gmail.com')

        // submit the form on this page
        cy.get('form')
            .submit()
        
        // view task in detail mode
        cy.get("img")
        .first()
        .click()
    })

      it('R8UC3 #1 attempting to delete done todo item from todo list', () => {

        // cy.intercept('/todos/byid/*').as('todos')
        // cy.intercept('/tasks/byid/*').as('tasks')
        // cy.intercept('/tasks/ofuser/*').as('tasksByUser')
        cy.get('.todo-item')
        .last()
        .find('.remover')
        .click()

        // cy.wait(['@todos', '@tasks'])
        // cy.wait(['@tasksByUser'])
        cy.wait(1500)

        cy.get('.todo-item')
        .should('have.length', 1)
      })

      it('R8UC3 #2 attempting to delete active todo item from todo list', () => {
        cy.get('.todo-item')
        .last()
        .find('.remover')
        .click()

        cy.wait(1500)

        cy.get('.todo-item')
        .should('not.exist');
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
