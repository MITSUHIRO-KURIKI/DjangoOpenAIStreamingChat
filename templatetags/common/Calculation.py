from django import template
from typing import Union
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN

register = template.Library()


@register.simple_tag
def calculation_Add(val1:Union[int, float],
                    val2:Union[int, float],
                    ) -> Union[int, float, None]:
    try:
        result = val1 + val2
        return result
    except:
        return None

@register.simple_tag
def calculation_Multiplication(val1:Union[int, float],
                               val2:Union[int, float],
                               ) -> Union[int, float, None]:
    try:
        result = val1 * val2
        return result
    except:
        return None

@register.simple_tag
def calculation_Division(val1:Union[int, float],
                         val2:Union[int, float],
                         decimals:str = '0',
                         rounding:str = 'ROUND_HALF_UP',
                         ) -> Union[int, float, None]:
    """
    ## Args: 
    ### decimals
      * '0'    => 求めたい桁数が整数\n
      * '0.1'  => 求めたい桁数が小数第一位\n
      * '0.01' => 求めたい桁数が小数第二位
    ### rounding
      * ROUND_HALF_UP(default) => 四捨五入\n
      * ROUND_HALF_EVEN        => 偶数への丸め
    """
    if rounding == 'ROUND_HALF_UP':
        rounding = ROUND_HALF_UP
    else:
        rounding = ROUND_HALF_EVEN
    try:
        result = val1 / val2
        result = Decimal(str(result)).quantize(Decimal(decimals), rounding=rounding)
        if decimals == '0':
            return int(result)
        else:
            return float(result)
    except:
        return None