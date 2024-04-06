document.addEventListener('DOMContentLoaded', function() {
    let forms = document.getElementsByTagName('form')
    for (let i = 0; i < forms.length; i++) {
        forms[i].addEventListener('submit', function(event) {
            event.preventDefault()
        })
    }
})