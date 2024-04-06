let check_in_date = document.getElementById('check_in_date').innerText
let check_out_date = document.getElementById('check_out_date').innerText

const checkin_date_parts = check_in_date.split('-')
const checkout_date_parts = check_out_date.split('-')

const checkin_date_object = new Date(checkin_date_parts[0], checkin_date_parts[1] - 1, checkin_date_parts[2])
const checkout_date_object = new Date(checkout_date_parts[0], checkout_date_parts[1] - 1, checkout_date_parts[2])

if (isValidDate(check_in_date) && isValidDate(check_out_date)) {
    pickerCheckin.setDate(checkin_date_object)
    pickerCheckin.setMaxDate(checkout_date_object)

    const disable_check_in_date = new Date(checkin_date_object)
    disable_check_in_date.setDate(disable_check_in_date.getDate() + 1)
    pickerCheckout.setDate(checkout_date_object)
    pickerCheckout.setMinDate(disable_check_in_date)
}

function openSearchApartmentPage(){
    check_in_date = document.getElementById('check_in_date').innerText
    check_out_date = document.getElementById('check_out_date').innerText
    const guests_count = parseInt(document.getElementById('guests_count').innerText)
    const children_count = parseInt(document.getElementById('children_count').innerText)

    if(isValidDate(check_in_date) && isValidDate(check_out_date)){
        window.location.href = `/apartments/${check_in_date}/${check_out_date}/${guests_count}/${children_count}`
    }else{
        showNotification('error', ERROR_MESSAGES['invalid_date'])
    }
}