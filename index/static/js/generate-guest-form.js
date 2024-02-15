function generateGuestInformationBlocks() {
    const guests_count = parseInt(document.getElementById('guests_count').innerText, 10) || 0;

    document.getElementById('guestInformationContainer').innerHTML = '';

    for (let i = 0; i < guests_count; i++) {
        let guestInformationBlock = document.createElement('div');
        guestInformationBlock.className = 'form-guest-information-item';

        guestInformationBlock.innerHTML = `
            <input id="guest_surname" type="input" class="text-input shadow-normal-blur" placeholder="ФАМИЛИЯ">
            <input id="guest_name" type="input" class="text-input shadow-normal-blur" placeholder="ИМЯ">
            <input id="guest_father_name" type="input" class="text-input shadow-normal-blur" placeholder="ОТЧЕСТВО">
            <div class="form-guest-information-citizenship">
                <div class="form-guest-information-citizenship-title">
                    ГРАЖДАНСТВО:
                </div>
                <div class="form-guest-information-citizenship-items">
                    <input type="button" class="choose-input shadow-normal-blur active" value="РБ">
                    <input type="button" class="choose-input shadow-normal-blur" value="РФ">
                </div>
            </div>
        `;
        document.getElementById('guestInformationContainer').appendChild(guestInformationBlock);
    }
    addActiveClassOnClick('form-guest-information-item', 'form-guest-information-citizenship-items');
}

window.onload = function () {
    generateGuestInformationBlocks();
    document.getElementById('adultIncrement').addEventListener('click', generateGuestInformationBlocks);
    document.getElementById('adultDecrement').addEventListener('click', generateGuestInformationBlocks);
};
