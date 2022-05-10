describe('Test todo', () => {
    let todoid;
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
                                // tid = this.tid;
                                cy.log(response.body[0].todos[0]._id.$oid)
                                todoid = response.body[0].todos[0]._id.$oid
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

    it('R8UC1 #1 can add new todo item to list of one', () => {
        // test that input is empty
        cy.get('.todo-list input[type=text]').should('have.value', '');

        const newItem = 'Take notes'

        cy.get('.todo-list')
        .find('input[type=text]').type(`${newItem}{enter}`)

        cy.get('.todo-item')
        .should('have.length', 2)
        .eq(1)
        .should('have.text', `${newItem}✖`)
    })

    /* Failing test
    Add button is disabled
    red border does not appear when clicking add button,
    since button can't be clicked
    */
    it('R8UC1 #2 attempting to add todo with empty input field', () => {
        // test that input is empty
        cy.get('.todo-list input[type=text]').should('have.value', '');

        // Fails because element is disabled
        cy.get('.todo-list')
        .find('input[type=submit]')
        .invoke('attr', 'disabled')
        .then(disabled =>{
            disabled ? cy.get('.todo-list').find('input[type=submit]').click() : cy.log('buttonIsNotDiabled')
        })

        // Not executed, todo should not be added
        cy.get('.todo-item')
        .should('have.length', 2)

        // Not executed, red border should appear
        cy.get('.todo-list')
        .find('input[type=text]')
        .should('have.css', 'border-color', 'red')
    })

    /* Failing test
    Fails if viewport is not edited
    This element <input> is not visible because its ancestor has position: fixed
    CSS property and it is overflowed by other elements.*/
    it('R8UC1 #3 can add new todo item to list of two', () => {
        // cy.viewport(1536, 960)
        const newItem = 'Discuss topic'
        cy.get('.todo-list')
        .find('input[type=text]').type(`${newItem}{enter}`)
    
        cy.get('.todo-item')
        .should('have.length', 3)
        .eq(2)
        .should('have.text', `${newItem}✖`)
    })

    /* Sometimes failing test
    AssertionError: Expected .editable to have CSS property 'text-decoration'
    with the value 'line-through' but the value was 'none'. */
    it('R8UC2 #1 Set todo item to done and check if todo item is struck through', () => {
        cy.get('.todo-item')
        .first()
        .find('.checker')
        .click()
        .then(() => {
            cy.get('.todo-item > .editable')
                .first()
                .should('have.css', 'text-decoration', 'line-through solid rgb(49, 46, 46)')
        })
    })

    /* Sometimes failing test
    // AssertionError: Expected .editable to have CSS property 'text-decoration'
    with the value 'none' but the value was 'line-through' */
    it('R8UC2 #2 Set todo item to active and check if todo item is not struck through', () => {
        cy.get('.todo-item')
        .first()
        .find('.checker')
        .click()
        .then(() => {
            cy.get('.todo-item > .editable')
                .first()
                .should('have.css', 'text-decoration', 'none solid rgb(49, 46, 46)')
        })
    })

    it('R8UC3 #1 attempting to delete todo item from todo list', () => {
        cy.get('.todo-item')
        .last()
        .find('.remover')
        .click()
        .then(() => {
            cy.get('.todo-item')
            .should('have.length', 1)
        })
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
