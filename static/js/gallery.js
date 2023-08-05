const galleryContainer = document.querySelector('.gallery-container');
const galleryControlsContainer = document.querySelector('.gallery-controls');
const galleryItems = document.querySelectorAll('.gallery-item');

class Carousel {
  constructor(container, items, controls) {
    this.carouselContainer = container;
    this.carouselControls = controls;
    this.carouselArray = [...items];
    this.setCurrentState('gallery-controls-previous');
    this.updateGallery();
    this.updateDataIndexAttributes();
  }

  updateGallery() {
    this.carouselArray.forEach((el) => {
      for (let i = 1; i <= 5; i++) {
        el.classList.remove(`gallery-item-${i}`);
      }
      el.classList.remove('active');
    });

    const activeItem = this.carouselArray[0];

    this.carouselArray.forEach((el, i) => {
      let index = (i + 3 - this.carouselArray.indexOf(activeItem)) % 5;
      index = index === 0 ? 5 : index;
      el.classList.add(`gallery-item-${index}`);
    });
    activeItem.classList.add('active');
  }

  setCurrentState(direction) {
    if (direction === 'gallery-controls-previous') {
      this.carouselArray.unshift(this.carouselArray.pop());
    } else {
      this.carouselArray.push(this.carouselArray.shift());
    }
    this.updateGallery();
    this.updateDataIndexAttributes();
  }

  updateDataIndexAttributes() {
    this.carouselArray.forEach((el, i) => {
      el.dataset.index = i + 2;
    });
  }

  setControls() {
    galleryControlsContainer.appendChild(document.createElement('button')).className = 'gallery-controls-previous';
    galleryControlsContainer.appendChild(document.createElement('button')).className = 'gallery-controls-next';
  }

  enableSwipe() {
    let xDown = null;
    let yDown = null;

    const handleTouchStart = (e) => {
      const firstTouch = e.touches[0];
      xDown = firstTouch.clientX;
      yDown = firstTouch.clientY;
    };

    const handleTouchMove = (e) => {
      if (!xDown || !yDown) return;

      const xUp = e.touches[0].clientX;
      const yUp = e.touches[0].clientY;

      const xDiff = xDown - xUp;
      const yDiff = yDown - yUp;

      if (Math.abs(xDiff) > Math.abs(yDiff)) {
        if (xDiff < 0) {
          this.setCurrentState('gallery-controls-previous');
        }else{
          this.setCurrentState('gallery-controls-next');
        }
      }

      xDown = null;
      yDown = null;
    };

    this.carouselContainer.addEventListener('touchstart', handleTouchStart);
    this.carouselContainer.addEventListener('touchmove', handleTouchMove);
    this.carouselContainer.addEventListener('mousedown', handleTouchStart);
    this.carouselContainer.addEventListener('mousemove', handleTouchMove);
  }

  disableSwipe() {
    this.carouselContainer.removeEventListener('touchstart', handleTouchStart);
    this.carouselContainer.removeEventListener('touchmove', handleTouchMove);
    this.carouselContainer.removeEventListener('mousedown', handleTouchStart);
    this.carouselContainer.removeEventListener('mousemove', handleTouchMove);
  }

  userControls() {
    const triggers = [...galleryControlsContainer.childNodes];
    triggers.forEach((control) => {
      control.addEventListener('click', (e) => {
        e.preventDefault();
        this.setCurrentState(control.className);
      });
    });

    this.enableSwipe();
  }
}

const exampleCarousel = new Carousel(galleryContainer, galleryItems);
exampleCarousel.setControls();
exampleCarousel.userControls();
