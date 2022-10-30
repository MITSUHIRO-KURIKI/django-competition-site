$(function () {
    $("#back-to-top").hide();
    $(window).scroll(function () {
        if ($(window).scrollTop() > 500) {
            $("#back-to-top").fadeIn(1000);
        } else {
            $("#back-to-top").fadeOut();
        }
    });
    $("#back-to-top").click(function () {
        $("body,html").animate({
            scrollTop: 0,
        }, 700, 'swing');
        return false;
    });
});