// ex. class="check-confirm" check-confirm-text="本当に削除しますか？削除後はもとに戻せません"

function CheckConfilm() {
    $('.check-confirm').on('click', function () {
        let text = $(this).data('check-confirm-text');
        if(!confirm(text)) {
            return false;
        } else {
            $('form').prepend(AddPostData);
            $("form").submit();
        }
    });
};

// document ready
$(function() {
    CheckConfilm();
});