import re
from urllib.parse import urlparse

def is_allowed_url(url:str, allowed_domains_list:list) -> bool:
    """URLが許可されたドメインリストに含まれているかどうかを判定する。"""
    parsed_url = urlparse(url)
    domain     = parsed_url.netloc
    # ドメインをピリオドで分割し、最後の2要素（または必要に応じてより多くの要素）を取得する
    domain_parts = domain.split('.')
    for allowed_domain in allowed_domains_list:
        allowed_parts = allowed_domain.split('.')
        # 許可されたドメインがURLのドメインで終わっていることを確認
        if domain_parts[-len(allowed_parts):] == allowed_parts:
            return True
    return False

def remove_disallowed_urls(text:str, allowed_domains_list:list) -> str:
    """テキストから許可されていないドメインのURLを削除する。"""
    url_pattern = re.compile(r'https?://[^\s]+')
    def filter_url(m):
        url = m.group(0).replace('http://', 'https://')  # HTTPをHTTPSに変換
        return url if is_allowed_url(url, allowed_domains_list) else ''
    return url_pattern.sub(filter_url, text)

def links_harmless(text:str, allowed_domains_list:list) -> str:
    """Markdown形式のリンクから許可されていないドメインのURLを削除する。"""
    md_link_pattern = re.compile(r'\[([^\]]+)\]\((https?://[^\s\)]+)\)')
    def replace_link(m):
        text, url = m.groups()
        url = url.replace('http://', 'https://')  # HTTPをHTTPSに変換
        if is_allowed_url(url, allowed_domains_list):
            return f'[{text}]({url})'             # HTTPSに変換後、リンクを保持
        else:
            return text  # 許可されていないURLはリンクを解除
    return md_link_pattern.sub(replace_link, text)

def text_url_hermless(text:str, allowed_domains_list:list) -> str:
    """テキスト内のURLを処理し、許可されたドメインのURLのみを保持する。"""
    # 直接URLとMarkdownリンクを処理
    text = remove_disallowed_urls(text, allowed_domains_list)
    text = links_harmless(text, allowed_domains_list)
    # 引用符で囲まれたURLを処理する
    quoted_url_pattern = re.compile(r'「(https?://[^\s]+?)」')
    def filter_quoted_url(m):
        url = m.group(1).replace('http://', 'https://')
        if is_allowed_url(url, allowed_domains_list):
            return f'「{url}」'  # 許可されたURLをそのまま保持
        else:
            return ''            # 許可されていないURLを完全に削除
    
    text = quoted_url_pattern.sub(filter_quoted_url, text)
    return text

def text_modify_fnc(text:str,
                    allowed_domains_list:list = ['go.jp', 'or.jp', 'google.com',],
                    ) -> str:
    text = text_url_hermless(text, allowed_domains_list)
    return text