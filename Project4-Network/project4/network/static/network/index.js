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
        //const div_listgroup = document.createElement('div');
        //div_listgroup.setAttribute('class','list-group');
        
        //Put the listgroup element to the div in the html file
        //document.querySelector('#all_post').appendChild(div_listgroup);

        console.log(posts);

        if(Object.keys(posts).length == 0)
        {
            var post = document.createElement('h4');
            post.innerHTML = "No posts in the wall yet.";
            document.querySelector('#all_post').appendChild(post);
        }
        else{
            for (i=0;i<posts.length;i++){

                //create a row
                const row = document.createElement('div');
                row.setAttribute('class','row');
                //Create left column
                const left_col = document.createElement('div');
                left_col.setAttribute('class','col-3');
                row.appendChild(left_col);

                //Create center column with padding at the bottom (pb-3)
                var center_col = document.createElement('div');
                center_col.setAttribute('class','col-6 pb-3');

                //Create a list item
                var post = document.createElement('div');
                post.setAttribute('class','card');
                post.innerHTML = `
                                    <div class="card-body">
                                    <h5><a href="network/${posts[i].user}">@${posts[i].user}</a></h5>
                                        <p class="card-text">${posts[i].content}</p>
                                        <a href="#" class="badge">Like this post</a>
                                    </div>
                                    <div class="card-footer text-muted">
                                        <span class="text-right"> Post created: ${posts[i].date_posted}</span>
                                        <span class="text-right"> Last updated: ${posts[i].date_edited}</span>
                                        <span>Likes: ${posts[i].likes}</span>
                                        
                                    </div>`;
                center_col.appendChild(post);
                row.appendChild(center_col);

                //Create right column
                const right_col = document.createElement('div');
                right_col.setAttribute('class','col-3');
                row.appendChild(right_col);
                document.querySelector('#all_post').appendChild(row);
              

                

            }
        }
        
        
       
        

    });


    document.querySelector('#form_submit').addEventListener('click', () =>{
        const emptyPostAlert = document.getElementById('liveToast');
        var isContentEmpty = document.getElementById('post_body');
        if (isContentEmpty.value.trim() === '') {
            const toast = new bootstrap.Toast(emptyPostAlert)
            toast.show()
        }
    });
    



}
  
