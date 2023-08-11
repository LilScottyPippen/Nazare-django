function isMobileDevice() {
    return (typeof window.orientation !== "undefined") || (navigator.userAgent.indexOf('IEMobile') !== -1);
}

function copyMobile(){
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

        const Toast = Swal.mixin({
            toast: true,
            position: 'bottom-end',
            showConfirmButton: false,
            timer: 3000,
            timerProgressBar: true,
            didOpen: (toast) => {
            toast.addEventListener('mouseenter', Swal.stopTimer)
            toast.addEventListener('mouseleave', Swal.resumeTimer)
            }
        })
        
        Toast.fire({
            icon: 'success',
            title: 'Номер телефона скопирован'
        })
    }
    event.preventDefault();
}

document.getElementById('contactLink').addEventListener('click', copyMobile);
try{
    document.getElementById('contactLinkDev').addEventListener('click', copyMobile);
} catch (error) {}