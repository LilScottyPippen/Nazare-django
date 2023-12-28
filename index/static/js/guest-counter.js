function incrementCounter(type) {
    var counterId = type + 'Count';
    var counter = document.getElementById(counterId);
    var count = parseInt(counter.innerText);

    if (count < 6) {
        count++;
        counter.innerText = count;
    }
}

function decrementCounter(type) {
    var counterId = type + 'Count';
    var counter = document.getElementById(counterId);
    var count = parseInt(counter.innerText);

    if (count > 0) {
        count--;
        counter.innerText = count;
    }
}