let pickerCheckin, pickerCheckout, selectedStartDate, selectedEndDate, inputs, totalCostElement,
    selectedInput, selectedPrice, bookedDates, dateFormat, defaultCheckInDate, defaultCheckOutDate,
    titleElementCheckin, titleElementCheckout, checkInTime, minDate, booking_list, guest_max

function getPikadayConfig(fieldId, defaultDate, onSelectHandler) {
    return {
        field: document.getElementById(fieldId),
        format: getFormatDatepicker(),
        minDate: minDate,
        maxDate: getMaxDateDatepicker(),
        position: 'bottom left',
        defaultDate: defaultDate.isValid() ? defaultDate.toDate() : null,
        setDefaultDate: defaultDate.isValid(),
        onSelect: onSelectHandler,
        toString(date) {
            return getToStringDatepicker(date)
        },
        i18n: getI18nDatepicker(),
        disableDayFn: function (date) {
            const dateString = moment(date).format(dateFormat)
            try {
                return bookedDates.some(range => {
                    const [startDate, endDate] = range.map(d => moment(d).format(dateFormat))
                    return dateString >= startDate && dateString <= endDate
                })
            } catch (TypeError){

            }
        },
        firstDay: 1,
    }
}

document.addEventListener('DOMContentLoaded', function () {
    booking_list = getBookingList() || {}
    inputs = document.querySelectorAll('.form-apartment-items input')
    totalCostElement = document.getElementById('totalCost')
    selectedInput = document.querySelector('.form-apartment-items input.active')
    let selectedInputDataId = selectedInput.getAttribute('data-id')
    selectedPrice = selectedInput ? parseFloat(selectedInput.getAttribute('data-price')) || 0 : 0
    bookedDates = booking_list[selectedInputDataId]
    dateFormat = 'YYYY-MM-DD'
    defaultCheckInDate = moment(document.getElementById('check_in_date').innerText, dateFormat)
    defaultCheckOutDate = moment(document.getElementById('check_out_date').innerText, dateFormat)
    checkInTime = getCheckInTime()
    minDate = calculateMinDate(checkInTime)
    guest_max = getGuestMaxApartment(selectedInputDataId) || 0

    document.querySelectorAll('#datepicker-checkin').forEach(function (element) {
        titleElementCheckin = element.querySelector('.search-apartment-dropdown-title')
    })

    document.querySelectorAll('#datepicker-checkout').forEach(function (element) {
        titleElementCheckout = element.querySelector('.search-apartment-dropdown-title')
    })

    pickerCheckin = new Pikaday(getPikadayConfig('datepicker-checkin', defaultCheckInDate, date => handleDateSelection(date, 'checkin', titleElementCheckin, pickerCheckin)))
    pickerCheckout = new Pikaday(getPikadayConfig('datepicker-checkout', defaultCheckOutDate, date => handleDateSelection(date, 'checkout', titleElementCheckout, pickerCheckout)))

    if (defaultCheckInDate.isValid() && defaultCheckOutDate.isValid()) {
        updateTotalCost(totalCostElement)
    }

    inputs.forEach(function (input) {
        input.addEventListener('click', function () {
            bookedDates = booking_list[input.getAttribute('data-id')] || []

            inputs.forEach(function (otherInput) {
                otherInput.classList.remove('active')
            })

            input.classList.add('active')
            guest_max = input.getAttribute('data-guest')

            resetDates(minDate)
            updateGuestCount(input)
        })
    })

    setDateAfterLoadPage()
})

function setDateAfterLoadPage(){
    const checkin_date_parts = titleElementCheckin.innerText.split('-')
    const checkout_date_parts = titleElementCheckout.innerText.split('-')

    const checkin_date_object = new Date(checkin_date_parts[0], checkin_date_parts[1] - 1, checkin_date_parts[2])
    const checkout_date_object = new Date(checkout_date_parts[0], checkout_date_parts[1] - 1, checkout_date_parts[2])

    if(isValidDate(titleElementCheckin.innerText) && isValidDate(titleElementCheckout.innerText)){
        pickerCheckin.setDate(checkin_date_object)
        pickerCheckin.setMaxDate(checkout_date_object)

        const disable_check_in_date = new Date(checkin_date_object)
        disable_check_in_date.setDate(disable_check_in_date.getDate() + 1)
        pickerCheckout.setDate(checkout_date_object)
        pickerCheckout.setMinDate(disable_check_in_date)
    }
}

function updateTotalCost(totalCostElement) {
    const check_in_date = moment(document.getElementById('check_in_date').innerText, dateFormat)
    const check_out_date = moment(document.getElementById('check_out_date').innerText, dateFormat)
    let selectedInput = document.querySelector('.form-apartment-items input.active')

    selectedPrice = selectedInput ? parseFloat(selectedInput.getAttribute('data-price')) || 0 : 0

    if (check_in_date.isValid() && check_out_date.isValid()) {
        const days = check_out_date.diff(check_in_date, 'days')
        totalCostElement.innerText = selectedPrice * days
    } else {
        totalCostElement.innerText = selectedPrice
    }
}

function updateGuestCount(){
    let guestCount = document.getElementById('guests_count')
    let childrenCount = document.getElementById('children_count')

    if (parseInt(guestCount.innerText) + parseInt(childrenCount.innerText) > guest_max) {
        while (parseInt(guestCount.innerText) + parseInt(childrenCount.innerText) > guest_max) {
            if (parseInt(childrenCount.innerText) > 0) {
                decrementCounter('children')
            } else if (parseInt(guestCount.innerText) > 1) {
                decrementCounter('guests')
            } else {
                break
            }
        }
        generateGuestInformationBlocks()
    }
    guestCount.setAttribute('data-guest', guest_max)
}

function resetDates(minDate){
    document.getElementById('check_in_date').innerText = "ЗАЕЗД"
    document.getElementById('check_out_date').innerText = "ВЫЕЗД"
    const maxDate = getMaxDateDatepicker()

    pickerCheckin.setDate(null)
    pickerCheckout.setDate(null)
    pickerCheckin.setMinDate(minDate)
    pickerCheckin.setMaxDate(maxDate)
    pickerCheckout.setMinDate(minDate)
    pickerCheckout.setMaxDate(maxDate)

    updateTotalCost(totalCostElement)
}

function isDateRangeOverlap(range1, range2) {
    return range1[0] <= range2[1] && range1[1] >= range2[0]
}

function handleDateSelection(date, calendarType, titleElement, pikadayInstance) {
    try {
        if (calendarType === 'checkin') {
            selectedStartDate = moment(date, dateFormat)
            if (selectedStartDate.isValid()) {
                titleElement.textContent = pikadayInstance.toString(date, dateFormat)
                pickerCheckout.setMinDate(moment(date).add(1, 'days').toDate())
                updateTotalCost(totalCostElement)
            }
        } else if (calendarType === 'checkout') {
            selectedEndDate = moment(date, dateFormat)
            if (selectedEndDate.isValid()) {
                titleElement.textContent = pikadayInstance.toString(date, dateFormat)
                pickerCheckin.setMaxDate(moment(date).subtract(1, 'days').toDate())
                updateTotalCost(totalCostElement)
            }
        }
        if (selectedStartDate && selectedEndDate){
            const overlappingRange = bookedDates.some(range =>
                isDateRangeOverlap([moment(selectedStartDate).format(dateFormat), moment(selectedEndDate).format(dateFormat)], range)
            )

            if(overlappingRange){
                showNotification("error", ERROR_MESSAGES['unavailable_period'])
                document.getElementById('check_out_date').innerText = "ВЫЕЗД"
                pickerCheckin.setMinDate(minDate)
                pickerCheckin.setMaxDate(null)
                pickerCheckout.setMaxDate(null)
                updateTotalCost(totalCostElement)
            }
        }
    } catch (error) {
        showNotification("error", error.message)
        resetDates(minDate)
    }
}