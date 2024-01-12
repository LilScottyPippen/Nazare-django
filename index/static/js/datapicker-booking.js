document.addEventListener('DOMContentLoaded', function () {
    let inputs = document.querySelectorAll('.form-apartment-items input');
    let totalCostElement = document.getElementById('totalCost');

    let selectedInput = document.querySelector('.form-apartment-items input.active');
    let selectedPrice = selectedInput ? parseFloat(selectedInput.getAttribute('data-price')) || 0 : 0;

    let pickerCheckin, pickerCheckout;

    function updateTotalCost() {
        let checkinDate = moment(pickerCheckin.getDate(), 'DD/MM/YYYY');
        let checkoutDate = moment(pickerCheckout.getDate(), 'DD/MM/YYYY');
        let selectedInput = document.querySelector('.form-apartment-items input.active');
        selectedPrice = selectedInput ? parseFloat(selectedInput.getAttribute('data-price')) || 0 : 0;

        if (checkinDate.isValid() && checkoutDate.isValid()) {
            let days = checkoutDate.diff(checkinDate, 'days');
            let totalCost = selectedPrice * days;
            totalCostElement.textContent = 'ИТОГОВАЯ СТОИМОСТЬ: ' + totalCost + ' BYN';
        } else {
            totalCostElement.textContent = 'ИТОГОВАЯ СТОИМОСТЬ: ' + selectedPrice + ' BYN';
        }
    }

    inputs.forEach(function (input) {
        input.addEventListener('click', function () {
            inputs.forEach(function (otherInput) {
                otherInput.classList.remove('active');
            });
            input.classList.add('active');
            updateTotalCost();
        });
    });

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

                updateTotalCost();
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
});
