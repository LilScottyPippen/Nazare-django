let slideIndex = 0
let caption, modal, modalImg, images

document.addEventListener('DOMContentLoaded', function() {
    modal = document.getElementById("galleryModal")
    modalImg = document.getElementById("modalImg")
    caption = document.getElementsByClassName("modal-caption")[0]
    images = document.querySelectorAll('.grid-gallery-image')
})

function openImageModal(backgroundImage) {
    document.body.style.overflow = "hidden"
    modal.style.display = "flex"

    modalImg.src = backgroundImage
    slideIndex = findIndex(backgroundImage)

    updateCaption()
}

function updateCaption() {
    const currentImage = images[slideIndex]
    caption.innerText = currentImage.getAttribute("data-caption") || currentImage.closest('.grid-gallery-item').getAttribute("data-caption")
}

function showImage(n) {
    images = document.getElementsByClassName('grid-gallery-image')

    slideIndex += n

    if (slideIndex >= images.length) {
        slideIndex = 0
    }
    if (slideIndex < 0) {
        slideIndex = images.length - 1
    }

    modalImg.src = images[slideIndex].querySelector('img').src

    updateCaption()
}

function findIndex(imgSrc) {
    images = document.querySelectorAll('.grid-gallery-image')
    for (let i = 0; i < images.length; i++) {
        if (images[i].style.backgroundImage.slice(5, -2) === imgSrc) {
            return i
        }
    }
    return 0
}

document.addEventListener('keydown', function (event) {
    if (modal.style.display === "flex") {
        if (event.key === "Escape" || event.key === "Esc") {
            closeModal(modal.id)
        } else if (event.key === "ArrowLeft") {
            showImage(-1)
        } else if (event.key === "ArrowRight") {
            showImage(1)
        }
    }
})
