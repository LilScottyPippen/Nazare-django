var pickerCheckin, pickerCheckout;

document.querySelectorAll('#datepicker-checkin, #datepicker-checkout').forEach(function (element) {
    moment.locale('ru');
    let minDate = moment().toDate();
    let maxDate = moment().add(365, 'days');
    let titleElement = element.querySelector('.search-apartment-dropdown-title');

    let picker = new Pikaday({
        field: element,
        format: 'D/M/YYYY',
        minDate: minDate,
        maxDate: maxDate.toDate(),
        onSelect: function (date) {
            titleElement.textContent = this.toString(date, 'D/M/YYYY');
            
            if (element.id === 'datepicker-checkin') {
                pickerCheckout.setMinDate(moment(date).add(1, 'days').toDate());
            } else if (element.id === 'datepicker-checkout') {
                pickerCheckin.setMaxDate(moment(date).subtract(1, 'days').toDate());
            }
        },
        toString(date, format) {
            const day = date.getDate();
            const month = date.getMonth() + 1;
            const year = date.getFullYear();
            return `${day}/${month}/${year}`;
        },
        parse(dateString, format) {
            const parts = dateString.split('/');
            const day = parseInt(parts[0], 10);
            const month = parseInt(parts[1], 10) - 1;
            const year = parseInt(parts[2], 10);
            return new Date(year, month, day);
        },
        i18n: {
            previousMonth: 'Предыдущий месяц',
            nextMonth: 'Следующий месяц',
            months: moment.months(),
            weekdays: moment.weekdaysShort(),
            weekdaysShort: moment.weekdaysShort()
        }
    });

    if (element.id === 'datepicker-checkin') {
        pickerCheckin = picker;
    } else if (element.id === 'datepicker-checkout') {
        pickerCheckout = picker;
    }
});