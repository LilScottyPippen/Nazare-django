function checkCaptcha(value, captcha){
    try {
        return value.length > 0 && captcha.getAttribute('data-sitekey').length > 0
    } catch{
        return false
    }
}

function resetALlCaptcha(){
    const recaptchaBlocks = document.querySelectorAll('.g-recaptcha').length
    for (let i = 0; i < recaptchaBlocks; i++)
        grecaptcha.reset(i)
}