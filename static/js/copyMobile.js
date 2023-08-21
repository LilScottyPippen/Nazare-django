function isMobileDevice() {
    return (typeof window.orientation !== "undefined") || (navigator.userAgent.indexOf('IEMobile') !== -1);
}

function showNotification(status, text) {
    new Notify({
        status: status,
        text: text,
        effect: 'fade',
        speed: 300,
        customClass: null,
        customIcon: null,
        showIcon: true,
        showCloseButton: true,
        autoclose: true,
        autotimeout: 3000,
        gap: 20,
        distance: 20,
        type: 1,
        position: 'right bottom'
    });
}

const contactLinks = document.querySelectorAll('#contactLink');

function copyMobile(event) {
    if (isMobileDevice()) {
        window.open('tel:+375291699106', '_blank');
    } else {
        const phoneNumber = '+375291699106';
        const tempInput = document.createElement('input');
        tempInput.value = phoneNumber;
        document.body.appendChild(tempInput);
        tempInput.select();
        document.execCommand('copy');
        document.body.removeChild(tempInput);

        showNotification('success', 'Номер телефона скопирован');
    }
    event.preventDefault();
}

contactLinks.forEach(link => {
    link.addEventListener('click', copyMobile);
});

try{
    document.getElementById('contactLinkDev').addEventListener('click', copyMobile);
} catch (error) {}