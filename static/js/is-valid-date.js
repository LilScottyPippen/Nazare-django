function isValidDate(dateString) {
    return dateRegex.test(dateString)
}

function isDateRangeOverlap(range1, range2) {
    return range1[0] <= range2[1] && range1[1] >= range2[0]
}