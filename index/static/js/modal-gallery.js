var slideIndex = 0;
var caption;

function openModal(backgroundImage) {
    document.body.style.overflow = "hidden";
    var modal = document.getElementById("myModal");
    var modalImg = document.getElementById("modalImg");
    caption = document.getElementsByClassName("modal-caption")[0]; // Change to getElementsByClassName
    modal.style.display = "flex";

    var imageUrl = backgroundImage.slice(5, -2);
    modalImg.src = imageUrl;

    slideIndex = findIndex(imageUrl);
    updateCaption();
}

function updateCaption() {
    var images = document.querySelectorAll('.grid-gallery-image');

    if (images.length > 0) {
        var currentImage = images[slideIndex];
        var imageCaption = currentImage.getAttribute("data-caption");

        if (imageCaption) {
            caption.innerHTML = imageCaption;
        } else {
            var parentElementFallback = currentImage.closest('.grid-gallery-item');
            if (parentElementFallback) {
                var imageCaptionFallback = parentElementFallback.getAttribute("data-caption");
                caption.innerHTML = imageCaptionFallback;
            }
        }
    } else {
        var parentElementFallback = document.querySelector('.grid-gallery-image[style*="' + modalImg.src + '"]').closest('.grid-gallery-item');
        if (parentElementFallback) {
            var imageCaptionFallback = parentElementFallback.getAttribute("data-caption");
            caption.innerHTML = imageCaptionFallback;
        }
    }
}



function closeModal() {
    document.body.style.overflow = "auto";
    var modal = document.getElementById("myModal");
    modal.style.display = "none";
}

function plusSlides(n) {
    slideIndex += n;
    showImage(slideIndex);
}

function showImage(n) {
    var modalImg = document.getElementById("modalImg");
    var images = document.querySelectorAll('.grid-gallery-image');
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
    var images = document.querySelectorAll('.grid-gallery-image');
    for (var i = 0; i < images.length; i++) {
        if (images[i].style.backgroundImage.slice(5, -2) === imgSrc) {
            return i;
        }
    }
    return 0;
}

document.addEventListener('keydown', function (event) {
    var modal = document.getElementById("myModal");
    if (modal.style.display === "flex") {
        keyboardControl(event);
    }
});

function keyboardControl(event) {
    if (event.key === "Escape") {
        closeModal();
    } else if (event.key === "ArrowLeft") {
        plusSlides(-1);
    } else if (event.key === "ArrowRight") {
        plusSlides(1);
    }
}
