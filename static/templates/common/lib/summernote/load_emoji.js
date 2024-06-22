$(document).ready(function () {
    $.ajax({
        url: 'https://api.github.com/emojis'
    }).then(function (data) {
        window.emojis    = Object.keys(data);
        window.emojiUrls = data;
    });
});