document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM fully loaded and parsed!");
    const leftArrow = document.querySelector('.left-arrow');
    const rightArrow = document.querySelector('.right-arrow');
    const slider = document.querySelector('.blog-slider');
    const slides = document.querySelectorAll('.blog-slide');
    let currentIndex = 0;
    const totalSlides = slides.length;

    console.log("Initializing blog slider functionality");
    console.log(`Total slides found: ${totalSlides}`);

    if (!leftArrow || !rightArrow || !slider) {
        console.error("Slider elements not found in the DOM!");
        return;
    }

    // Update the slider position
    function updateSliderPosition() {
        const offset = -(currentIndex * 33.33); // Adjust slider movement percentage as per layout
        slider.style.transform = `translateX(${offset}%)`;
        console.log(`Slider position updated to index: ${currentIndex}`);
    }

    // Handle left arrow click
    leftArrow.addEventListener('click', () => {
        console.log("Left arrow clicked");
        if (currentIndex > 0) {
            currentIndex--;
        } else {
            currentIndex = totalSlides - 1; // Loop to the last slide
        }
        updateSliderPosition();
    });

    // Handle right arrow click
    rightArrow.addEventListener('click', () => {
        console.log("Right arrow clicked");
        if (currentIndex < totalSlides - 1) {
            currentIndex++;
        } else {
            currentIndex = 0; // Loop to the first slide
        }
        updateSliderPosition();
    });
});