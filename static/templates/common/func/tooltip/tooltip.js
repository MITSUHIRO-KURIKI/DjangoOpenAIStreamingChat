var delay_show = 300,
    delay_hide = 100;

function ToolTipFnc() {
    $('[data-bs-toggle="tooltip"]').tooltip({
        delay:    { "show": delay_show, "hide": delay_hide },
        template: '<div class="tooltip" role="tooltip"><div class="tooltip-inner bg-info"></div></div>'
    });
};

// document ready
$(function() {
    ToolTipFnc();
});