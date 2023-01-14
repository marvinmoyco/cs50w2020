document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#all_post').addEventListener('click', () => load_newsfeed());
    //document.querySelector('#form_submit').addEventListener('click', () => new_post());
    // By default, load the newsfeed
    load_newsfeed();
  
  
  });

function load_newsfeed(){
      
    

    fetch('/news_feed')
    .then(response => response.json())
    .then(posts => {
        console.log("hELLLLO");
        //Creating the listgroup
        const div_listgroup = document.createElement('div');
        div_listgroup.setAttribute('class','list-group');

        //Put the listgroup element to the div in the html file
        document.querySelector('#all_post').appendChild(div_listgroup);

        console.log(posts);

        if(Object.keys(posts).length == 0)
        {
            var post = document.createElement('li');
            post.innerHTML = "No posts in the wall yet.";
            div_listgroup.appendChild(post);
        }
        else{
            for (i=0;i<posts.length;i++){
                //Create a list item
                var post = document.createElement('li');
                post.setAttribute('class','list-group-item');
                post.innerHTML = `<div class="d-flex w-100 justify-content-between">
                                      <h5 class="mb-1">${posts[i].user}</h5>
                                      <small class="text-muted">${posts[i].date_posted}</small>
                                 </div>
                                 <span class="badge bg-primary rounded-pill">${posts[i].likes}</span>
                                      <small class="text-muted">${posts[i].content }</small>`;
                //Append the list item to the list group
                div_listgroup.appendChild(post);
            }
        }
        


    });
    /*document.querySelector('#new_post_form').onsubmit = () => {
        fetch('/news_feed',{
            method: 'POST',
            body: JSON.stringify({
                post_content: document.querySelector('#post_body').value,
            })
        })
        .then(response => response.json())
        .then(result => {
            alert("Post successfully posted in newsfeed.");
            load_newsfeed();

        });


    };*/

}
  
/*

function new_post(){

    document.querySelector('#new_post_form').onsubmit = () => {
        fetch('/news_feed',{
            method: 'POST',
            body: JSON.stringify({
                post_content: document.querySelector('#post_body').value,
            })
        })
        .then(response => response.json())
        .then(result => {
            alert("Post successfully posted in newsfeed.");
            load_newsfeed();

        });


    };


}*/