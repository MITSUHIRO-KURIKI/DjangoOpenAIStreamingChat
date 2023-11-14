var navber_transition    = 300,
    startPos             = 0,
    navber_height_rem    = 3,
    in_page_anker_transition_speed = 0;

// rem → px 変換
function ConvertRem2Px(rem) {
    let fontSize = getComputedStyle(document.documentElement).fontSize;
    return rem * parseFloat(fontSize);
};
// Navber すりガラス(HERO初期値)
function HeroAreaNavSetDefault() {
    let offSet       = ConvertRem2Px(navber_height_rem),
        winScrollTop = $(window).scrollTop(),
        heroBottom   = $('#HeroArea').height() - offSet;
    if(winScrollTop <= heroBottom) {
        $('#NavbarItem').addClass('frosted-glass');
    };
};
// スクロールで Navber を隠す
function NavberHide() {
    let offSet       = ConvertRem2Px(navber_height_rem),
        winScrollTop = $(window).scrollTop(),
        heroBottom   = $('#HeroArea').height() - offSet;
    // Navbar の表示非表示
    if (winScrollTop >= startPos ) {
        if(winScrollTop >= heroBottom){
            $('#Navbar').addClass('hide');
        };
    } else {
        $('#Navbar').removeClass('hide');
    };
    startPos = winScrollTop;
    // Navber すりガラス
    if(winScrollTop <= heroBottom){
        $('#NavbarItem').addClass('frosted-glass');
    } else {
        $('#NavbarItem').removeClass('frosted-glass');
    };
};
// Toggler 使用時 Navbar の色リセット
function NavberColorReset() {
    $('#TogglerNavigation').on('click', function () {
        if ( $('#NavbarItem').hasClass('navber-color-reset') || $('#NavbarNav').hasClass('navber-color-reset') ) {
            setTimeout(function(){
                $('#NavbarItem').removeClass('navber-color-reset');
                $('#NavbarNav').removeClass('navber-color-reset');
           }, navber_transition);
        } else {
            $('#NavbarItem').addClass('navber-color-reset');
            $('#NavbarNav').addClass('navber-color-reset');
        };
    });
};
// スクロール時 Toggler を閉じる
function CloseToggleNav() {
    // remove navber-color-reset
    if ( $('#NavbarItem').hasClass('navber-color-reset') || $('#NavbarNav').hasClass('navber-color-reset') ) {
        setTimeout(function(){
            $('#NavbarItem').removeClass('navber-color-reset');
            $('#NavbarNav').removeClass('navber-color-reset');
       }, navber_transition);
    };
    // remove show
    if ( $('#NavbarNav').hasClass('show') ) {
        setTimeout(function(){
            $('#NavbarNav').removeClass('show');
       }, navber_transition);
       // aria-expanded bool 反転
       let x = $('#TogglerNavigation').attr('aria-expanded');
       setTimeout(function(){
           $('#TogglerNavigation').attr('aria-expanded', !x);
       }, navber_transition);
       // add collapsed
       setTimeout(function(){
           $('#TogglerNavigation').addClass('collapsed');
       }, navber_transition);
    };
};
// ページ内リンクの移動先画面位置を Navber 分下げる
function InPageLinkTransition() {
    $('a[href^="#"]').click(function(){
        let offSet = -ConvertRem2Px(navber_height_rem),
            href   = $(this).attr("href"),
            target = $(href == "#" || href == "" ? 'html' : href),
            position = target.offset().top + offSet;
        $("body,html").animate({
            scrollTop: position,
        }, in_page_anker_transition_speed, 'easeInOutCubic');
        return false;
      });
};

// document ready
$(function() {
    HeroAreaNavSetDefault(),
    NavberColorReset(),
    InPageLinkTransition();
});
// document scroll
$(document).on('scroll', function() {
    NavberHide(),
    CloseToggleNav();
});