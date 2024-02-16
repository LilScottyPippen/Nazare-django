function isValidDate(dateString) {
    const dateRegex = /^\d{4}\-\d{1,2}\-\d{1,2}$/
    return dateRegex.test(dateString);
}