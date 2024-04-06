const slider = document.querySelector('.slider')
const prevBtn = document.querySelector('.prevBtn')
const nextBtn = document.querySelector('.nextBtn')
const cardWidth = document.querySelector('.review-width').offsetWidth + 20
const totalSlides = slider.children.length
let currentIndex = 0

prevBtn.addEventListener('click', () => {
    currentIndex = currentIndex > 0 ? currentIndex - 1 : totalSlides - 1
    updateSliderPosition()
})

nextBtn.addEventListener('click', () => {
    currentIndex = currentIndex < totalSlides - 1 ? currentIndex + 1 : 0
    updateSliderPosition()
})

function updateSliderPosition() {
    if (currentIndex === totalSlides) {
        currentIndex = 0
    } else if (currentIndex < 0) {
        currentIndex = totalSlides - 1
    }

    const newPosition = -currentIndex * cardWidth
    slider.style.transform = `translateX(${newPosition}px)`

    if (currentIndex === totalSlides) {
        setTimeout(() => {
        slider.style.transition = 'none'
        currentIndex = 0
        slider.style.transform = `translateX(0px)`
        setTimeout(() => {
            slider.style.transition = 'transform 0.3s ease-in-out'
        })
        }, 200)
    }
}