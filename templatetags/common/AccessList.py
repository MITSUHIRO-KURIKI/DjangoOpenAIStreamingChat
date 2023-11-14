from django import template
from typing import Union, Any, List

register = template.Library()


@register.simple_tag
def access_list(some_list: List[Any],
                index:     int) -> Union[Any, None]:
    try:
        result = some_list[int(index)]
        return result
    except:
        return None