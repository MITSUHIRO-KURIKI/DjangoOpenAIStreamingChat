var offset       = 100,
    fadein_time  = 1000,
    fadeout_time = 300,
    scroll_time  = 0;

function Back2TopSetDefault() {
    $("#Back2Top").hide();
};
function Back2TopFadeInOut() {
    if ($(window).scrollTop() > offset) {
        $("#Back2Top").fadeIn(fadein_time);
    } else {
        $("#Back2Top").fadeOut(fadeout_time);
    }
};
function Back2TopClick() {
    $('#Back2Top').on('click', function () {
        $("body,html").animate({
            scrollTop: 0,
        }, scroll_time, 'easeInOutCubic');
        return false;
    });
};

// document ready
$(function() {
    Back2TopSetDefault(),
    Back2TopClick();
});
// document scroll
$(document).on('scroll', function() {
    Back2TopFadeInOut();
});