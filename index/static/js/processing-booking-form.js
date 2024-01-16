function getClientFormData(method){
    const apartment_id = document.querySelector('.form-apartment-items .choose-input.active').getAttribute('data-id')
    const check_in_date = document.getElementById('span_check_in_date').innerText
    const check_out_date = document.getElementById('span_check_out_date').innerText
    const guests_count = document.getElementById('adultCount').innerText
    const children_count = document.getElementById('childCount').innerText
    const client_surname = document.getElementById('client_surname').value
    const client_name = document.getElementById('client_name').value
    const client_father_name = document.getElementById('client_father_name').value
    const client_phone = document.getElementById('client_phone').value
    const client_mail = document.getElementById('client_mail').value
    const total_sum = document.getElementById('totalCost').innerText

    return {
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
        payment_method: method,
        total_sum: total_sum
    }
}

function getGuestFormData(guestForm) {
    const lastName = guestForm.querySelector('input:nth-child(1)').value;
    const firstName = guestForm.querySelector('input:nth-child(2)').value;
    const fatherName = guestForm.querySelector('input:nth-child(3)').value;
    const citizenship = document.querySelector('.form-guest-information-citizenship-items .choose-input.active').value

    return {
        lastName: lastName,
        firstName: firstName,
        fatherName: fatherName,
        citizenship: citizenship
    };
}

function handlePayment(method) {
    const clientData = getClientFormData(method);

    const guestForms = document.querySelectorAll('.form-guest-information-item');
    const guestData = Array.from(guestForms).map(getGuestFormData);

    const formData = {
        clientData: clientData,
        guestData: guestData
    };

    $.ajax({
        type: "POST",
        url: "/booking",
        data: JSON.stringify(formData),
        contentType: "application/json",
        headers: {
            'X-CSRFToken': window.csrf_token
        },
        success: function(response) {
            console.log(response);
        },
        error: function(xhr, textStatus, errorThrown) {
            console.error('Request failed with status:', xhr.status);
        }
    });
}
