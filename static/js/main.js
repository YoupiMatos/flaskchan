const post_images = document.getElementsByClassName('post_images');

// Merci Jean!
for (var i = 0; i < post_images.length; i++){
    post_images[i].addEventListener('click', function(event){
        if (event.target.classList.contains('minimized')){
            event.target.classList.remove('minimized');
            event.target.classList.add('maximized');
        } else{
            event.target.classList.remove('maximized');
            event.target.classList.add('minimized');
        }
        
    });
}