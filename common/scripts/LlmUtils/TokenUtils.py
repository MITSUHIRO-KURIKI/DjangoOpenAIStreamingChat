import tiktoken
from typing import Dict

def decompression(json_data) -> Dict[str, str]:
    try:
        user_sentence = json_data['user_sentence']
    except KeyError:
        user_sentence = ''
    try:
        rag_type = json_data['rag_type']
    except KeyError:
        rag_type = 1
    return {
            'user_sentence': user_sentence,
            'rag_type': rag_type,
        }

def calc_token(sentence:str   = '',
               model_name:str = None,
               ) -> int:
    if model_name:
        encoding      = tiktoken.encoding_for_model(model_name)
        encoding_name = encoding.name
    else:
        encoding_name = 'cl100k_base'
    num_tokens = len(tiktoken.get_encoding(encoding_name).encode(sentence))
    return num_tokens

def is_tokens_less_than_settings(sentence:str   = '',
                                 model_name:str = None,
                                 max_tokens:int = 0,) -> bool:
    if max_tokens == 0:
        return True
    else:
        if calc_token(sentence, model_name) > max_tokens:
            return False
        else:
            return True