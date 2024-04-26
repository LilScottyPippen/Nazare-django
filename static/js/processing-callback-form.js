let captchaCallbackInput, captchaCallbackResponse

function handleCallbackCaptcha(response){
    captchaCallbackResponse = response
    getValidityCaptcha(CAPTCHA_SUBJECTS['callback_captcha'], response)
}

function is_valid_phone(phone) {
    return phoneRegex.test(phone)
}

function handleCallback(csrf_token) {
    let hasError = false
    const form = document.getElementById('callbackForm')
    let client_name = document.getElementById('name').value
    let client_phone = document.getElementById('phone').value
    let client_data = {
        'client_data': {
            'name': client_name,
            'phone': client_phone,
        }
    }

    for (const key in client_data.client_data) {
        const input = document.querySelector(`#${key}`)
        const value = client_data.client_data[key]

        if (key === 'phone' && !is_valid_phone(value)) {
            hasError = true
            if (input) {
                input.style.borderColor = errorBorderColor
            }
        } else if (!value) {
            hasError = true
            if (input) {
                input.style.borderColor = errorBorderColor
            }
        } else {
            if (input) {
                input.style.borderColor = null
            }
        }

        if(key === 'name'){
            if(value.length < 3 || !stringRegex.test(value)){
                hasError = true
                if (input) {
                    input.style.borderColor = errorBorderColor
                }
            }else{
                input.style.borderColor = null
            }
        }
    }

    const privacy_policy_block = document.querySelector('.footer-form')
    const privacy_policy = document.getElementById('callback-privacy_policy')
    const is_checked = privacy_policy.checked

    if (is_checked === false) {
        privacy_policy_block.style.border = errorBorderStyle
        hasError = true
    } else {
        privacy_policy_block.style.border = null
    }

    captchaCallbackInput = document.getElementById('callback-recaptcha')

    if (checkCaptcha(captchaCallbackResponse, captchaCallbackInput)){
        captchaCallbackInput.style.border = null
    }else{
        hasError = true
        captchaCallbackInput.style.border = errorBorderStyle
        showNotification('error', ERROR_MESSAGES['invalid_captcha'])
    }

    if (!hasError) {
        client_data.client_data.is_privacy_policy = true
        $.ajax({
            type: "POST",
            url: "/api/callback",
            data: JSON.stringify(client_data),
            contentType: "application/json",
            headers: {
                'X-CSRFToken': csrf_token
            },
            success: function (response) {
                form.reset()
                resetAllCaptcha()
                captchaCallbackResponse = null
                document.getElementById('callback-privacy_policy').checked = false
                showNotification(response.status, response.message)
            },
            error: function (response) {
                showNotification(response.responseJSON.status, response.responseJSON.message)
            }
        })
    } else{
        showNotification('error', ERROR_MESSAGES['invalid_form'])
    }
}