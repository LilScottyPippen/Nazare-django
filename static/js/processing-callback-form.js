let captchaCallbackInput, captchaCallbackResponse

function handleCallbackCaptcha(response){
    captchaCallbackResponse = response
}

function is_valid_phone(phone) {
    const belarus_pattern = /^(?:\+375|375)\d{9}$/
    const russia_pattern = /^(?:\+7|7)\d{10}$/

    return belarus_pattern.test(phone) || russia_pattern.test(phone)
}

function handleCallback(csrf_token) {
    let hasError = false
    const form = document.getElementById('callbackForm')
    let client_name = document.getElementById('name').value
    let client_phone = document.getElementById('phone').value
    let client_data = {
        'client_data': {
            'name': client_name,
            'phone': client_phone
        }
    }

    for (const key in client_data.client_data) {
        const input = document.querySelector(`#${key}`)
        const value = client_data.client_data[key]

        if (key === 'phone' && !is_valid_phone(value)) {
            hasError = true
            if (input) {
                input.style.borderColor = 'red'
            }
        } else if (!value) {
            hasError = true
            if (input) {
                input.style.borderColor = 'red'
            }
        } else {
            if (input) {
                input.style.borderColor = ''
            }
        }

        if(key === 'name' && value.length < 3){
            hasError = true
            if (input) {
                input.style.borderColor = 'red'
            }
        }
    }

    const privacy_policy_block = document.querySelector('.footer-form')
    const privacy_policy = document.getElementById('callback-privacy_policy')
    const is_checked = privacy_policy.checked

    if (is_checked === false) {
        privacy_policy_block.style.border = '2px solid red'
        hasError = true
    } else {
        privacy_policy_block.style.border = ''
    }

    captchaCallbackInput = document.getElementById('callback-recaptcha')

    if (checkCaptcha(captchaCallbackResponse, captchaCallbackInput)){
        captchaCallbackInput.style.border = 'none'
        client_data.client_data.captcha = captchaCallbackResponse
    }else{
        hasError = true
        captchaCallbackInput.style.border = '2px solid red'
        showNotification('error', ERROR_MESSAGES['invalid_captcha'])
    }

    if (!hasError) {
        client_data.client_data.is_privacy_policy = true
        $.ajax({
            type: "POST",
            url: "/api/callback/",
            data: JSON.stringify(client_data),
            contentType: "application/json",
            headers: {
                'X-CSRFToken': csrf_token
            },
            success: function (response) {
                form.reset()
                resetALlCaptcha()
                captchaCallbackResponse = ''
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