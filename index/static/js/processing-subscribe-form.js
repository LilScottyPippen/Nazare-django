function handleSubscriber(csrf_token) {
    let hasError = false;
    const form = document.getElementById('mailingForm');
    const mail = document.getElementById('input-mail').value;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailRegex.test(mail)){
        hasError = true;
        const errorField = document.getElementById('input-mail');
        errorField.style.border = '2px solid red';
    }

    if (!hasError) {
        const activeFields = document.getElementById('input-mail');
        activeFields.style.border = '';
    }

    $.ajax({
        type: "POST",
        url: "/subscribe/",
        data: {
            'mail': mail
        },
        contentType: "application/x-www-form-urlencoded",
        headers: {
            'X-CSRFToken': csrf_token
        },
        success: function (response) {
            form.reset()
            showNotification(response.status, response.message);
        },
        error: function (response) {
            showNotification(response.responseJSON.status, response.responseJSON.message);
        }
    });
}