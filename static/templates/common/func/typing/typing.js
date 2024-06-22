$(window).on('load', function () {
    const elements = $(".typing");
    elements.each(function () {
        const text = $(this).html();
        let textbox = "";
        text.split('').forEach(function (target) {
            textbox += target !== " " ? '<span>' + target + '</span>' : target;
        });
        $(this).html(textbox);
    });

    function typeAnimation(index) {
        if (index >= elements.length) return;

        const element = $(elements[index]);
        const children = element.children();
        const baseTime = 80; // 基本となるタイム

        element.addClass('active');

        children.each(function (i) {
            // ランダムな変動を加える（例: 基本時間の 50% 〜 150% の間）
            let timeVariation = baseTime * (0.5 + Math.random());
            let delay = timeVariation * i;
            $(this).delay(delay).fadeIn(timeVariation);
        });

        children.last().promise().done(function () {
            if (index < elements.length - 1) {
                element.removeClass('active');
            }
            typeAnimation(index + 1);
        });
    }

    typeAnimation(0);
});

$(window).on('load', function () {
    const elements = $(".typing-NoRandom");
    elements.each(function () {
        const text = $(this).html();
        let textbox = "";
        text.split('').forEach(function (target) {
            textbox += target !== " " ? '<span>' + target + '</span>' : target;
        });
        $(this).html(textbox);
    });

    function typeAnimationNoRandom(index) {
        if (index >= elements.length) return;

        const element = $(elements[index]);
        const children = element.children();
        const baseTime = 50; // 基本となるタイム

        element.addClass('active');

        children.each(function (i) {
            let timeVariation = baseTime;
            let delay = timeVariation * i;
            $(this).delay(delay).fadeIn(timeVariation);
        });

        children.last().promise().done(function () {
            if (index < elements.length - 1) {
                element.removeClass('active');
            }
            typeAnimationNoRandom(index + 1);
        });
    }

    typeAnimationNoRandom(0);
});