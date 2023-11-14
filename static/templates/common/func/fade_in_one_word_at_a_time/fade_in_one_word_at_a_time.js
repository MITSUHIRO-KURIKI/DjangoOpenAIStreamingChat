// rem → px 変換
function ConvertRem2Px(rem) {
    let fontSize = getComputedStyle(document.documentElement).fontSize;
    return rem * parseFloat(fontSize);
};

function fadeInOneWord() {
    let intervalTime = 50,
        actTime      = intervalTime;
    $('.fade-in-one-word').each(function () {
            if ( $(this).data('cs-fade-in-one-word-offset') ) {
                var offSet = $(this).data('cs-fade-in-one-word-offset');
            } else {
                var offSet = ConvertRem2Px(10);
            };
            let parent       = this,
                childs       = $(this).children(),
                elemPos      = $(this).offset().top + offSet,
                winScrollTop = $(window).scrollTop(),
                winHeight    = $(window).height();
            if (winScrollTop >= elemPos - winHeight && !$(parent).hasClass('play')) {
                    $(childs).each(function () {
                            if (!$(this).hasClass('fadeInOneWordHandler')) {
                                    $(parent).addClass('play');
                                    $(this).css('animation-delay', actTime + "ms");
                                    $(this).addClass('fadeInOneWordHandler');
                                    actTime = actTime + intervalTime + Math.floor(Math.random() * 50);
                                    var index = $(childs).index(this);
                                    if((childs.length-1) == index){
                                            $(parent).removeClass('play');
                                    }
                            }
                    });
                    $(this).next().css('animation-delay', actTime + "ms");
            }
    });
};

// document ready
$(function() {
    fadeInOneWord();
});
// document scroll
$(document).on('scroll', function() {
    fadeInOneWord();
});