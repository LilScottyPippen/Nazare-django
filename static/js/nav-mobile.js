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

const itemContainers = document.querySelectorAll('.nav-mobile-item-container');
let openedDropdown = null;

itemContainers.forEach(itemContainer => {
    const dropdownLinks = itemContainer.querySelector('.nav-mobile-dropdown-links');
    itemContainer.addEventListener('click', () => {
        if (openedDropdown && openedDropdown !== dropdownLinks) {
            openedDropdown.style.maxHeight = null;
            openedDropdown.style.transition = null;
        }

        if (dropdownLinks.style.maxHeight) {
            dropdownLinks.style.maxHeight = null;
            dropdownLinks.style.transition = null;
            openedDropdown = null;
        } else {
            dropdownLinks.style.maxHeight = '2000px';
            dropdownLinks.style.transition = 'max-height 0.4s ease-in';
            openedDropdown = dropdownLinks;
        }
    });
});
