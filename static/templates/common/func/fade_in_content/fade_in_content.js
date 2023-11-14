// rem → px 変換
function ConvertRem2Px(rem) {
    let fontSize = getComputedStyle(document.documentElement).fontSize;
    return rem * parseFloat(fontSize);
};

function fadeUpAnime() {
    $('.fade-up-content').each(function () {
        if ( $(this).data('cs-fade-up-content-offset') ) {
            var offSet = $(this).data('cs-fade-up-content-offset');
        } else {
            var offSet = ConvertRem2Px(10);
        };
        let elemPos = $(this).offset().top + offSet,
            winScrollTop = $(window).scrollTop(),
            winHeight    = $(window).height();
        if (winScrollTop >= elemPos - winHeight) {
            $(this).addClass('fadeUpContent');
        };
    });
}

// document ready
$(function() {
    fadeUpAnime();
});
// document scroll
$(document).on('scroll', function() {
    fadeUpAnime();
});