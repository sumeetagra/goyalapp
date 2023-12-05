$(function () {
    /* set variables locally for increased performance */
    var scroll_timer;
    var displayed = false;
    var $message = $('#message a');
    var $window = $(window);
    var top = $(document.body).children(0).position().top;

    /* react to scroll event on window */
    $window.scroll(function () {
        window.clearTimeout(scroll_timer);
        scroll_timer = window.setTimeout(function () {
            if ($window.scrollTop() <= top) {
                displayed = false;
                $message.fadeOut(500);
            }
            else if (displayed == false) {
                displayed = true;
                $message.stop(true, true).show().click(function () { $message.fadeOut(500); });
            }
        }, 100);
    });
    $('a[href*=#]:not([href=#])').click(function () {
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            if (target.length) {
                $('html,body').animate({
                    scrollTop: target.offset().top
                }, 1000);
                return false;
            }
        }
    });
});

$(document).ready(function () {

    $("#mob-menu").click(function () {
        $(".mmenu_show").toggle("1000");
    });
    $("body").on("contextmenu", "img", function (e) {
        return false;
    });

    //if ($(window).width() > 767) {
    //    var contact_formWidth = $('.reldiv').outerWidth();

    //    $(window).bind('scroll', function () {
    //        $('#contact_form').css('width', contact_formWidth);
    //        var navHeight = $(window).height() - 0;
    //        if ($(window).scrollTop() > navHeight) {
    //            $('#contact_form').removeClass('reldiv');
    //            $('#contact_form').addClass('fixeddiv');
    //        }
    //        else {
    //            $('#contact_form').css('width', '100%');
    //            $('#contact_form').removeClass('fixeddiv');
    //            $('#contact_form').addClass('reldiv');
    //        }
    //    });
    //}
});
$(function () {
    $(".menu_ul li a").each(function () {
        var hreff = this.href.trim().split("/").splice(3, 4);

        if (hreff.length > 1)
            hreff.splice(0, 1);

        if (hreff[0] == window.location.pathname.split("/").splice(1, 1)[0])
            $(this).parent().addClass("active");
    });
});




