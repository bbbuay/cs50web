document.addEventListener('DOMContentLoaded', () => {

    // For update schedule part
    document.querySelectorAll('.schedule-item span').forEach((span) => {
        span.addEventListener('click', function (event) {
            event.stopPropagation();
        });
    });

    document.querySelectorAll('.schedule-item').forEach((li) => {
        li.addEventListener('click', update_schedule)
    });

    // For update todo and top priorities part
    document.querySelectorAll('.todo-item label').forEach((label) => {
        label.addEventListener('click', function (event) {
            event.stopPropagation();
        });
    });

    document.querySelectorAll('.todo-item').forEach((li) => {
        li.addEventListener('click', update_todo)
    });

    document.querySelector('.new-schedule-button').addEventListener('click', function () {
        // clear all html form calue in modal body
        $('#schedule-popup-form').on('shown.bs.modal', function () {
            $('#schedule_name').val('');
            $('#start-hours').val('00');
            $('#start-mins').val('00');
            $('#end-hours').val('00');
            $('#end-mins').val('00');
            document.querySelector('input[name="color"][value="#F7A4A4"]').checked = true
        });


        //hide "Save Changes" button and show "Add New Schedule" button
        document.querySelector('.add-schedule-button').style.display = 'block';
        document.querySelector('.update-schedule-button').style.display = 'none';
    });

    document.querySelector('.update-schedule-button').addEventListener('click', function () {

        const schedule_button = document.querySelector('.update-schedule-button');
        // get schedule id from the value that coming with clicked button
        const schedule_id = schedule_button.value;
        console.log(schedule_id);

        // get new data by using querySelector (select by ID)
        const schedule_name = document.querySelector('#schedule_name').value;
        const schedule_date = document.querySelector('#date-selected').value;
        const start_hours = document.querySelector('#start-hours').value;
        const start_mins = document.querySelector('#start-mins').value;
        const end_hours = document.querySelector('#end-hours').value;
        const end_mins = document.querySelector('#end-mins').value;
        const bg_hex_color = document.querySelector('input[name="color"]:checked').value;

        const csrf_token = document.querySelector('#schedule-form').querySelector('input').value;

        // update schedule
        fetch(`/schedule/${schedule_id}`, {
            method: 'PUT',
            headers: {
                "X-CSRFToken": csrf_token,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                schedule_name: schedule_name,
                date: schedule_date,
                start_hours: start_hours,
                end_hours: end_hours,
                start_mins: start_mins,
                end_mins: end_mins,
                bg_hex_color: bg_hex_color,
            })
        })
            .then((response) => {
                console.log(response);
                // hide the modal
                $('#schedule-popup-form').modal('hide');
                // load the current page
                location.reload();
            })

    });

    // Listen for all checkbox inputs that were checked
    checkboxs = document.querySelectorAll('.todo-task');
    checkboxs.forEach(function (checkbox) {
        checkbox.addEventListener('change', function () {

            // get data 
            const todo_id = this.value;
            const todo_form = document.querySelector('#todo-form');
            const csrf_token = todo_form.querySelector('input').value;

            // Check if : the checkbox is checked or not
            if (this.checked) {
                console.log(todo_id, todo_form, csrf_token)

                // update : this todo task is done
                fetch(`/todo/${todo_id}`, {
                    method: 'PUT',
                    headers: {
                        "X-CSRFToken": csrf_token,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        is_done: true,
                    })
                })
                    .then((response) => {
                        console.log(response)
                    })

            } else {
                console.log(todo_id, todo_form, csrf_token)

                // update : this todo task is not done
                fetch(`/todo/${todo_id}`, {
                    method: 'PUT',
                    headers: {
                        "X-CSRFToken": csrf_token,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        is_done: false,
                    })
                })
                    .then((response) => {
                        console.log(response)
                    })

            }
        });
    });

    document.querySelector('#new-todo-button').addEventListener('click', function () {
        // hide "Save Changes" button and show "Add New Schedule" button
        document.querySelector('.update-todo-button').style.display = 'none';
        document.querySelector('.add-todo-button').style.display = 'block';

        $('#add-todo').on('shown.bs.modal', function () {
            $('#todo-task').val('');
        });

    });


    document.querySelector('.update-todo-button').addEventListener('click', function () {
        const todo_button = document.querySelector('.update-todo-button');
        // get schedule id from the value that coming with clicked button
        const todo_id = todo_button.value;

        // get new data by using querySelector (select by ID)
        const todo_name = document.querySelector('#todo-task').value;
        const todo_date = document.querySelector('#todo-date').value;
        const is_toppriorities = document.querySelector('#top-priorities').checked;

        const csrf_token = document.querySelector('#todo-form').querySelector('input').value;

        // update todo task
        fetch(`/todo/${todo_id}`, {
            method: 'PUT',
            headers: {
                "X-CSRFToken": csrf_token,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                todo_name: todo_name,
                date: todo_date,
                is_toppriorities: is_toppriorities,
            })
        })
            .then((response) => {
                console.log(response);
                // hide the modal
                $('#schedule-popup-form').modal('hide');
                // load the current page
                location.reload();
            })

    });

    // Listen for write a note button is clicked
    document.querySelector('#write-note-button').addEventListener('click', edit_note)

    // Listen for "Save Changes" button in Note Modal
    document.querySelector('#edit-note-button').addEventListener('click', save_changes_note)

});



function update_schedule(event) {
    const li = event.target;
    const schedule_id = li.dataset.id;
    const schedule_color = li.dataset.color;
    const schedule_date = li.dataset.date;
    const schedule_time = li.querySelector('.schedule-time').innerHTML.trim();
    const [start_time, end_time] = schedule_time.split(' - ');
    const [start_hours, start_mins] = start_time.split(':');
    const [end_hours, end_mins] = end_time.split(':');
    const schedule_name = li.querySelector('.schedule-name').innerHTML;

    // show "Save Changes" button and hide "Add New Schedule" button
    document.querySelector('.add-schedule-button').style.display = 'none';
    document.querySelector('.update-schedule-button').style.display = 'block';

    // add value to button to send value with it
    const schedule_button = document.querySelector('.update-schedule-button');
    schedule_button.value = schedule_id;

    console.log(schedule_color, schedule_id, schedule_date)
    console.log(schedule_name);

    // show the old data
    $('#schedule-popup-form').modal('show');
    $('#schedule-popup-form').on('shown.bs.modal', function () {
        $('#schedule_name').val(schedule_name);
        $('#start-hours').val(start_hours);
        $('#start-mins').val(start_mins);
        $('#end-hours').val(end_hours);
        $('#end-mins').val(end_mins);

        // Use the querySelector method to select the specific radio button
        const radioButton = document.querySelector(`input[name="color"][value="${schedule_color}"]`);

        // Set the checked attribute of the radio button to true
        radioButton.checked = true;

    });
}


function update_todo(event) {
    const li = event.target;
    // todo id coming with the input value
    const todo_id = li.querySelector('input').value;

    // add value to button to send value with it
    const todo_button = document.querySelector('.update-todo-button');
    todo_button.value = todo_id;

    // show "Save Changes" button and hide "Add New Schedule" button
    document.querySelector('.add-todo-button').style.display = 'none';
    document.querySelector('.update-todo-button').style.display = 'block'

    // Get data
    fetch(`/todo/${todo_id}`)
        .then(response => response.json())
        .then(todo => {
            // Define Variable for using in the next step
            const todo_name = todo.name;
            const todo_date = todo.date;
            const todo_top = todo.is_toppriorities;
            // show modal with prefilled data
            $('#add-todo').modal('show');
            $('#add-todo').on('shown.bs.modal', function () {
                $('#todo-task').val(todo_name);
                $('#todo-date').val(todo_date);
                if (todo_top === true) {
                    document.querySelector('#top-priorities').checked = true;
                };
            });
        });

}

function edit_note() {
    const write_note_button = document.querySelector('#write-note-button');
    const note_id = write_note_button.value;


    // Get data by using fetch
    fetch(`/note/${note_id}`)
        .then(response => response.json())
        .then(note => {
            note_content = note.content;
            date = note.date;

            // show modal and prefilled data
            $('#notesModal').modal('show');
            $('#notesModal').on('shown.bs.modal', function () {
                $('#note-date').val(date);

                // fill note_content in textarea in modal
                document.querySelector('#note_content').innerHTML = note_content;
            });
        })
}


function save_changes_note() {
    // get new value from form
    const note_id = document.querySelector('#edit-note-button').value;
    const note_date = document.querySelector('#note-date').value;
    const note_content = document.querySelector('#note_content').value;
    const csrf_token = document.querySelector('#note-form').querySelector('input').value;

    // update new value using fetch
    fetch(`/note/${note_id}`, {
        method: 'PUT',
        headers: {
            "X-CSRFToken": csrf_token,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            note_content: note_content,
            date: note_date,
        })
    })
        .then((response) => {
            console.log(response)

            // update front-end part
            document.querySelector("#note_content").innerHTML = note_content;
            document.querySelector(".card-text").innerHTML = note_content;

            // hide modals
            $('#notesModal').modal('hide');
        })
}