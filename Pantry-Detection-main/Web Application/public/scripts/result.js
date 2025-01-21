function cycleImages() {
    const carouselContainer = document.getElementById('carousel-container');
    const carouselItems = carouselContainer.querySelectorAll('.carousel-item');
    let currentIndex = 0;

    setInterval(() => {
        // Hide the current image
        carouselItems[currentIndex].style.display = 'none';
        // Move to the next image
        currentIndex = (currentIndex + 1) % carouselItems.length;
        // Display the next image
        carouselItems[currentIndex].style.display = 'block';
    }, 500); // Change this value to adjust the interval between image changes (in milliseconds)
}

// Call the function to start the image carousel
cycleImages();

function getRand(array) {
    const index = Math.floor(Math.random() * array.length);
    return array[index];
  }
  
  const phrases = ["May the odds forever be in your flavor!", "Scanning for lifeforms...Er, food", "Pantry investigation in progress, please stand by.", "That's a nice pantry you've got there.", "Your recipes are on the way!", "Rummaging through your foods...", "Fear not, your next meal adventure awaits!", "Lettuce romaine calm while we search for ingredients!"];
  
  const phrase = getRand(phrases);
  document.getElementById("loading-text").textContent = phrase;


  function cycleLoadingText() {
    setInterval(() => {
      const phrase = getRand(phrases);
      document.getElementById("loading-text").textContent = phrase;
    }, 7000); //Interval of phrase changes
  }
  
  cycleLoadingText();