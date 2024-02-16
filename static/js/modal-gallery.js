let slideIndex = 0;
let caption;

function openModal(backgroundImage) {
    document.body.style.overflow = "hidden";

    const modal = document.getElementById("galleryModal");
    const modalImg = document.getElementById("modalImg");

    caption = document.getElementsByClassName("modal-caption")[0];
    modal.style.display = "flex";

    const imageUrl = backgroundImage.slice(5, -2);
    modalImg.src = imageUrl;

    slideIndex = findIndex(imageUrl);
    updateCaption();
}

function updateCaption() {
    const images = document.querySelectorAll('.grid-gallery-image');

    if (images.length > 0) {
        const currentImage = images[slideIndex];
        const imageCaption = currentImage.getAttribute("data-caption");

        if (imageCaption) {
            caption.innerText = imageCaption;
        } else {
            const parentElementFallback = currentImage.closest('.grid-gallery-item');
            if (parentElementFallback) {
                const imageCaptionFallback = parentElementFallback.getAttribute("data-caption");
                caption.innerText = imageCaptionFallback;
            }
        }
    } else {
        const parentElementFallback = document.querySelector('.grid-gallery-image[style*="' + modalImg.src + '"]').closest('.grid-gallery-item');
        if (parentElementFallback) {
            const imageCaptionFallback = parentElementFallback.getAttribute("data-caption");
            caption.innerText = imageCaptionFallback;
        }
    }
}

function plusSlides(n) {
    slideIndex += n;
    showImage(slideIndex);
}

function showImage(n) {
    const modalImg = document.getElementById("modalImg");
    const images = document.querySelectorAll('.grid-gallery-image');
    if (n >= images.length) {
        slideIndex = 0;
    }
    if (n < 0) {
        slideIndex = images.length - 1;
    }
    modalImg.src = images[slideIndex].style.backgroundImage.slice(5, -2);

    updateCaption();
}

function findIndex(imgSrc) {
    const images = document.querySelectorAll('.grid-gallery-image');
    for (let i = 0; i < images.length; i++) {
        if (images[i].style.backgroundImage.slice(5, -2) === imgSrc) {
            return i;
        }
    }
    return 0;
}

document.addEventListener('keydown', function (event) {
    const modal = document.getElementById("galleryModal");
    if (modal.style.display === "flex") {
        if (event.key === "Escape") {
            closeModal();
        } else if (event.key === "ArrowLeft") {
            plusSlides(-1);
        } else if (event.key === "ArrowRight") {
            plusSlides(1);
        }
    }
});
