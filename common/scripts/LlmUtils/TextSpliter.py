from django.conf import settings
import tiktoken

def split_by_token(text:str,
                   model_name:str = 'gpt-3.5-turbo',
                   max_token:int  = 1024,
                   sep:str        = '。') -> list[str]:
    """
    textをsepで分割して、token数単位でmax_tokenに達するまで連結してテキスト分割を行う。
    """
    encoding = tiktoken.encoding_for_model(model_name)
    
    lines  = text.split(sep)
    blocks = []
    
    token = 0
    block = ''
    for line in lines:
        if len(line) <= 1:
            continue
        t = len(encoding.encode(line))
        if token > 0 and max_token <= (token + t):
            blocks.append(block)
            token = 0
            block = '' 
        token += t
        block += line + sep
    blocks.append(block)
    
    return blocks