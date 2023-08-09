document.addEventListener('DOMContentLoaded', function() {
    const callbackForm = document.getElementById('callbackForm');

    function openCallbackForm() {
        callbackForm.style.display = 'flex';
        document.body.style.overflow = 'hidden';

        callbackForm.addEventListener('wheel', function(event) {
            event.preventDefault();
        });

        callbackForm.addEventListener('keydown', function(event) {
            if (event.target.tagName.toLowerCase() !== 'input') {
                event.preventDefault();
            }
        });
    }

    try{
        document.getElementById('navCall').addEventListener('click', openCallbackForm);
    } catch(error) {}
    try {
        document.getElementById('navCallDev').addEventListener('click', openCallbackForm);
    } catch (error) {}
    try{
        document.getElementById('navCallMobile').addEventListener('click', openCallbackForm);
    } catch (error) {}

    document.getElementById('closeCallback').addEventListener('click', function() {
        callbackForm.style.display = 'none';
        document.body.style.overflow = 'auto';
    });
})