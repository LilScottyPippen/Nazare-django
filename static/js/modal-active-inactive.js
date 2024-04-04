let viberModal, callbackModal, emailModal, subscribeModal;
let navMobileSection
document.addEventListener('DOMContentLoaded', function () {
    viberModal = document.getElementById('viberModal');
    callbackModal = document.getElementById('callbackModal');
    emailModal = document.getElementById('emailModal');
    subscribeModal = document.getElementById('subscribeModal')

    navMobileSection = document.getElementById('nav-mobile');
});

function openViberModal(){
    viberModal.style.display = 'flex';
    document.body.style.overflow = "hidden";
}

function openCallbackModal(){
    callbackModal.style.display = 'flex';
    document.body.style.overflow = "hidden";
}

function openEmailModal(){
    emailModal.style.display = 'flex';
    document.body.style.overflow = "hidden"
}

function openSubscribeModal(){
    subscribeModal.style.display = 'flex'
    document.body.style.overflow = "hidden"
}

function closeModal(object){
    document.getElementById(object).style.display = 'none';
    const isOpenSection = navMobileSection.classList.contains('show-menu')
    if (isOpenSection === false){
        document.body.style.overflow = "auto";
    }
}