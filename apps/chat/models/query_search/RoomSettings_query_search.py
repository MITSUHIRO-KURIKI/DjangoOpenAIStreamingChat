from django.db.models import Q
from functools import reduce
from common.scripts.DjangoUtils import parse_search_params

def room_settings_query_search(objs, query:str):
    search_words_list = parse_search_params(query)
    query             = reduce(
                            lambda x,y : x & y,
                            list(map(lambda z: Q(room_name__icontains=z), search_words_list))
                        )
    return objs.filter(query)