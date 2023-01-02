document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // add function display_mail(mailbox)
  display_mail(mailbox);
}

function send_email(event) {
  event.preventDefault();
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  })
    .then(response => response.json())
    .then(result => {
      // Print result
      console.log(result);
      load_mailbox('sent');
    });
}

function create_display_div(email_id, html_content) {
  const div = document.createElement('div');
  div.className = "inner-each-email";
  div.innerHTML = `${html_content}`

  div.addEventListener('click', function () {

    // Show the email and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';

    // update : email is read
    fetch(`/emails/${email_id}`, {
      method: 'PUT',
      body: JSON.stringify({
        read: true
      })
    })

    view_email(email_id);
  });
  return div
}

function display_mail(mailbox) {

  const email_views = document.querySelector('#emails-view');

  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      // Print emails
      // console.log(emails);

      if (emails.length > 0) {
        emails.forEach(email => {

          // console.log(email);
          const id = email.id;
          const sender = email.sender;
          const recipients = email.recipients;
          const subject = email.subject;
          const timestamp = email.timestamp;
          const is_read = email.read;

          const email_div = document.createElement('div');
          email_div.className = "each-email rounded-pill"
          if (is_read) {
            email_div.classList.add("read");
          }
          // create archieve and unarchieve button
          const button = document.createElement('button');

          // create each element div
          const sender_div = create_display_div(id, `<strong>From:</strong> ${sender}`);
          const recipients_div = create_display_div(id, `<strong>To:</strong> ${recipients}`);
          const subject_div = create_display_div(id, `${subject}`);
          const timestamp_div = create_display_div(id, `${timestamp}`);

          if (mailbox === 'inbox') {
            button.className = "archive-button btn btn-sm";
            button.innerHTML = "archive";
            button.addEventListener('click', () => achieve_mail(id));
            email_div.append(sender_div, subject_div, timestamp_div, button);
          } else if (mailbox === 'sent') {
            email_div.append(recipients_div, subject_div, timestamp_div);
          } else if (mailbox === 'archive') {
            button.className = "unarchive-button btn btn-sm btn-secondary";
            button.innerHTML = "unarchive";
            button.addEventListener('click', () => unachieve_mail(id));
            email_div.append(sender_div, subject_div, timestamp_div, button);
          }

          email_views.append(email_div);

        });
      }
    });

}

function create_email_div(title, html_content) {
  const div = document.createElement('div');
  div.className = "inner-email";
  div.innerHTML = `<strong>${title}:</strong> ${html_content}`
  return div
}

function view_email(email_id) {

  fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(email => {

      // Print email
      // console.log(email);

      const sender = email.sender;
      const recipients = email.recipients;
      const subject = email.subject;
      const timestamp = email.timestamp;
      const body = email.body;

      const div = document.createElement('div');
      div.className = "email";
      const reply_button = document.createElement('button');
      reply_button.className = "btn btn-sm button"
      reply_button.innerHTML = "Reply"

      reply_button.addEventListener('click', () => reply_email(sender, subject, body, timestamp));

      const sender_div = create_email_div("From", sender);
      const recipients_div = create_email_div("To", recipients);
      const subject_div = create_email_div("Subject", subject);
      const body_div = create_email_div("Body", body);
      const timestamp_div = create_email_div("Timestamp", timestamp);

      div.append(sender_div, recipients_div, subject_div, body_div, timestamp_div, reply_button);
      // clear prior inner HTML first
      document.querySelector("#email-view").innerHTML = "";
      document.querySelector("#email-view").append(div);
    });
}

function achieve_mail(email_id) {
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: true
    })
  })
    .then(() => load_mailbox('inbox'))

}

function unachieve_mail(email_id) {
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: false
    })
  })
    .then(() => load_mailbox('inbox'))
}

function reply_email(recipients, subject, body, timestamp) {

  compose_email()

  // Pre fill composition fields
  document.querySelector('#compose-recipients').value = recipients;

  // check is subject start with Re:
  if (subject.trim().slice(0, 3) == "Re:") {
    document.querySelector('#compose-subject').value = `${subject}`;
  } else {
    document.querySelector('#compose-subject').value = `Re: ${subject}`;
  }

  document.querySelector('#compose-body').value = `On ${timestamp} ${recipients} wrote: ${body}`;

}