 AOS.init({
     duration: 800,
     easing: 'slide'
 });

 (function($) {

     "use strict";

     $(window).stellar({
         responsive: true,
         parallaxBackgrounds: true,
         parallaxElements: true,
         horizontalScrolling: false,
         hideDistantElements: false,
         scrollProperty: 'scroll'
     });


     var fullHeight = function() {

         $('.js-fullheight').css('height', $(window).height());
         $(window).resize(function() {
             $('.js-fullheight').css('height', $(window).height());
         });

     };
     fullHeight();

     // loader
     var loader = function() {
         setTimeout(function() {
             if ($('#ftco-loader').length > 0) {
                 $('#ftco-loader').removeClass('show');
             }
         }, 1);
     };
     loader();

     // Scrollax
     $.Scrollax();

     var carousel = function() {
         $('.home-slider').owlCarousel({
             loop: true,
             autoplay: true,
             margin: 0,
             animateOut: 'fadeOut',
             animateIn: 'fadeIn',
             nav: false,
             autoplayHoverPause: false,
             items: 1,
             navText: ["<span class='ion-md-arrow-back'></span>", "<span class='ion-chevron-right'></span>"],
             responsive: {
                 0: {
                     items: 1
                 },
                 600: {
                     items: 1
                 },
                 1000: {
                     items: 1
                 }
             }
         });
         $('.carousel-testimony').owlCarousel({
             autoplay: true,
             center: true,
             loop: true,
             items: 1,
             margin: 30,
             stagePadding: 0,
             nav: false,
             navText: ['<span class="ion-ios-arrow-back">', '<span class="ion-ios-arrow-forward">'],
             responsive: {
                 0: {
                     items: 1
                 },
                 600: {
                     items: 1
                 },
                 1000: {
                     items: 2
                 }
             }
         });

     };
     carousel();

     $('nav .dropdown').hover(function() {
         var $this = $(this);
         // 	 timer;
         // clearTimeout(timer);
         $this.addClass('show');
         $this.find('> a').attr('aria-expanded', true);
         // $this.find('.dropdown-menu').addClass('animated-fast fadeInUp show');
         $this.find('.dropdown-menu').addClass('show');
     }, function() {
         var $this = $(this);
         // timer;
         // timer = setTimeout(function(){
         $this.removeClass('show');
         $this.find('> a').attr('aria-expanded', false);
         // $this.find('.dropdown-menu').removeClass('animated-fast fadeInUp show');
         $this.find('.dropdown-menu').removeClass('show');
         // }, 100);
     });


     $('#dropdown04').on('show.bs.dropdown', function() {
         console.log('show');
     });

     // scroll
     var scrollWindow = function() {
         $(window).scroll(function() {
             var $w = $(this),
                 st = $w.scrollTop(),
                 navbar = $('.ftco_navbar'),
                 sd = $('.js-scroll-wrap');

             if (st > 150) {
                 if (!navbar.hasClass('scrolled')) {
                     navbar.addClass('scrolled');
                 }
             }
             if (st < 150) {
                 if (navbar.hasClass('scrolled')) {
                     navbar.removeClass('scrolled sleep');
                 }
             }
             if (st > 350) {
                 if (!navbar.hasClass('awake')) {
                     navbar.addClass('awake');
                 }

                 if (sd.length > 0) {
                     sd.addClass('sleep');
                 }
             }
             if (st < 350) {
                 if (navbar.hasClass('awake')) {
                     navbar.removeClass('awake');
                     navbar.addClass('sleep');
                 }
                 if (sd.length > 0) {
                     sd.removeClass('sleep');
                 }
             }
         });
     };
     scrollWindow();


     var counter = function() {

         $('#section-counter').waypoint(function(direction) {

             if (direction === 'down' && !$(this.element).hasClass('ftco-animated')) {

                 var comma_separator_number_step = $.animateNumber.numberStepFactories.separator(',')
                 $('.number').each(function() {
                     var $this = $(this),
                         num = $this.data('number');
                     console.log(num);
                     $this.animateNumber({
                         number: num,
                         numberStep: comma_separator_number_step
                     }, 7000);
                 });

             }

         }, {
             offset: '95%'
         });

     }
     counter();

     var contentWayPoint = function() {
         var i = 0;
         $('.ftco-animate').waypoint(function(direction) {

             if (direction === 'down' && !$(this.element).hasClass('ftco-animated')) {

                 i++;

                 $(this.element).addClass('item-animate');
                 setTimeout(function() {

                     $('body .ftco-animate.item-animate').each(function(k) {
                         var el = $(this);
                         setTimeout(function() {
                             var effect = el.data('animate-effect');
                             if (effect === 'fadeIn') {
                                 el.addClass('fadeIn ftco-animated');
                             } else if (effect === 'fadeInLeft') {
                                 el.addClass('fadeInLeft ftco-animated');
                             } else if (effect === 'fadeInRight') {
                                 el.addClass('fadeInRight ftco-animated');
                             } else {
                                 el.addClass('fadeInUp ftco-animated');
                             }
                             el.removeClass('item-animate');
                         }, k * 50, 'easeInOutExpo');
                     });

                 }, 100);

             }

         }, {
             offset: '95%'
         });
     };
     contentWayPoint();


     // magnific popup
     $('.image-popup').magnificPopup({
         type: 'image',
         closeOnContentClick: true,
         closeBtnInside: false,
         fixedContentPos: true,
         mainClass: 'mfp-no-margins mfp-with-zoom', // class to remove default margin from left and right side
         gallery: {
             enabled: true,
             navigateByImgClick: true,
             preload: [0, 1] // Will preload 0 - before current, and 1 after the current image
         },
         image: {
             verticalFit: true
         },
         zoom: {
             enabled: true,
             duration: 300 // don't foget to change the duration also in CSS
         }
     });

     $('.popup-youtube, .popup-vimeo, .popup-gmaps').magnificPopup({
         disableOn: 700,
         type: 'iframe',
         mainClass: 'mfp-fade',
         removalDelay: 160,
         preloader: false,

         fixedContentPos: false
     });


     $('.appointment_date').datepicker({
         'format': 'm/d/yyyy',
         'autoclose': true
     });

     $('.appointment_time').timepicker();




 })(jQuery);

 // Custom Bubble Cursor Effect
 const cursor = document.createElement('div');
 cursor.classList.add('cursor');
 document.body.appendChild(cursor);

 // Create small bubble particles
 const particles = [];
 const particleCount = 5; // Number of trailing particles

 // Initialize particles
 for (let i = 0; i < particleCount; i++) {
     const particle = document.createElement('div');
     particle.classList.add('cursor-particle');
     document.body.appendChild(particle);
     particles.push({
         element: particle,
         x: 0,
         y: 0,
         size: Math.random() * 10 + 5, // Random size between 5 and 15
         delay: i * 0.05, // Staggered delay for trailing effect
         xPos: 0,
         yPos: 0
     });
 }

 // Track mouse position
 let mouseX = 0;
 let mouseY = 0;
 let cursorX = 0;
 let cursorY = 0;
 let isHovered = false;

 // Update cursor position with easing
 document.addEventListener('mousemove', (e) => {
     mouseX = e.clientX;
     mouseY = e.clientY;

     // Check if hovering over interactive elements
     const target = e.target;
     const isInteractive = target.matches('a, button, .btn, [role="button"], [onclick], input, textarea, select, label[for]') ||
         target.closest('a, button, .btn, [role="button"], [onclick], input, textarea, select, label[for]');

     if (isInteractive && !isHovered) {
         cursor.classList.add('hover');
         cursor.classList.add('pulse');
         isHovered = true;
     } else if (!isInteractive && isHovered) {
         cursor.classList.remove('hover');
         cursor.classList.remove('pulse');
         isHovered = false;
     }
 });

 // Smooth animation for cursor and particles
 function animateCursor() {
     // Main cursor easing (faster response)
     const cursorEase = 0.2;
     cursorX += (mouseX - cursorX) * cursorEase;
     cursorY += (mouseY - cursorY) * cursorEase;

     // Update main cursor position
     cursor.style.transform = `translate3d(${cursorX}px, ${cursorY}px, 0)`;

     // Update particles with staggered delay
     particles.forEach((particle, index) => {
         // Calculate target position with offset based on movement
         const targetX = mouseX - (mouseX - cursorX) * (1 - particle.delay);
         const targetY = mouseY - (mouseY - cursorY) * (1 - particle.delay);

         // Apply easing to particles (slower than main cursor)
         const particleEase = 0.1 + (index * 0.02); // Slightly different easing for each particle
         particle.xPos += (targetX - particle.xPos) * particleEase;
         particle.yPos += (targetY - particle.yPos) * particleEase;

         // Apply position to particle element
         particle.element.style.transform = `translate3d(${particle.xPos}px, ${particle.yPos}px, 0) scale(${isHovered ? 1.5 : 1})`;

         // Randomize particle size slightly for organic feel
         if (Math.random() > 0.95) {
             particle.size = Math.random() * 10 + 5;
         }

         // Update particle styles
         const size = isHovered ? particle.size * 1.5 : particle.size;
         particle.element.style.width = `${size}px`;
         particle.element.style.height = `${size}px`;
         particle.element.style.opacity = 0.5 - (index * 0.08); // Fade out trailing particles
     });

     requestAnimationFrame(animateCursor);
 }

 // Start animation
 animateCursor();

 // Hide cursor on touch devices
 const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints;
 if (isTouchDevice) {
     cursor.style.display = 'none';
     particles.forEach(particle => {
         particle.element.style.display = 'none';
     });
 }