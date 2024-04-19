let resendTimer

function startResendTimer(interval, text_id) {
    let duration = interval
    let display = document.getElementById(text_id);

    if (resendTimer) {
        return;
    }

    updateDisplay();

    resendTimer = setInterval(function() {
        if (duration > 0) {
            display.textContent = resendCodeMessage(duration);
            duration--;
        } else {
            clearInterval(resendTimer);
            resendTimer = null;
            display.textContent = resendCodeMessage();
            display.style.textDecoration = "underline";
            display.style.cursor = "pointer";
            display.setAttribute("onclick", "resendCode()");
        }
    }, 1000);

    function updateDisplay() {
        display.textContent = resendCodeMessage(duration);
        display.style.textDecoration = "none"
        display.removeAttribute("onclick")
        display.style.cursor = "default"
    }
}

function resendCode(){
    $.ajax({
        type: "GET",
        url: `/api/send_confirmation_code/${document.getElementById('client_mail').value}`,
        contentType: "application/json",
        success: function(response) {
            openEmailModal()
            startResendTimer(31, 'resendBtn')
            showNotification(response.status, response.message)
        },
        error: function(response) {
            showNotification(response.responseJSON.status, response.responseJSON.message)
        }
    })
}