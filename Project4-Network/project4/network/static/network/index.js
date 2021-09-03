document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#all_post').addEventListener('click', () => load_newsfeed());
    
    // By default, load the newsfeed
    load_newsfeed();
  
  
  });

function load_newsfeed(){
      
    

    fetch('network/news_feed')
    .then(response => response.json())
    .then(posts => {
        //Creating the listgroup
        const div_listgroup = document.createElement('div');
        div_listgroup.setAttribute('class','list-group');

        //Put the listgroup element to the div in the html file
        document.querySelector('#all_post').appendChild(div_listgroup);


        for (i=0;i<posts.length;i++){
            //Create a list item
            var list_item = document.createElement('li');
            
            //Append the list item to the list group

        }


    }
}
  