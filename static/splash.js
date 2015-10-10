$(document).ready(function(){
      // Index used to cycle through images (this controls the repetition)
      var index = 1;
      // Element names for images to manipulate
      var images = ["#london", "#newyork", "#paris", "#tokyo", "#venice"];
      var cities = ["london", "new+york", "paris", "tokyo", "venice"]
      // Repeats every sixty seconds to bring up a new image
      setInterval(function(){
            index = index % images.length
            $(images[index]).fadeIn(1750);
            if (index == 0) {
                  $(images[4]).fadeOut(1750);
            } else {
                  $(images[index - 1]).fadeOut(1750);
            }
            index += 1
      }, 6000);
});