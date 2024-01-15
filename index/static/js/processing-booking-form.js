function setElementValue(id, value) {
    document.getElementById(id).value = value;
}

function getElementValue(selector) {
    return document.querySelector(selector).innerText;
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
    const activeChooseInput = document.querySelector('.choose-input.active');
    const guestFormContainer = document.getElementById('guest-form');

    setElementValue('id_apartment', activeChooseInput.getAttribute('data-id'));
    setElementValue('id_check_in_date', getElementValue('#span_check_in_date'));
    setElementValue('id_check_out_date', getElementValue('#span_check_out_date'));
    setElementValue('id_guests_count', getElementValue('#adultCount'));
    setElementValue('id_children_count', getElementValue('#childCount'));
    setElementValue('id_client_surname', document.getElementById('client_surname').value);
    setElementValue('id_client_name', document.getElementById('client_name').value);
    setElementValue('id_client_father_name', document.getElementById('client_father_name').value);
    setElementValue('id_client_phone', document.getElementById('client_phone').value);
    setElementValue('id_client_mail', document.getElementById('client_mail').value);
    setElementValue('id_total_sum', getElementValue('#totalCost'));
    setElementValue('id_payment_method', method);

    const formDataArray = [];
    const guestForms = document.querySelectorAll('.form-guest-information-item');

    guestForms.forEach((guestForm, index) => {
        formDataArray.push(getGuestFormData(guestForm));
    });

    guestForms.forEach((form, index) => {
        const guestForm = guestFormContainer.querySelector(`#id_form-${index}-guest_name`);

        if (guestForm) {
            const inputFields = guestFormContainer.querySelectorAll(`[id^="id_form-${index}"]`);
            const formData = formDataArray[index];

            inputFields[0].value = formData.lastName || '';
            inputFields[1].value = formData.firstName || '';
            inputFields[2].value = formData.fatherName || '';
            inputFields[3].value = formData.citizenship || '';
        }
    });
}