// URLが許可されたドメインリストに含まれているかどうかを判定する関数
function isAllowedUrl(url, allowedDomainsList) {
    const parsedUrl = new URL(url);
    const domain = parsedUrl.hostname;
    const domainParts = domain.split('.');
    return allowedDomainsList.some(allowedDomain => {
        const allowedParts = allowedDomain.split('.');
        return domainParts.slice(-allowedParts.length).join('.') === allowedParts.join('.');
    });
}

// テキストから許可されていないドメインのURLを削除する関数
function removeDisallowedUrls(text, allowedDomainsList) {
    const urlPattern = /https?:\/\/[^\s]+/g;
    return text.replace(urlPattern, (match) => {
        const url = match.replace('http://', 'https://');
        return isAllowedUrl(url, allowedDomainsList) ? url : '';
    });
}

// Markdown形式のリンクから許可されていないドメインのURLを削除する関数
function linksHarmless(text, allowedDomainsList) {
    const mdLinkPattern = /\[([^\]]+)\]\((https?:\/\/[^\s\)]+)\)/g;
    return text.replace(mdLinkPattern, (match, text, url) => {
        const secureUrl = url.replace('http://', 'https://');
        if (isAllowedUrl(secureUrl, allowedDomainsList)) {
            return `[${text}](${secureUrl})`;
        } else {
            return text;
        }
    });
}

// テキスト内のURLを処理し、許可されたドメインのURLのみを保持する関数
function textUrlHarmless(text, allowedDomainsList) {
    text = removeDisallowedUrls(text, allowedDomainsList);
    text = linksHarmless(text, allowedDomainsList);
    const quotedUrlPattern = /「(https?:\/\/[^\s]+?)」/g;
    return text.replace(quotedUrlPattern, (match, url) => {
        const secureUrl = url.replace('http://', 'https://');
        if (isAllowedUrl(secureUrl, allowedDomainsList)) {
            return `「${secureUrl}」`;
        } else {
            return '';
        }
    });
}