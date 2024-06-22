from django import template
import json
from typing import Optional, Union

register = template.Library()


@register.filter
def json_loads(data:str) -> Optional[Union[dict, list]]:
    try:
        return json.loads(data)
    except:
        try:
            data = data.replace("'", '"')
            return json.loads(data)
        except:
            return None