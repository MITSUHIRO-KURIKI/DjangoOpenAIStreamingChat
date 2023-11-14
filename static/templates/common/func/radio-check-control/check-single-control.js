function RadioSingleCheck() {
    $('.radio-single-check').on('click', function () {
        if ($(this).prop('checked')) {
            $('.radio-single-check').prop('checked', false);
            $(this).prop('checked', true);
        }
    });
};

// document ready
$(function() {
    RadioSingleCheck();
});