const navMobile = document.getElementById('nav-mobile'),
      navToggle = document.getElementById('nav-toggle');

navToggle.addEventListener('click', () => {
    const isOpen = navToggle.classList.contains('open'),
          icon = document.querySelector('#nav-toggle i');

    if (isOpen) {
        document.body.style.overflow = "hidden";
        navMobile.classList.add('show-menu');
        if (icon) {
            icon.classList.remove('fa-bars');
            icon.classList.add('fa-xmark');
        }
    } else {
        document.body.style.overflow = "auto";
        navMobile.classList.remove('show-menu');
        if (icon) {
            icon.classList.remove('fa-xmark');
            icon.classList.add('fa-bars');
        }
    }
    navToggle.classList.toggle('open');
});
