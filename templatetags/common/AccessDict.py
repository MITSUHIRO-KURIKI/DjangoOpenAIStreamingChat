from django import template
from typing import Dict, Union, Any

register = template.Library()

 
@register.simple_tag
def access_dict(dict_:Dict[Union[str, int], Any],
                arg:Union[str, int],
                ) -> Union[Any, None]:
    try:
        if arg in dict_:
            return dict_[arg]
        else:
            return None
    except:
        return None