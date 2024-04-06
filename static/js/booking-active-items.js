function addActiveClassOnClick(formItemsClass, citizenshipItemsClass) {
    let formItemsContainers = document.querySelectorAll('.' + formItemsClass)

    formItemsContainers.forEach(function(formItemsContainer) {
        let formItems = formItemsContainer.querySelectorAll('.choose-input')
        let citizenshipItems = formItemsContainer.querySelectorAll('.' + citizenshipItemsClass + ' .choose-input')

        formItems.forEach(function(input) {
            input.addEventListener('click', function() {
                formItems.forEach(function(item) {
                    item.classList.remove('active')
                })
                input.classList.add('active')
            })
        })

        citizenshipItems.forEach(function(input) {
            input.addEventListener('click', function() {
                citizenshipItems.forEach(function(item) {
                    item.classList.remove('active')
                })
                input.classList.add('active')
            })
        })

        formItems[0].classList.add('active')
        citizenshipItems[0].classList.add('active')
    })
}

document.addEventListener('DOMContentLoaded', function() {
    addActiveClassOnClick('form-guest-information-item', 'form-guest-information-citizenship-items')
})