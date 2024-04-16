function getFormatDatepicker(){
    return 'YYYY/MM/DD'
}

function getToStringDatepicker(date){
    const year = date.getFullYear()
    const month = ('0' + (date.getMonth() + 1)).slice(-2)
    const day = ('0' + date.getDate()).slice(-2)
    return `${year}-${month}-${day}`
}

function getI18nDatepicker(){
    moment.locale('ru')
    return {
        months: moment.months(),
        weekdays: moment.weekdaysShort(),
        weekdaysShort: moment.weekdaysShort()
    }
}

function getMaxDateDatepicker(){
    return moment().add(180, 'days').toDate()
}