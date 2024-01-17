function getClientFormData(method){
    let hasError = false;

    const apartment_id = document.querySelector('.form-apartment-items .choose-input.active').getAttribute('data-id')
    const check_in_date = document.getElementById('check_in_date').innerText
    const check_out_date = document.getElementById('check_out_date').innerText
    const guests_count = document.getElementById('guests_count').innerText
    const children_count = document.getElementById('children_count').innerText
    const client_surname = document.getElementById('client_surname').value
    const client_name = document.getElementById('client_name').value
    const client_father_name = document.getElementById('client_father_name').value
    const client_phone = document.getElementById('client_phone').value
    const client_mail = document.getElementById('client_mail').value
    const total_sum = document.getElementById('totalCost').innerText
    const privacy_policy = document.getElementById('privacy_policy')

    const formData = {
        apartment: apartment_id,
        check_in_date: check_in_date,
        check_out_date: check_out_date,
        guests_count: guests_count,
        children_count: children_count,
        client_surname: client_surname,
        client_name: client_name,
        client_father_name: client_father_name,
        client_phone: client_phone,
        client_mail: client_mail,
    }

    for (const key in formData) {
        const input = document.getElementById(key);
        const dateRegex = /^\d{4}-(0?[1-9]|1[0-2])-(0?[1-9]|[12]\d|3[01])$/;

        if (!formData[key]) {
            hasError = true;
            if (input) {
                input.style.borderColor = 'red';
                const parentElement = input.closest('.search-apartment-dropdown');
                if (parentElement) {
                    parentElement.style.borderColor = 'red';
                }
            }
        } else {
            input.style.borderColor = '';
            const parentElement = input.closest('.search-apartment-dropdown');
            if (parentElement) {
                parentElement.style.borderColor = '';
            }
        }

        if (key === 'check_in_date' || key === 'check_out_date') {
            const parentElement = input.closest('.search-apartment-dropdown');

            if (!dateRegex.test(formData[key])) {
                hasError = true;
                parentElement.style.borderColor = 'red';
            } else {
                parentElement.style.borderColor = '';
            }
        }
    }

    const is_checked = privacy_policy.checked

    if (hasError) {
        return false;
    }

    formData.payment_method = method;
    formData.total_sum = total_sum
    formData.is_privacy_policy = is_checked

    return formData;
}

function getGuestFormData(guestForm) {
    let hasError = false;

    const lastName = guestForm.querySelector('.text-input[id="guest_surname"]');
    const firstName = guestForm.querySelector('.text-input[id="guest_name"]');
    const fatherName = guestForm.querySelector('.text-input[id="guest_father_name"]');
    const citizenship = guestForm.querySelector('.form-guest-information-citizenship-items .choose-input.active');

    const formData = {
        guest_surname: lastName.value,
        guest_name: firstName.value,
        guest_father_name: fatherName.value,
        citizenship: citizenship ? citizenship.value : null
    };

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
    }

    if (hasError) {
        return false;
    }

    return formData;
}

function handlePayment(method) {
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
         showNotification("error", "Форма не заполнена");
    }else{
        $.ajax({
            type: "POST",
            url: "/booking",
            data: JSON.stringify(formData),
            contentType: "application/json",
            headers: {
                'X-CSRFToken': window.csrf_token
            },
            success: function(response) {
                showNotification(response.status, response.message);
            },
            error: function(response) {
                showNotification(response.responseJSON.status, response.responseJSON.message);
            }
        });
    }
}
