var sidenav_item_width = 12;

// rem → px 変換
function ConvertRem2Px(rem) {
    let fontSize = getComputedStyle(document.documentElement).fontSize;
    return rem * parseFloat(fontSize);
};

// 水平メニューの遷移後に active な項目へ水平スライドする
function SideberPagenateTransition() {
    let target = $("#SideNav a.active"),
        index = $("#SideNav a").index(target),
        scrollValue = ConvertRem2Px(sidenav_item_width) * index;
    $('#SideNavScrollArea').scrollLeft(scrollValue);
};
// スクロールボタンクリック
function SideNavScrollLeftBtnClick() {
    $('#SideNavScrollLeftBtn').on('mousedown', function () {
        let scrollValue = $('#SideNavScrollArea').scrollLeft();
        scrollValue -= ConvertRem2Px(sidenav_item_width) / 3;
        $('#SideNavScrollArea').scrollLeft(scrollValue);
    });
};
function SideNavScrollRightBtnClick() {
    $('#SideNavScrollRightBtn').on('mousedown', function () {
        let scrollValue = $('#SideNavScrollArea').scrollLeft();
        scrollValue += ConvertRem2Px(sidenav_item_width) / 3;
        $('#SideNavScrollArea').scrollLeft(scrollValue);
    });
};

// footer に SideNav の最下部が到達したら隠す
function SideNavHide() {
	let docHeight        = $(document).height(),
        winScrollTop     = $(window).scrollTop(),
        SideNavHeight    = $('#SideNav').height(),
	    footerStartPoint = docHeight - $('footer').height();
	if (winScrollTop + SideNavHeight >= footerStartPoint) {
		$('#SideNav').addClass('hide');
	} else {
		$('#SideNav').removeClass('hide');
	};
};

// document ready
$(function() {
    SideberPagenateTransition(),
    SideNavScrollLeftBtnClick(),
    SideNavScrollRightBtnClick();
});
// document scroll
$(document).on('scroll', function() {
    SideNavHide();
});