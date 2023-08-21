document.addEventListener('DOMContentLoaded', function() {
    const viberQrCode = document.getElementById('viberQrCode');

    function openViberQrCode() {
        viberQrCode.style.display = 'flex';
        document.body.style.overflow = 'hidden';

        viberQrCode.addEventListener('wheel', function(event) {
            event.preventDefault();
        });

        viberQrCode.addEventListener('keydown', function(event) {
            if (event.target.tagName.toLowerCase() !== 'input') {
                event.preventDefault();
            }
        });
    }

    const viberIconButtons = document.querySelectorAll('.fab.fa-viber');

    viberIconButtons.forEach(function(button) {
        button.parentElement.addEventListener('click', openViberQrCode);
    });

    document.getElementById('closeQrCode').addEventListener('click', function() {
        viberQrCode.style.display = 'none';
        document.body.style.overflow = 'auto';
    });
});
