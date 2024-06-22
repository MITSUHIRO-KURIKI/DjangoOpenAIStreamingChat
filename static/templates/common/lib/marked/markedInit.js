// グローバル変数として宣言
const markedRenderer = new marked.Renderer();

function escapeHtml(codeHtml) {
    return codeHtml
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
markedRenderer.code  = function (code, language) {
    let escapedCode = code.trim()
    if (language === 'html') {
        escapedCode = escapeHtml(code);
    };
    if (language === 'mermaid') {
        return `<pre class="mermaid">${escapedCode}</pre>`;
    } else {
        return `<pre><code class="language-${language || 'none'}" data-language="${language || 'none'}">${escapedCode}</code></pre>`;
    }
};
// table
markedRenderer.table = function(header, body) {
    return `<table class="table table-bordered table-hover"><thead>${header}</thead><tbody>${body}</tbody></table>`;
};
markedRenderer.tablerow = function(content) {
    return `<tr>${content}</tr>`;
};
markedRenderer.tablecell = function(content, flags) {
    const tag   = flags.header ? 'th' : 'td';
    const align = flags.align ? `text-${flags.align}` : '';
    return `<${tag} class="${align}">${content}</${tag}>`;
};
// ul, ol
markedRenderer.list = function(body, ordered, start) {
    const type = ordered ? 'ol' : 'ul';
    const startAttr = ordered && start !== 1 ? (` start="${start}"`) : '';
    return `<${type}${startAttr} class="">${body}</${type}>`;
};
// li
markedRenderer.listitem = function(text, task, checked) {
    const taskClass = task ? ' list-group-item-action' : '';
    return `<li class="list-style-on ${taskClass}">${text}</li>`;
};
// p
markedRenderer.paragraph = function(text) {
    return `<p class="mb-2">${text}</p>`;
};
// 強調表示 (strong)
markedRenderer.strong = function(text) {
    return `<strong class="font-weight-bold">${text}</strong>`;
};
// h1, h2, ...
markedRenderer.heading = function(text, level) {
    return `<h${level} class="mt-3">${text}</h${level}>`;
};
// anker
markedRenderer.link = function(href, title, text) {
    let pattern     = /https?:\/\/[\w\/:%#\$&\?\(\)~\.=\+\-]+/gim;
    let patternHref = href.match(pattern);
    return `<a href="${patternHref}" title="${title}" class="text-primary" target="_blank" rel="noopener noreferrer">${text}</a>`;
};