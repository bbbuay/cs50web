document.addEventListener('DOMContentLoaded', () => {

    // Hide save change button in modal 
    document.querySelector('#save_event').style.display = 'none';

    document.querySelectorAll('.edit-event-button').forEach(function (button) {
        button.addEventListener('click', function (event) {
            const event_id = event.target.value;
            update_event(event_id);
        })
    });

    // listen for click "save button" in modal
    document.querySelector('#save_event').addEventListener('click', () => {

        // get new value that user change 
        const event_id = document.querySelector('#save_event').value;
        const event_name = document.querySelector('#event_name').value;
        const date = document.querySelector('#event_date').value;
        const start_time = document.querySelector('#start_time').value;
        const end_time = document.querySelector('#end_time').value;
        const csrf_token = document.querySelector('#event_form').querySelector('input').value;


        // update event object
        fetch(`/event/${event_id}`, {
            method: 'PUT',
            headers: {
                "X-CSRFToken": csrf_token,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                event_name: event_name,
                date: date,
                start_time: start_time,
                end_time: end_time
            })
        })
            .then((response) => {
                console.log(response)
                // hide modals
                $('#eventModal').modal('hide');

                location.reload();
            })

    });

    // listen for click "create event button" in modal
    document.querySelector('#create_event_button').addEventListener('click', () => {
        // hide save change button and show submit button
        document.querySelector('#save_event').style.display = 'none';
        document.querySelector('#event_submit_button').style.display = 'block';

        $('#eventModal').on('shown.bs.modal', function () {
            $('#event_name').val('');
            $('#event_date').val('');
            $('#start_time').val('');
            $('#end_time').val('');
        });
    })


});

function update_event(event_id) {
    // get data by using fetch
    fetch(`/event/${event_id}`)
        .then(response => response.json())
        .then(event => {
            console.log(event.name)
            const event_name = event.name;
            const date = event.date;
            const start_time = event.start_time;
            const end_time = event.end_time;

            // open modal 
            $('#eventModal').modal('show');
            $('#eventModal').on('shown.bs.modal', function () {
                $('#event_name').val(event_name);
                $('#event_date').val(date);
                $('#start_time').val(start_time);
                $('#end_time').val(end_time);
            });

            // show save change button and hide submit button
            document.querySelector('#save_event').style.display = 'block';
            document.querySelector('#event_submit_button').style.display = 'none';

            // add value to save change button 
            document.querySelector('#save_event').value = event_id;

        });

}
