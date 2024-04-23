let captchaBookingInput, captchaBookingResponse

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
            field.style.borderColor = null
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
                input.style.borderColor = null
                if (parentElement) {
                    parentElement.style.borderColor = null
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
                input.style.borderColor = null
                if (parentElement) {
                    parentElement.style.borderColor = null
                }
            }

            if (key === 'check_in_date' || key === 'check_out_date') {
                if (!dateRegex.test(formData[key])) {
                    hasError = true
                    parentElement.style.borderColor = errorBorderColor
                } else {
                    parentElement.style.borderColor = null
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
                    parentElement.style.borderColor = null
                }
            }

            if (key === 'guests_count'){
                if (parseInt(formData[key]) < 1) {
                    hasError = true
                    parentElement.style.borderColor = errorBorderColor
                } else {
                    parentElement.style.borderColor = null
                }
            }
        }
    }

    const client_father_name_input = document.getElementById('client_father_name')

    if (!check_name(client_father_name_input.value)){
        client_father_name_input.style.border = errorBorderStyle
    }else{
        client_father_name_input.style.border = null
    }

    const privacy_policy_block = document.querySelector('.form-privacy-policy')
    const privacy_policy = document.getElementById('privacy_policy')
    const is_checked = privacy_policy.checked

    if (is_checked === false) {
        privacy_policy_block.style.border = errorBorderStyle
    } else {
        privacy_policy_block.style.border = null
    }

    captchaBookingInput = document.getElementById('booking-recaptcha')

    if (checkCaptcha(captchaBookingResponse, captchaBookingInput)){
        captchaBookingInput.style.border = null
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
            field.style.borderColor = null
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
                input.style.borderColor = null
            }
        }

        if(key === 'guest_name' || key === 'guest_surname'){
            if(formData[key].length < 3 || !stringRegex.test(formData[key])){
                hasError = true
                input.style.borderColor = errorBorderColor
            } else{
                input.style.borderColor = null
            }
        }
    }

    const guest_father_name_input = guestForm.querySelector('.text-input[id="guest_father_name"]')

    if (!check_name(guest_father_name_input.value)){
        hasError = true
        guest_father_name_input.style.border = errorBorderStyle
    }else{
        guest_father_name_input.style.border = null
    }

    if (hasError) {
        return false
    }

    formData.guest_father_name = guest_father_name_input.value
    return formData
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
    const data = formData(method)
    if (data.clientData === false || data.guestData[0] === false || data.clientData.is_privacy_policy === false){
        showNotification("error", ERROR_MESSAGES['invalid_form'])
    }else{
        startResendTimer(31, 'resendBtn')
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
                            captchaBookingResponse = null
                            code_input.style.borderColor = null
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
        input.value = null
    })

    formCheckboxes.forEach(function(checkbox) {
        checkbox.checked = false
    })

    modalNumbers.forEach(function (input){
        input.value = null
    })

    selectedStartDate = null
    selectedEndDate = null

    resetDates(moment().toDate())

    generateGuestInformationBlocks()

    closeModal(modals.emailModal.id)
}

function handleBookingCaptcha(response){
    captchaBookingResponse = response
    getValidityCaptcha(CAPTCHA_SUBJECTS['booking_captcha'], response)
}

function check_name(name){
    const name_length = name.length
    return (name_length === 0 || (name_length > 0 && name_length > 2 && stringRegex.test(name)));
}