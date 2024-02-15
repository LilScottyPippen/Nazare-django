let viberModal, callbackModal;

document.addEventListener('DOMContentLoaded', function () {
    viberModal = document.getElementById('viberModal');
    callbackModal = document.getElementById('callbackModal');
});

function openViberModal(){
    viberModal.style.display = 'flex';
    document.body.style.overflow = "hidden";
}

function openCallbackModal(){
    callbackModal.style.display = 'flex';
    document.body.style.overflow = "hidden";
}

function closeModal(object){
    document.getElementById(object).style.display = 'none';
    document.body.style.overflow = "auto";
}