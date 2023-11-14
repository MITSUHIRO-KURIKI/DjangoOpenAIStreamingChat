function ButtonOnClickDisable() {
    $('.on-click-disable').on('click', function() {
        $(this).prop('disabled', true);
        $(this).html('\
            <div>\
                <span class="spinner-grow spinner-grow-sm me-1" role="status" aria-hidden="true"></span>\
                <small>prosessing...</small>\
            </div>\
        ');
    });
};

// document ready
$(function() {
    ButtonOnClickDisable();
});