function makeAjaxRequest(options) {
    let result

    $.ajax({
        type: options.type,
        async: options.async,
        url: options.url,
        dataType: 'json',
        success: function(response) {
            result = response
        },
        error: function() {
            result = null
        }
    });

    return result;
}

function getBookingList() {
    return makeAjaxRequest({
        type: "GET",
        async: false,
        url: '/api/get-booking-list'
    });
}

function getGuestMax() {
    let result = makeAjaxRequest({
        type: "GET",
        async: false,
        url: '/api/get-guest-max'
    });

    return result ? result.guest_max : null
}

function getGuestMaxApartment(apartment_id) {
    let result = makeAjaxRequest({
        type: "GET",
        async: false,
        url: `/api/get-guest-max/${apartment_id}`
    });

    return result ? result.guest_max : null
}

function getCheckInTime() {
    let result = makeAjaxRequest({
        type: "GET",
        async: false,
        url: '/api/get-check-in-time'
    });

    return result ? result.check_in_time : null
}

function getCheckOutTime() {
    let result = makeAjaxRequest({
        type: "GET",
        async: false,
        url: '/api/get-check-out-time'
    });

    return result ? result.check_in_time : null
}

function getMaxBookingPeriod(){
    let result = makeAjaxRequest({
        type: "GET",
        async: false,
        url: '/api/get-max-booking-period'
    })

    return result ? result.booking_period : null
}

function getValidityCaptcha(subject, value){
    return makeAjaxRequest({
        type: "GET",
        async: false,
        url: `/api/get-validity-captcha/${subject}/${value}`
    })
}