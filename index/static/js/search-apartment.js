function openSearchApartmentPage(){
    const check_in_date = document.getElementById('check_in_date').innerText
    const check_out_date = document.getElementById('check_out_date').innerText
    const guests_count = parseInt(document.getElementById('guests_count').innerText)
    const children_count = parseInt(document.getElementById('children_count').innerText)

    if(isValidDate(check_in_date) && isValidDate(check_out_date)){
        window.location.href = `/apartments/${check_in_date}/${check_out_date}/${guests_count}/${children_count}`
    }else{
        showNotification('error', ERROR_MESSAGES['invalid_date'])
    }
}

function isValidDate(dateString) {
    const dateRegex = /^\d{4}\-\d{1,2}\-\d{1,2}$/
    return dateRegex.test(dateString);
}