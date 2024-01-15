function incrementCounter(type) {
    let counterId = type + 'Count';
    let counter = document.getElementById(counterId);
    let count = parseInt(counter.innerText);

    if (count < 6) {
        count++;
        counter.innerText = count;
    }
}

function decrementCounter(type) {
    let counterId = type + 'Count';
    let counter = document.getElementById(counterId);
    let count = parseInt(counter.innerText);

    if (type === 'adult' && count > 1) {
        count--;
        counter.innerText = count;
    } else if (type === 'child' && count > 0) {
        count--;
        counter.innerText = count;
    }
}