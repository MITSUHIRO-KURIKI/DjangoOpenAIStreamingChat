function FormSubmitOnClickDisable() {
    $('form').on('submit', function() {
        $('.on-click-disable').prop('disabled', true);
        $('.on-click-disable').html('\
            <div>\
                <span class="spinner-grow spinner-grow-sm me-1" role="status" aria-hidden="true"></span>\
                <small>prosessing...</small>\
            </div>\
        ');
    });
};

// document ready
$(function() {
    FormSubmitOnClickDisable();
});