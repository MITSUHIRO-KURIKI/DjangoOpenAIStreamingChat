$(function () {
    let theme = document.documentElement.getAttribute('data-bs-theme');
    if (theme === 'dark') {
        theme = 'dark';
    } else {
        theme = 'default';
    };
    mermaid.initialize({ startOnLoad: false, theme: theme,});
    mermaid.run();
});