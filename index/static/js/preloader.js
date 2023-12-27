function hidePreloader() {
    const preloader = document.getElementById("preloader");
    preloader.style.opacity = "0";
    setTimeout(() => {
        document.body.style.overflow = "auto";
        preloader.style.display = "none";
    }, 800);
}

// function simulateLongLoad() {
//     setTimeout(function() {
//         hidePreloader();
//     }, 2000);
// }

window.addEventListener("load", hidePreloader);