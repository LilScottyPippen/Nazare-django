const ERROR_MESSAGES = {
    'invalid_form': 'Ошибка в форме.',
    'invalid_date': 'Неверный формат даты. Пожалуйста, выберите другую дату.',
    'unavailable_period': 'Выбранный период пересекается с забронированным периодом. Пожалуйста, выберите другие даты.',
    'invalid_captcha': 'Пройдите reCaptcha.',
    'incorrect_code': 'Код подтверждения неверный.',
}

const SUCCESS_MESSAGES = {

}

const dateFormat = 'YYYY-MM-DD'

const dateRegex = /^\d{4}\-\d{1,2}\-\d{1,2}$/
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const phoneRegex = /^(?:\+375|375)\d{9}$|^(?:\+7|7)\d{10}$/
const stringRegex = /^[\p{L}]+$/u

const errorBorderColor = 'red'
const errorBorderStyle = '2px solid ' + errorBorderColor

let resendCodeMessage = function(duration = null){
    if(duration) {
        return "Отправить код повторно через: " + duration + " секунд"
    }else{
        return "Запросить повторный код подтверждения"
    }
}