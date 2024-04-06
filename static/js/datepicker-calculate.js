function calculateMinDate(checkInTime) {
    const [hours, minutes] = checkInTime.split(':').map(str => parseInt(str, 10))
    const minDate = new Date()
    const currentHour = minDate.getHours()
    const currentMinute = minDate.getMinutes()

    if (currentHour > hours || (currentHour === hours && currentMinute > minutes)) {
        minDate.setDate(minDate.getDate() + 1)
    }

    return minDate
}