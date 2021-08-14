document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  
  // By default, load the inbox
  load_mailbox('inbox');


});

function compose_email(email) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#single-email-view').style.display = 'none';
  //alert(receipients)
  // Clear out composition fields
  if(email === undefined){
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  }
  else{
    document.querySelector('#compose-recipients').value = email.sender;
    var check_subj = email.subject.search("Re: ");
    if (check_subj === 0){ // There is a 'Re: ' in the subject line
      document.querySelector('#compose-subject').value = email.subject;
    }
    else if(check_subj === -1){ //There is no 'Re: ' at the start of the subject line
      document.querySelector('#compose-subject').value = 'Re: '+email.subject;
    }
    
    
    document.querySelector('#compose-body').value = '\n\n\n\nOn ' + email.timestamp+ ', ' + email.sender + ' wrote: \n' + email.body;
  }
  

  //Code when email is sent
  document.querySelector('form').onsubmit = () => {
    //alert("Entering onsubmit")
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: document.querySelector('#compose-recipients').value,
          subject: document.querySelector('#compose-subject').value,
          body: document.querySelector('#compose-body').value,
          archived: false,
          read: false
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        var toast_msg = document.createElement('div');
        toast_msg.setAttribute('class','toast');
        toast_msg.setAttribute('role','alert');
        toast_msg.setAttribute('aria-live','assertive');
        toast_msg.setAttribute('aria-atomic','true');
        toast_msg.innerHTML = `<div class="toast-header">
                                  <img src="..." class="rounded me-2" alt="...">
                                  <strong class="me-auto">Mail Status</strong>
                                  <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
                              </div>
                              <div class="toast-body">
                                ${result.value}
                              </div>

                              `;
        var toast = new bootstrap.Toast(toast_msg);
        toast.show()    
        load_mailbox('inbox');
    });
    
  };
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch('/emails/'+mailbox)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);
      //console.log(emails[1].subject)
      // ... do something else with emails ...
      document.querySelector('#emails-view').innerHTML += `<div class="list-group">`;
      for (let i=0;i<emails.length;i++)
      {
        const element = document.createElement('a');
        if (emails[i].read === true){ //If an email is already read...
          element.setAttribute('class','list-group-item list-group-item-action list-group-item-dark');
        }
        else{ //If it is unread...
          element.setAttribute('class','list-group-item list-group-item-action');
        }
        
        element.innerHTML = `<div class="d-flex w-100 justify-content-between">
                                  <h5 class="mb-1">${emails[i].subject}</h5>
                                  <small class="text-muted">${emails[i].timestamp}</small>
                             </div>
                                  <p class="mb-1">${emails[i].sender}</p>
                                  <small class="text-muted">${emails[i].body.slice(0,100) + "...."}</small>`;
        element.addEventListener('click', () => load_email(emails[i].id,mailbox))
        document.querySelector('.list-group').appendChild(element);
        
        

      }
      
  });
  
}

function load_email(id,mailbox){

  // Show the mailbox and hide other views
  document.querySelector('#single-email-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';

  //Clear any pre-existing email content
  document.querySelector('#single-email-view').innerHTML = '';

  //Update Record from unread to read status
  fetch('/emails/'+id, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })

  //Get the JSON GET request
  fetch('/emails/'+id)
  .then(response => response.json())
  .then(email => {
      // Print emails
      console.log(email);
      var email_subject = document.createElement('h3');
      email_subject.innerHTML = email.subject;
      document.querySelector('#single-email-view').appendChild(email_subject);
      var email_sender = document.createElement('h5');
      email_sender.setAttribute('id','email-sender');
      email_sender.innerHTML = 'From: ' + email.sender;
      document.querySelector('#single-email-view').appendChild(email_sender);
      document.querySelector('#single-email-view').innerHTML += '<hr>';
      var email_body = document.createElement('p');
      email_body.setAttribute('class','lead text-break');
      email_body.innerHTML = email.body;
      document.querySelector('#single-email-view').appendChild(email_body);
      var reply_button = document.createElement('button');
      reply_button.innerHTML = 'Reply';
      reply_button.setAttribute('class','btn btn-primary');
      reply_button.setAttribute('role','button');
      reply_button.addEventListener('click' , () => compose_email(email));
      document.querySelector('#single-email-view').appendChild(reply_button);

      //Creating button for archiving and unarchiving email
      if(mailbox === 'inbox'){
        var archive_button = document.createElement('button');
        archive_button.setAttribute('class','btn btn-warning');
        archive_button.innerHTML = "Archive this email";
        archive_button.addEventListener('click', () => archive_email(email.id,mailbox));
        document.querySelector('#single-email-view').appendChild(archive_button);
      }
      else if(mailbox === 'archive'){
        var archive_button = document.createElement('button');
        archive_button.setAttribute('class','btn btn-light');
        archive_button.innerHTML = "Unarchive this email";
        archive_button.addEventListener('click', () => archive_email(email.id,mailbox));
        document.querySelector('#single-email-view').appendChild(archive_button);
      }
  });


}

function archive_email(id,mailbox)
{
  if(mailbox === 'inbox'){ //If in inbox mailbox, changed the archive status to true
    //Update Record
    fetch('/emails/'+id, {
      method: 'PUT',
      body: JSON.stringify({
          archived: true
      })
    })
  }
  else if(mailbox === 'archive'){//If in archive mailbox, changed the archive status to false
    //Update Record 
    fetch('/emails/'+id, {
    method: 'PUT',
      body: JSON.stringify({
          archived: false
      })
    })
  }

  var delayInMilliseconds = 500; //1 second

  setTimeout(function() {
    load_mailbox('inbox')
  }, delayInMilliseconds);
  
}