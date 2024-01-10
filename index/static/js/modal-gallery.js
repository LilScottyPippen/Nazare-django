let slideIndex = 0;

function openModal(backgroundImage) {
    document.body.style.overflow = "hidden";
    let modal = document.getElementById("myModal");
    let modalImg = document.getElementById("modalImg");
    modal.style.display = "flex";
    
    let imageUrl = backgroundImage.slice(5, -2);
    modalImg.src = imageUrl;
    
    slideIndex = findIndex(imageUrl);
}

function closeModal() {
    document.body.style.overflow = "auto";
    let modal = document.getElementById("myModal");
    modal.style.display = "none";
}

function plusSlides(n) {
    slideIndex += n;
    showImage(slideIndex);
}

function showImage(n) {
    let modalImg = document.getElementById("modalImg");
    let images = document.querySelectorAll('.grid-gallery-image');
    if (n >= images.length) {
        slideIndex = 0;
    }
    if (n < 0) {
        slideIndex = images.length - 1;
    }
    modalImg.src = images[slideIndex].style.backgroundImage.slice(5, -2);
}

function findIndex(imgSrc) {
    let images = document.querySelectorAll('.grid-galery-image');
    for (let i = 0; i < images.length; i++) {
        if (images[i].style.backgroundImage.slice(5, -2) === imgSrc) {
            return i;
        }
    }
    return 0;
}

document.addEventListener('keydown', function (event) {
let modal = document.getElementById("myModal");
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