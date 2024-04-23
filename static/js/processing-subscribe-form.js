function handleSubscriber(response) {
    getValidityCaptcha(CAPTCHA_SUBJECTS['subscribe_captcha'], response)

    let hasError = false
    const form = document.getElementById('mailingForm')
    const mail = document.getElementById('input-mail').value
    const captcha = document.getElementById('subscribe-recaptcha')
    const csrf_token = captcha.getAttribute('data-csrf')

    if (!emailRegex.test(mail)){
        hasError = true
        const errorField = document.getElementById('input-mail')
        errorField.style.border = errorBorderStyle
    }

    if (!hasError) {
        const activeFields = document.getElementById('input-mail')
        activeFields.style.border = null
    }

    $.ajax({
        type: "POST",
        url: "/api/subscribe",
        data: {
            'mail': mail,
        },
        contentType: "application/x-www-form-urlencoded",
        headers: {
            'X-CSRFToken': csrf_token
        },
        success: function (response) {
            form.reset()
            showNotification(response.status, response.message)
        },
        error: function (response) {
            showNotification(response.responseJSON.status, response.responseJSON.message)
        }
    })

    closeModal(modals.subscribeModal.id)
    resetALlCaptcha()
}