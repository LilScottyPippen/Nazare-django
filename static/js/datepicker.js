let pickerCheckin, pickerCheckout
const checkInTime = getCheckInTime()
let minDate = calculateMinDate(checkInTime)

document.querySelectorAll('#datepicker-checkin, #datepicker-checkout').forEach(function (element) {
    let titleElement = element.querySelector('.search-apartment-dropdown-title')

    let picker = new Pikaday({
        field: element,
        format: getFormatDatepicker(),
        minDate: minDate,
        maxDate: getMaxDateDatepicker(),
        onSelect: function (date) {
            titleElement.textContent = this.toString(date, getFormatDatepicker())
            
            if (element.id === 'datepicker-checkin') {
                pickerCheckout.setMinDate(moment(date).add(1, 'days').toDate())
            } else if (element.id === 'datepicker-checkout') {
                pickerCheckin.setMaxDate(moment(date).subtract(1, 'days').toDate())
            }
        },
        toString(date) {
            return getToStringDatepicker(date)
        },
        i18n: getI18nDatepicker(),
        firstDay: 1,
    })

    if (element.id === 'datepicker-checkin') {
        pickerCheckin = picker
    } else if (element.id === 'datepicker-checkout') {
        pickerCheckout = picker
    }
})