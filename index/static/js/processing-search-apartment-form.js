function openSearchApartmentPage(){
    const check_in_date = document.getElementById('check_in_date')
    const check_out_date = document.getElementById('check_out_date')
    const guests_count = parseInt(document.getElementById('guests_count').innerText)
    const children_count = parseInt(document.getElementById('children_count').innerText)
    if (!isValidDate(check_in_date.innerText)) {
         const parentElement = check_in_date.closest('.search-apartment-dropdown');
        parentElement.style.border = '2px solid red';
    } else {
        check_in_date.closest('.search-apartment-dropdown').style.border = '';
    }


    if(!isValidDate(check_out_date.innerText)){
        const parentElement = check_out_date.closest('.search-apartment-dropdown');
        parentElement.style.border = '2px solid red'
    }

    if(isValidDate(check_in_date.innerText) && isValidDate(check_out_date.innerText)){
        window.location = `apartments/${check_in_date.innerText}/${check_out_date.innerText}/${guests_count}/${children_count}`
    }else{
        showNotification('error', ERROR_MESSAGES['invalid_date'])
    }
}

function isValidDate(dateString) {
    const dateRegex = /^\d{4}\-\d{1,2}\-\d{1,2}$/
    return dateRegex.test(dateString);
}