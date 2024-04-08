function sumCounters() {
    const adultsCount = parseInt(document.getElementById('guests_count').innerText)
    const childrenCount = parseInt(document.getElementById('children_count').innerText)

    const total = adultsCount + childrenCount

    try{
        return total < guest_max
    }
    catch (ReferenceError) {
        return total < getGuestMax() || 0
    }
}

function incrementCounter(type) {
    let counterId = type + '_count'
    let counter = document.getElementById(counterId)
    let count = counter.innerText

    if (sumCounters()) {
        count++
        counter.innerText = count
    }
}

function decrementCounter(type) {
    let counterId = type + '_count'
    let counter = document.getElementById(counterId)
    let count = counter.innerText

    sumCounters()

    if (type === 'guests' && count > 1) {
        count--
        counter.innerText = count
    } else if (type === 'children' && count > 0) {
        count--
        counter.innerText = count
    }
}