let modals = {
    viberModal: null,
    callbackModal: null,
    emailModal: null,
    subscribeModal: null,
}

let navMobileSection

document.addEventListener('DOMContentLoaded', function () {
    modals.viberModal = document.getElementById('viberModal')
    modals.callbackModal = document.getElementById('callbackModal')
    modals.emailModal = document.getElementById('emailModal')
    modals.subscribeModal = document.getElementById('subscribeModal')

    navMobileSection = document.getElementById('nav-mobile')
})

function openModal(modal){
    modal.style.display = 'flex'
    document.body.style.overflow = "hidden"
}

function closeModal(object){
    document.getElementById(object).style.display = 'none'
    const isOpenSection = navMobileSection.classList.contains('show-menu')
    if (isOpenSection === false){
        document.body.style.overflow = "auto"
    }
}

function openViberModal(){
    openModal(modals.viberModal)
}

function openCallbackModal(){
    openModal(modals.callbackModal)
}

function openEmailModal(){
    openModal(modals.emailModal)
}

function openSubscribeModal(){
    resetAllCaptcha()
    openModal(modals.subscribeModal)
}