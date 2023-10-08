document.addEventListener('DOMContentLoaded', function() {
    let modalWindows;

    function openModalWindows(modalId) {
        modalWindows = document.getElementById(modalId);
        modalWindows.style.display = 'flex';
        document.body.style.overflow = 'hidden';

        modalWindows.addEventListener('wheel', function(event) {
            event.preventDefault();
        });

        modalWindows.addEventListener('keydown', function(event) {
            if (event.target.tagName.toLowerCase() !== 'input') {
                event.preventDefault();
            }
        });
    }

    try {
        let modalBtnCallback = document.querySelectorAll('#modal_btn_callback');
        let modalBtnViber = document.querySelectorAll('#modal_btn_viber');

        modalBtnCallback.forEach(function(element) {
            element.addEventListener('click', function() {
                openModalWindows('modal_windows_callback');
            });
        });

        modalBtnViber.forEach(function(element) {
            element.addEventListener('click', function() {
                openModalWindows('modal_windows_viber');
            });
        });
    } catch (error) {}

    let modalBtnClose = document.querySelectorAll('#close_modal');

    modalBtnClose.forEach(function(element) {
        element.addEventListener('click', function() {
            if (modalWindows) {
                modalWindows.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        });
    });
});
