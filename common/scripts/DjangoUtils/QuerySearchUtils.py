from typing import List

def parse_search_params(words:str,) -> List[str]:
    search_words_list = words.replace('　', ' ').split()
    return search_words_list