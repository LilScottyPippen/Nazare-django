let captchaBookingInput, captchaBookingResponse

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const dateRegex = /^\d{4}\-\d{1,2}\-\d{1,2}$/
const phoneRegex = /^(?:\+375|375)\d{9}$|^(?:\+7|7)\d{10}$/
const stringRegex = /^[\p{L}]+$/u

const errorBorderColor = 'red'
const errorBorderStyle = '2px solid ' + errorBorderColor

function getClientFormData(method){
    let hasError = false
    let apartment_id

    try {
        apartment_id = document.querySelector('.form-apartment-items .choose-input.active').getAttribute('data-id')
    } catch (error) {
        hasError = true
        const errorFields = document.querySelectorAll('.form-apartment-items .choose-input')
        errorFields.forEach((field) => {
            field.style.borderColor = errorBorderColor
        })
    }

    if (!hasError) {
        const activeFields = document.querySelectorAll('.form-apartment-items .choose-input')
        activeFields.forEach((field) => {
            field.style.borderColor = ''
        })
    }

    const formData = {
        apartment: apartment_id,
        check_in_date: document.getElementById('check_in_date').innerText,
        check_out_date: document.getElementById('check_out_date').innerText,
        guests_count: document.getElementById('guests_count').innerText,
        children_count: document.getElementById('children_count').innerText,
        client_surname: document.getElementById('client_surname').value,
        client_name: document.getElementById('client_name').value,
        client_phone: document.getElementById('client_phone').value,
        client_mail: document.getElementById('client_mail').value,
    }

    const nameFields = ['client_surname', 'client_name']

    for (const key in formData) {
        const input = document.getElementById(key)
        const parentElement = input.closest('.search-apartment-dropdown')

        if (nameFields.includes(key)) {
            const fullNamePart = formData[key]
            if (!fullNamePart.trim() || !stringRegex.test(fullNamePart) || fullNamePart.length < 3) {
                hasError = true
                if (input) {
                    input.style.borderColor = errorBorderColor
                    if (parentElement) {
                        parentElement.style.borderColor = errorBorderColor
                    }
                }
            } else {
                input.style.borderColor = ''
                if (parentElement) {
                    parentElement.style.borderColor = ''
                }
            }
        } else if (key === 'client_phone' && !phoneRegex.test(formData[key])) {
            hasError = true
            input.style.borderColor = errorBorderColor
            if (parentElement) {
                parentElement.style.borderColor = errorBorderColor
            }
        } else {
            if (!formData[key]) {
                hasError = true
                if (input) {
                    input.style.borderColor = errorBorderColor
                    if (parentElement) {
                        parentElement.style.borderColor = errorBorderColor
                    }
                }
            } else {
                input.style.borderColor = ''
                if (parentElement) {
                    parentElement.style.borderColor = ''
                }
            }

            if (key === 'check_in_date' || key === 'check_out_date') {
                if (!dateRegex.test(formData[key])) {
                    hasError = true
                    parentElement.style.borderColor = errorBorderColor
                } else {
                    parentElement.style.borderColor = ''
                }
            }

            if (key === 'client_mail' && !emailRegex.test(formData[key])) {
                hasError = true
                input.style.borderColor = errorBorderColor
                if (parentElement) {
                    parentElement.style.borderColor = errorBorderColor
                }
            }

            if (key === 'children_count') {
                if (parseInt(formData[key]) < 0) {
                    hasError = true
                    parentElement.style.borderColor = errorBorderColor
                } else {
                    parentElement.style.borderColor = ''
                }
            }

            if (key === 'guests_count'){
                if (parseInt(formData[key]) < 1) {
                    hasError = true
                    parentElement.style.borderColor = errorBorderColor
                } else {
                    parentElement.style.borderColor = ''
                }
            }
        }
    }

    const client_father_name_input = document.getElementById('client_father_name')

    if (!check_name(client_father_name_input.value)){
        client_father_name_input.style.border = errorBorderStyle
    }else{
        client_father_name_input.style.border = ''
    }

    const privacy_policy_block = document.querySelector('.form-privacy-policy')
    const privacy_policy = document.getElementById('privacy_policy')
    const is_checked = privacy_policy.checked

    if (is_checked === false) {
        privacy_policy_block.style.border = errorBorderStyle
    } else {
        privacy_policy_block.style.border = ''
    }

    captchaBookingInput = document.getElementById('booking-recaptcha')

    if (checkCaptcha(captchaBookingResponse, captchaBookingInput)){
        captchaBookingInput.style.border = 'none'
        formData.captcha = captchaBookingResponse
    }else{
        hasError = true
        captchaBookingInput.style.border = errorBorderStyle
        showNotification('error', ERROR_MESSAGES['invalid_captcha'])
    }

    if (hasError) {
        return false
    }
    formData.client_father_name = document.getElementById('client_father_name').value
    formData.payment_method = method
    formData.total_sum = document.getElementById('totalCost').innerText
    formData.is_privacy_policy = is_checked

    return formData
}

function getGuestFormData(guestForm) {
    let hasError = false

    let citizenship = guestForm.querySelectorAll('.form-guest-information-citizenship-items .choose-input')

    try {
        if(Array.from(citizenship).find(button => button.classList.contains('active')).value) {
            citizenship = guestForm.querySelector('.form-guest-information-citizenship-items .choose-input.active')
        }
    } catch (error) {
        hasError = true
        const errorFields = document.querySelectorAll('.form-guest-information-citizenship-items .choose-input')
        errorFields.forEach((field) => {
            field.style.borderColor = errorBorderColor
        })
    }

    if (!hasError) {
        const activeFields = document.querySelectorAll('.form-guest-information-citizenship-items .choose-input')
        activeFields.forEach((field) => {
            field.style.borderColor = ''
        })
    }

    const formData = {
        guest_surname: guestForm.querySelector('.text-input[id="guest_surname"]').value,
        guest_name: guestForm.querySelector('.text-input[id="guest_name"]').value,
        citizenship: citizenship.value,
    }

    for (const key in formData) {
        const input = guestForm.querySelector(`#${key}`)

        if (!formData[key]) {
            hasError = true
            if (input) {
                input.style.borderColor = errorBorderColor
            }
        } else {
            if (input) {
                input.style.borderColor = ''
            }
        }

        if(key === 'guest_name' || key === 'guest_surname'){
            if(formData[key].length < 3 || !stringRegex.test(formData[key])){
                hasError = true
                input.style.borderColor = errorBorderColor
            } else{
                input.style.borderColor = ''
            }
        }
    }

    const guest_father_name_input = guestForm.querySelector('.text-input[id="guest_father_name"]')

    if (!check_name(guest_father_name_input.value)){
        hasError = true
        guest_father_name_input.style.border = errorBorderStyle
    }else{
        guest_father_name_input.style.border = '';
    }

    if (hasError) {
        return false
    }

    formData.guest_father_name = guest_father_name_input.value
    return formData
}

function resendCode(){
    $.ajax({
        type: "GET",
        url: `/api/send_confirmation_code/${document.getElementById('client_mail').value}`,
        contentType: "application/json",
        success: function(response) {
            openEmailModal()
            startResendTimer(31, 'resendBtn')
            showNotification(response.status, response.message)
        },
        error: function(response) {
            showNotification(response.responseJSON.status, response.responseJSON.message)
        }
    })
}

const formData = (method) => {
    const clientData = getClientFormData(method)
    const guestData = []

    const guestForms = document.querySelectorAll('.form-guest-information-item')

    guestForms.forEach((form) => {
        const formData = getGuestFormData(form)
        if (formData !== null) {
            guestData.push(formData)
        }
    })

    return {
        clientData: clientData,
        guestData: guestData
    }
}

function handleBookingForm(method) {
    startResendTimer(31, 'resendBtn')
    const data = formData(method)
    if (data.clientData === false || data.guestData[0] === false || data.clientData.is_privacy_policy === false){
        showNotification("error", ERROR_MESSAGES['invalid_form'])
    }else{
        openEmailModal()
        $.ajax({
            type: "GET",
            url: `/api/send_confirmation_code/${data.clientData.client_mail}`,
            contentType: "application/json",
            success: function(response) {
                showNotification(response.status, response.message)
            },
            error: function(response) {
                showNotification(response.responseJSON.status, response.responseJSON.message)
            }
        })
    }
}

let resendTimer

function startResendTimer(interval, text_id) {
    let duration = interval
    let display = document.getElementById(text_id);

    if (resendTimer) {
        return;
    }

    updateDisplay();

    resendTimer = setInterval(function() {
        if (duration > 0) {
            display.textContent = "Отправить код повторно через: " + duration + " секунд";
            duration--;
        } else {
            clearInterval(resendTimer);
            resendTimer = null;
            display.textContent = "Запросить повторный код подтверждения";
            display.style.textDecoration = "underline";
            display.style.cursor = "pointer";
            display.setAttribute("onclick", "resendCode()");
        }
    }, 1000);

    function updateDisplay() {
        display.textContent = "Отправить код повторно через: " + duration + " секунд";
        display.style.textDecoration = "none"
        display.removeAttribute("onclick")
        display.style.cursor = "default"
    }
}

function handleBookingConfirmForm(method, csrf_token){
    const data = formData(method)

    if (data.clientData === false || data.guestData[0] === false || data.clientData.is_privacy_policy === false){
        showNotification("error", ERROR_MESSAGES['invalid_form'])
    }else{
        const code_input = document.getElementById('email-code')
        const code = code_input.value

        if (code.length === 0){
            code_input.style.borderColor = errorBorderColor
            showNotification("error", ERROR_MESSAGES['incorrect_code'])
        }else{
            $.ajax({
                type: "GET",
                url: `/api/confirm_email/${code}`,
                contentType: "application/json",

                success: function() {
                    $.ajax({
                        type: "POST",
                        url: "/booking",
                        data: JSON.stringify(data),
                        contentType: "application/json",
                        headers: {
                            'X-CSRFToken': csrf_token
                        },
                        success: function(response) {
                            clearForm()
                            resetALlCaptcha()
                            captchaBookingResponse = ''
                            code_input.style.borderColor = ''
                            showNotification(response.status, response.message)
                        },
                        error: function(response) {
                            code_input.style.borderColor = errorBorderColor
                            showNotification(response.responseJSON.status, response.responseJSON.message)
                        }
                    })
                },
                error: function(response) {
                    code_input.style.borderColor = errorBorderColor
                    showNotification(response.responseJSON.status, response.responseJSON.message)
                }
            })
        }
    }
}

function clearForm() {
    const formInputs = document.querySelectorAll('.booking-form input[type="input"]')
    const formCheckboxes = document.querySelectorAll('.booking-form input[type="checkbox"]')
    const modalNumbers = document.querySelectorAll('.modal-form input[type="number"]')

    document.getElementById('children_count').innerText = 0
    document.getElementById('guests_count').innerText = 1

    formInputs.forEach(function(input) {
        input.value = ''
    })

    formCheckboxes.forEach(function(checkbox) {
        checkbox.checked = false
    })

    modalNumbers.forEach(function (input){
        input.value = ''
    })

    resetDates(moment().toDate())

    generateGuestInformationBlocks()

    closeModal(modals.emailModal.id)
}

function handleBookingCaptcha(response){
    captchaBookingResponse = response
}

function check_name(name){
    const name_length = name.length
    return (name_length === 0 || (name_length > 0 && name_length > 2 && stringRegex.test(name)));
}