function CheckAllControl() {
    $('#check-all-control-btn').on('click', function () {
        if ($('.check-all-control').prop('checked')) {
            // チェックを外す
            $('.check-all-control').prop('checked', false);
            // もしチェックが外れていたら
        } else {
            // チェックを入れる
            $('.check-all-control').prop('checked', true);
        };
    });
};

// document ready
$(function() {
    CheckAllControl();
});