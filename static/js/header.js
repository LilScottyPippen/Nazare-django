function setInitialHeaderColor() {
    const header = document.getElementById('header');
    if (window.scrollY > 200) {
        header.classList.add('header-transition');
        header.style.backgroundColor = '#24486C';
    } else {
        header.style.backgroundColor = 'transparent';
    }
}

function handleScroll() {
    const header = document.getElementById('header');
    if (window.scrollY > 200) {
        header.classList.add('header-transition');
        header.style.backgroundColor = '#24486C';
    } else {
        header.style.backgroundColor = 'transparent';
    }
}

window.addEventListener('load', setInitialHeaderColor);
window.addEventListener('scroll', handleScroll);

/*======== SHOW MENU ========*/
const navMenu = document.getElementById('menu-mobile'),
    navToggle = document.getElementById('nav-toggle'),
    navClose = document.getElementById('nav-close');

/*======== MENU SHOW ========*/
if (navToggle) {
    navToggle.addEventListener('click', () => {
        navMenu.classList.add('show-menu');
    });
}

/*======== MENU HIDDEN ========*/
if (navClose) {
    navClose.addEventListener('click', () => {
        navMenu.classList.remove('show-menu');
    });
}