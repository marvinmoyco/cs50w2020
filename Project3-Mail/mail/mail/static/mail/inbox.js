document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  //Code when email is sent
  document.querySelector('form').onsubmit = () => {
    alert("Entering onsubmit")
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: document.querySelector('#compose-recipients').value,
          subject: document.querySelector('#compose-subject').value,
          body: document.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
        alert(result)
    });
    
  };
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch('/emails/'+mailbox)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);
      console.log(emails[0].subject)
      // ... do something else with emails ...
      document.querySelector('#emails-view').innerHTML += `<div class="list-group">`;
      for (let i=0;i<emails.length;i++)
      {
        document.querySelector('#emails-view').innerHTML += `<a href="#" class="list-group-item list-group-item-action">
                                                                <div class="d-flex w-100 justify-content-between">
                                                                  <h5 class="mb-1">${emails[i].subject}</h5>
                                                                  <small class="text-muted">${emails[i].timestamp}</small>
                                                                </div>
                                                                <p class="mb-1">${emails[i].recipients}</p>
                                                                <small class="text-muted">${emails[i].body}</small>
                                                              </a>
                                                                `;
        
        
        
        
        //document.querySelector('#emails-view').innerHTML += `<div class="d-flex w-100 justify-content-between">`;
        //document.querySelector('#emails-view').innerHTML += `<h5 class="mb-1">${emails[i].subject}</h5>`;
        //document.querySelector('#emails-view').innerHTML += `<small class="text-muted">${emails[i].timestamp}</small>`;
        //document.querySelector('#emails-view').innerHTML += `</div>`;
        //document.querySelector('#emails-view').innerHTML += `<p class="mb-1">${emails[i].recipients}</p>`;
        //document.querySelector('#emails-view').innerHTML += `<small class="text-muted">${emails[i].body}</small>`;
        //document.querySelector('#emails-view').innerHTML += `</a>`;
      }
      //document.querySelector('#emails-view').innerHTML += `</div">`;
  });


}