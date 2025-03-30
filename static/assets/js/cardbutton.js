document.addEventListener("DOMContentLoaded",
  function () {
    const swiper = new Swiper('.swiper', {
      slidesPerView: 1,
      spaceBetween: 15,
      breakpoints: {
        768: {
          slidesPerView: 3
        }
      },

      // If we need pagination
      pagination: {
        el: '.swiper-pagination',
        clickable: true,
      },
    });
    const swiper1 = new Swiper('.swiper1', {
      slidesPerView: 1,
      spaceBetween: 15,
      breakpoints: {
        768: {
          slidesPerView: 3
        }
      },
      
      // If we need pagination
      pagination: {
        el: '.swiper-pagination',
        clickable: true,
      },
    });
    const swiperuongozi = new Swiper('.swiperuongozi', {
      slidesPerView: 1,
      spaceBetween: 15,
      loop: true,
      breakpoints: {
        768: {
          slidesPerView: 3
        }
      },
      autoplay: {
        delay: 2000,
      },

      // If we need pagination
      pagination: {
        el: '.swiper-pagination',
        clickable: true,
      },
    });
    const swiperuongozi1 = new Swiper('.swiperuongozi1', {
      slidesPerView: 1,
      spaceBetween: 15,
      loop: true,
      breakpoints: {
        768: {
          slidesPerView: 3
        }
      },
      autoplay: {
        delay: 2000,
      },

      // If we need pagination
      pagination: {
        el: '.swiper-pagination',
        clickable: true,
      },
    });
    const swiperuongozi2 = new Swiper('.swiperuongozi2', {
      slidesPerView: 1,
      spaceBetween: 15,
      loop: true,
      breakpoints: {
        768: {
          slidesPerView: 3
        }
      },
      autoplay: {
        delay: 2000,
      },

      // If we need pagination
      pagination: {
        el: '.swiper-pagination',
        clickable: true,
      },
    });
  });

