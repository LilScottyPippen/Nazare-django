let pickerCheckin, pickerCheckout
let selectedStartDate, selectedEndDate;
let inputs = document.querySelectorAll('.form-apartment-items input');
let totalCostElement = document.getElementById('totalCost');

let selectedInput = document.querySelector('.form-apartment-items input.active');
let selectedPrice = selectedInput ? parseFloat(selectedInput.getAttribute('data-price')) || 0 : 0;
let bookedDates = booking_list[selectedInput.getAttribute('data-id')] || [];

const dateFormat = 'YYYY-MM-DD'

const defaultCheckInDate = moment(document.getElementById('check_in_date').innerText, dateFormat);
const defaultCheckOutDate = moment(document.getElementById('check_out_date').innerText, dateFormat);

let titleElementCheckin, titleElementCheckout

moment.locale('ru');
let minDate = moment().toDate();

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('#datepicker-checkin').forEach(function (element) {
        titleElementCheckin = element.querySelector('.search-apartment-dropdown-title');
    })

    document.querySelectorAll('#datepicker-checkout').forEach(function (element) {
        titleElementCheckout = element.querySelector('.search-apartment-dropdown-title');
    })

    pickerCheckin = new Pikaday({
        field: document.getElementById('datepicker-checkin'),
        format: 'YYYY/MM/DD',
        minDate: minDate,
        position: 'top left',
        defaultDate: defaultCheckInDate.isValid() ? defaultCheckInDate.toDate() : null,
        setDefaultDate: defaultCheckInDate.isValid(),
        onSelect: function (date) {
            handleDateSelection(date, 'checkin', titleElementCheckin, pickerCheckin);
        },
        toString(date) {
            const year = date.getFullYear();
            const month = ('0' + (date.getMonth() + 1)).slice(-2);
            const day = ('0' + date.getDate()).slice(-2);
            return `${year}-${month}-${day}`;
        },
        parse(dateString) {
            const parts = dateString.split('/');
            const day = parseInt(parts[0], 10);
            const month = parseInt(parts[1], 10) - 1;
            const year = parseInt(parts[2], 10);
            return new Date(year, month, day);
        },
        i18n: {
            months: moment.months(),
            weekdays: moment.weekdaysShort(),
            weekdaysShort: moment.weekdaysShort()
        },
        disableDayFn: function (date) {
            const dateString = moment(date).format(dateFormat);

            return bookedDates.some(range => {
                const [startDate, endDate] = range.map(d => moment(d).format(dateFormat));
                return dateString >= startDate && dateString <= endDate;
            });
        },
        firstDay: 1,
    });

    pickerCheckout = new Pikaday({
        field: document.getElementById('datepicker-checkout'),
        format: 'YYYY/M/D',
        minDate: minDate,
        position: 'top left',
        defaultDate: defaultCheckOutDate.isValid() ? defaultCheckOutDate.toDate() : null,
        setDefaultDate: defaultCheckOutDate.isValid(),
        onSelect: function (date) {
            handleDateSelection(date, 'checkout', titleElementCheckout, pickerCheckout);
        },
        toString(date) {
            const year = date.getFullYear();
            const month = ('0' + (date.getMonth() + 1)).slice(-2);
            const day = ('0' + date.getDate()).slice(-2);
            return `${year}-${month}-${day}`;
        },
        parse(dateString) {
            const parts = dateString.split('/');
            const day = parseInt(parts[0], 10);
            const month = parseInt(parts[1], 10) - 1;
            const year = parseInt(parts[2], 10);
            return new Date(year, month, day);
        },
        i18n: {
            months: moment.months(),
            weekdays: moment.weekdaysShort(),
            weekdaysShort: moment.weekdaysShort()
        },
        disableDayFn: function (date) {
            const dateString = moment(date).format(dateFormat);

            return bookedDates.some(range => {
                const [startDate, endDate] = range.map(d => moment(d).format(dateFormat));
                return dateString >= startDate && dateString <= endDate;
            });
        },
        firstDay: 1,
    });

    if (defaultCheckInDate.isValid() && defaultCheckOutDate.isValid()) {
        updateTotalCost(totalCostElement);
    }

    inputs.forEach(function (input) {
        input.addEventListener('click', function () {
            bookedDates = booking_list[input.getAttribute('data-id')] || [];

            inputs.forEach(function (otherInput) {
                otherInput.classList.remove('active');
            });

            input.classList.add('active');
            guest_max = input.getAttribute('data-guest')

            resetDates(minDate);
            updateGuestCount(input);
        });
    });

    setDateAfterLoadPage()
});

function setDateAfterLoadPage(){
    const checkin_date_parts = titleElementCheckin.innerText.split('-')
    const checkout_date_parts = titleElementCheckout.innerText.split('-')

    const checkin_date_object = new Date(checkin_date_parts[0], checkin_date_parts[1] - 1, checkin_date_parts[2])
    const checkout_date_object = new Date(checkout_date_parts[0], checkout_date_parts[1] - 1, checkout_date_parts[2])

    if(isValidDate(titleElementCheckin.innerText) && isValidDate(titleElementCheckout.innerText)){
        pickerCheckin.setDate(checkin_date_object)
        pickerCheckin.setMaxDate(checkout_date_object)

        const disable_check_in_date = new Date(checkin_date_object);
        disable_check_in_date.setDate(disable_check_in_date.getDate() + 1);
        pickerCheckout.setDate(checkout_date_object)
        pickerCheckout.setMinDate(disable_check_in_date);
    }
}


function updateTotalCost(totalCostElement) {
    const check_in_date = moment(document.getElementById('check_in_date').innerText, dateFormat);
    const check_out_date = moment(document.getElementById('check_out_date').innerText, dateFormat);
    let selectedInput = document.querySelector('.form-apartment-items input.active');

    selectedPrice = selectedInput ? parseFloat(selectedInput.getAttribute('data-price')) || 0 : 0;

    if (check_in_date.isValid() && check_out_date.isValid()) {
        const days = check_out_date.diff(check_in_date, 'days');
        totalCostElement.innerText = selectedPrice * days;
    } else {
        totalCostElement.innerText = selectedPrice;
    }
}

function updateGuestCount(){
    let guestCount = document.getElementById('guests_count');
    let childrenCount = document.getElementById('children_count')

    if (parseInt(guestCount.innerText) + parseInt(childrenCount.innerText) > guest_max) {
        while (parseInt(guestCount.innerText) + parseInt(childrenCount.innerText) > guest_max) {
            if (parseInt(childrenCount.innerText) > 0) {
                decrementCounter('children');
            } else if (parseInt(guestCount.innerText) > 1) {
                decrementCounter('guests');
            } else {
                break;
            }
        }
        generateGuestInformationBlocks();
    }
    guestCount.setAttribute('data-guest', guest_max);
}

function resetDates(minDate){
    document.getElementById('check_in_date').innerText = "ЗАЕЗД";
    document.getElementById('check_out_date').innerText = "ВЫЕЗД";

    pickerCheckin.setDate(null);
    pickerCheckout.setDate(null);
    pickerCheckin.setMinDate(minDate);
    pickerCheckin.setMaxDate(null);
    pickerCheckout.setMinDate(minDate);
    pickerCheckout.setMaxDate(null);

    updateTotalCost(totalCostElement)
}

function isDateRangeOverlap(range1, range2) {
    return range1[0] <= range2[1] && range1[1] >= range2[0];
}

function handleDateSelection(date, calendarType, titleElement, pikadayInstance) {
    try {
        if (calendarType === 'checkin') {
            selectedStartDate = moment(date, dateFormat);
            if (selectedStartDate.isValid()) {
                titleElement.textContent = pikadayInstance.toString(date, dateFormat);
                pickerCheckout.setMinDate(moment(date).add(1, 'days').toDate());
                updateTotalCost(totalCostElement);
            }
        } else if (calendarType === 'checkout') {
            selectedEndDate = moment(date, dateFormat);
            if (selectedEndDate.isValid()) {
                titleElement.textContent = pikadayInstance.toString(date, dateFormat);
                pickerCheckin.setMaxDate(moment(date).subtract(1, 'days').toDate());
                updateTotalCost(totalCostElement);
            }
        }
        if (selectedStartDate && selectedEndDate){
            const overlappingRange = bookedDates.some(range =>
                isDateRangeOverlap([moment(selectedStartDate).format(dateFormat), moment(selectedEndDate).format(dateFormat)], range)
            );

            if(overlappingRange){
                showNotification("error", ERROR_MESSAGES['unavailable_period']);
                document.getElementById('check_out_date').innerText = "ВЫЕЗД";
                pickerCheckin.setMinDate(minDate);
                pickerCheckin.setMaxDate(null);
                pickerCheckout.setMaxDate(null);
                updateTotalCost(totalCostElement)
            }
        }
    } catch (error) {
        showNotification("error", error.message);
        resetDates(minDate);
    }
}