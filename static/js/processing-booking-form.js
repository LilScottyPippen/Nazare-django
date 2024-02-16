function getClientFormData(method){
    let hasError = false;
    let apartment_id

    try {
        apartment_id = document.querySelector('.form-apartment-items .choose-input.active').getAttribute('data-id');
    } catch (error) {
        hasError = true;
        const errorFields = document.querySelectorAll('.form-apartment-items .choose-input');
        errorFields.forEach((field) => {
            field.style.borderColor = 'red';
        });
    }

    if (!hasError) {
        const activeFields = document.querySelectorAll('.form-apartment-items .choose-input');
        activeFields.forEach((field) => {
            field.style.borderColor = '';
        });
    }

    const formData = {
        apartment: apartment_id,
        check_in_date: document.getElementById('check_in_date').innerText,
        check_out_date: document.getElementById('check_out_date').innerText,
        guests_count: document.getElementById('guests_count').innerText,
        children_count: document.getElementById('children_count').innerText,
        client_surname: document.getElementById('client_surname').value,
        client_name: document.getElementById('client_name').value,
        client_father_name: document.getElementById('client_father_name').value,
        client_phone: document.getElementById('client_phone').value,
        client_mail: document.getElementById('client_mail').value,
    }

    const nameFields = ['client_surname', 'client_name', 'client_father_name'];
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const dateRegex = /^\d{4}\-\d{1,2}\-\d{1,2}$/;
    const phoneRegex = /^(?:\+375|375)\d{9}$|^(?:\+7|7)\d{10}$/;

    for (const key in formData) {
        const input = document.getElementById(key);
        const parentElement = input.closest('.search-apartment-dropdown');

        if (nameFields.includes(key)) {
            const fullNamePart = formData[key];
            if (!fullNamePart.trim() || !/^[\p{L}]+$/u.test(fullNamePart) || fullNamePart.length < 3) {
                hasError = true;
                if (input) {
                    input.style.borderColor = 'red';
                    if (parentElement) {
                        parentElement.style.borderColor = 'red';
                    }
                }
            } else {
                input.style.borderColor = '';
                if (parentElement) {
                    parentElement.style.borderColor = '';
                }
            }
        } else if (key === 'client_phone' && !phoneRegex.test(formData[key])) {
            hasError = true;
            input.style.borderColor = 'red';
            if (parentElement) {
                parentElement.style.borderColor = 'red';
            }
        } else {
            if (!formData[key]) {
                hasError = true;
                if (input) {
                    input.style.borderColor = 'red';
                    if (parentElement) {
                        parentElement.style.borderColor = 'red';
                    }
                }
            } else {
                input.style.borderColor = '';
                if (parentElement) {
                    parentElement.style.borderColor = '';
                }
            }

            if (key === 'check_in_date' || key === 'check_out_date') {
                if (!dateRegex.test(formData[key])) {
                    hasError = true;
                    parentElement.style.borderColor = 'red';
                } else {
                    parentElement.style.borderColor = '';
                }
            }

            if (key === 'client_mail' && !emailRegex.test(formData[key])) {
                hasError = true;
                input.style.borderColor = 'red';
                if (parentElement) {
                    parentElement.style.borderColor = 'red';
                }
            }
        }
    }

    const privacy_policy_block = document.querySelector('.form-privacy-policy')
    const privacy_policy = document.getElementById('privacy_policy')
    const is_checked = privacy_policy.checked

    if (is_checked === false) {
        privacy_policy_block.style.border = '2px solid red';
    } else {
        privacy_policy_block.style.border = '';
    }

    if (hasError) {
        return false;
    }

    formData.payment_method = method;
    formData.total_sum = document.getElementById('totalCost').innerText
    formData.is_privacy_policy = is_checked

    return formData;
}

function getGuestFormData(guestForm) {
    let hasError = false;

    let citizenship = guestForm.querySelectorAll('.form-guest-information-citizenship-items .choose-input');

    try {
        if(Array.from(citizenship).find(button => button.classList.contains('active')).value) {
            citizenship = guestForm.querySelector('.form-guest-information-citizenship-items .choose-input.active');
        }
    } catch (error) {
        hasError = true;
        const errorFields = document.querySelectorAll('.form-guest-information-citizenship-items .choose-input');
        errorFields.forEach((field) => {
            field.style.borderColor = 'red';
        });
    }

    if (!hasError) {
        const activeFields = document.querySelectorAll('.form-guest-information-citizenship-items .choose-input');
        activeFields.forEach((field) => {
            field.style.borderColor = '';
        });
    }

    const formData = {
        guest_surname: guestForm.querySelector('.text-input[id="guest_surname"]').value,
        guest_name: guestForm.querySelector('.text-input[id="guest_name"]').value,
        guest_father_name: guestForm.querySelector('.text-input[id="guest_father_name"]').value,
        citizenship: citizenship.value,
    };

    const nameRegex = /^[\p{L}]+$/u;

    for (const key in formData) {
        const input = guestForm.querySelector(`#${key}`);

        if (!formData[key]) {
            hasError = true;
            if (input) {
                input.style.borderColor = 'red';
            }
        } else {
            if (input) {
                input.style.borderColor = '';
            }
        }

        if(key === 'guest_name' || key === 'guest_surname' || key === 'guest_father_name'){
            if(formData[key].length < 3 || !nameRegex.test(formData[key])){
                hasError = true
                input.style.borderColor = 'red';
            } else{
                input.style.borderColor = ''
            }
        }
    }

    if (hasError) {
        return false;
    }

    return formData;
}

function handlePayment(method, csrf_token) {
    const clientData = getClientFormData(method);
    const guestData = [];

    const guestForms = document.querySelectorAll('.form-guest-information-item');

    guestForms.forEach((form) => {
        const formData = getGuestFormData(form);
        if (formData !== null) {
            guestData.push(formData);
        }
    });

    const formData = {
        clientData: clientData,
        guestData: guestData
    };

    if (clientData === false || guestData === false){
         showNotification("error", ERROR_MESSAGES['invalid_form']);
    }else{
        $.ajax({
            type: "POST",
            url: "/booking",
            data: JSON.stringify(formData),
            contentType: "application/json",
            headers: {
                'X-CSRFToken': csrf_token
            },
            success: function(response) {
                clearForm()
                showNotification(response.status, response.message);
            },
            error: function(response) {
                showNotification(response.responseJSON.status, response.responseJSON.message);
            }
        });
    }
}

function clearForm() {
    let formInputs = document.querySelectorAll('.booking-form input[type="input"]');
    let formCheckboxes = document.querySelectorAll('.booking-form input[type="checkbox"]');
    document.getElementById('children_count').innerText = 0
    document.getElementById('guests_count').innerText = 1

    formInputs.forEach(function(input) {
        input.value = '';
    });

    formCheckboxes.forEach(function(checkbox) {
        checkbox.checked = false;
    });

    resetDates(moment().toDate())

    generateGuestInformationBlocks();
}