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

    try {
        document.getElementById('viber-icon').addEventListener('click', openViberQrCode);
    } catch (error) {}

    document.getElementById('closeQrCode').addEventListener('click', function() {
        viberQrCode.style.display = 'none';
        document.body.style.overflow = 'auto';
    });
});