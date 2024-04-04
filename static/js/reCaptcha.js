function checkCaptcha(value, captcha){
    return value.length > 0 && captcha.getAttribute('data-sitekey').length > 0
}

function resetALlCaptcha(){
    const recaptchaBlocks = document.querySelectorAll('.g-recaptcha').length;
    console.log(recaptchaBlocks)
    for (let i = 0; i < recaptchaBlocks; i++)
        grecaptcha.reset(i);
}