(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();


    // Initiate the wowjs
    new WOW().init();


    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.sticky-top').addClass('shadow-sm').css('top', '0px');
        } else {
            $('.sticky-top').removeClass('shadow-sm').css('top', '-100px');
        }
    });
    $(window).scroll(function () {
        if ($(this).scrollTop() > 1200) {
            $('.stickyjob').addClass('shadow-sm').css('top', '-300px');
        } else {
            $('.stickyjob').removeClass('shadow-sm').css('top', '125px');
        }
    });

    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({ scrollTop: 0 }, 1500, 'easeInOutExpo');
        return false;
    });


    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        items: 1,
        dots: true,
        loop: true,
    });


})(jQuery);




$(document).ready(function () {

    $('.counter').each(function () {
        $(this).prop('Counter', 0).animate({
            Counter: $(this).text()
        }, {
            duration: 4000,
            easing: 'swing',
            step: function (now) {
                $(this).text(Math.ceil(now));
            }
        });
    });

});



$(document).ready(function () {
    $(".nav-tabs a").click(function () {
        $(this).tab('show');
    });
});


if (localStorage.getItem('cookieSeen') != 'shown') {
    $(".cookie-banner").delay(2000).fadeIn();
    localStorage.setItem('cookieSeen', 'shown')
}

$('.close').click(function (e) {
    $('.cookie-banner').fadeOut();
});



$(document).ready(function () {

    $('.slick-wrap').on('init', function (event, slick) {
        var dots = $('.slick-dots li');
        console.log('SRANZAN VEE');
        dots.each(function (k, v) {
            $(this).find('button').addClass('heading' + k);
        });
        var items = slick.$slides;
        items.each(function (k, v) {
            var text = $(this).find('h2').text();
            $('.heading' + k).text(text);
        });
    });
    $('.slick-wrap').slick({
        dots: true,
        focusOnSelect: true,
        infinite: true,
        arrows: true,
        speed: 300,
        slidesToShow: 5,
        slidesToScroll: 2,
        centerMode: true,
        autoplay: true,
        autoplaySpeed: 2000,
        centerPadding: '30px',
    });

    $('.one-time').slick({
        dots: true,
        infinite: true,
        speed: 300,
        slidesToShow: 1,
        autoplay: true,
        autoplaySpeed: 2000,
        adaptiveHeight: true
    });
});


if (localStorage.getItem('cookieSeen') != 'shown') {
    $(".cookie-banner").delay(2000).fadeIn();
    localStorage.setItem('cookieSeen', 'shown')
}

$('.close').click(function (e) {
    $('.cookie-banner').fadeOut();
});

$(document).ready(function () {

    $('.slick-wrap').on('init', function (event, slick) {
        var dots = $('.slick-dots li');
        console.log('SRANZAN VEE');
        dots.each(function (k, v) {
            $(this).find('button').addClass('heading' + k);
        });
        var items = slick.$slides;
        items.each(function (k, v) {
            var text = $(this).find('h2').text();
            $('.heading' + k).text(text);
        });
    });
    $('.slick-wrap').slick({
        dots: true,
        focusOnSelect: true,
        infinite: true,
        arrows: true,
        speed: 300,
        slidesToShow: 5,
        slidesToScroll: 2,
        centerMode: true,
        autoplay: true,
        autoplaySpeed: 2000,
        centerPadding: '30px',
    });

    $('.one-time').slick({
        dots: true,
        infinite: true,
        speed: 300,
        slidesToShow: 1,
        autoplay: true,
        autoplaySpeed: 2000,
        adaptiveHeight: true
    });
});


// profile tab

function openCity(evt, cityName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
}

// Get the element with id="defaultOpen" and click on it
document.getElementById("defaultOpen").click();