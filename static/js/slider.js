const wrapper = document.querySelector('.content__item_container');
const carousel = document.querySelector('.content_carousel');
const items = document.querySelectorAll('.feedback');
const buttons = document.querySelectorAll('.button');

let itemIndex = 0;
let intervalId;

const createPaginator = () => {
    const paginatorContainer = document.querySelector('.control__paginator');
    paginatorContainer.innerHTML = '';
    for (let i = 0; i < items.length; i++) {
        const circle = document.createElement('i');
        circle.className = 'fa-regular fa-circle';
        paginatorContainer.appendChild(circle);
    }
    const firstPaginatorItem = paginatorContainer.querySelector('i');
    if (firstPaginatorItem) {
        firstPaginatorItem.classList.add('fa-solid');
    }
    updatePaginator();
};

const slideItem = (index) => {
    carousel.style.transform = `translate(-${index * 100}%)`;
};

const updatePaginator = () => {
    const paginatorItems = document.querySelectorAll('.control__paginator i');
    paginatorItems.forEach((item, index) => {
        item.classList.toggle('fa-solid', index === itemIndex);
        item.classList.toggle('fa-regular', index !== itemIndex);
    });
};

const startAutoSlide = () => {
    intervalId = setInterval(() => {
        itemIndex = (itemIndex + 1) % items.length;
        slideItem(itemIndex);
        updatePaginator();
    }, 10000);
};

buttons.forEach((button) => {
    button.addEventListener('click', () => {
        clearInterval(intervalId);
        if (button.id === 'prev') {
            itemIndex = (itemIndex - 1 + items.length) % items.length;
        } else if (button.id === 'next') {
            itemIndex = (itemIndex + 1) % items.length;
        }
        slideItem(itemIndex);
        updatePaginator();
        startAutoSlide();
    });
});

slideItem(itemIndex);
createPaginator();
startAutoSlide();