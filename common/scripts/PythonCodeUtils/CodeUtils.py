from typing import Dict, Any, Optional

def inverse_dict_lookup(d:Dict[Any, Any], x:Any) -> Optional[Any]:
    for k,v in d.items():
        if x == v:
            return k
    return None

def calc_score_deviation_value(x:float, mean:float, std:float) -> Optional[float]:
    if std == 0:
        return None
    deviation_value = ((x - mean) / std) * 10 + 50
    return deviation_value

def insert_br_multi_lines_optimized(input_string:str,
                                    br_str:str = '<br>',
                                    n:int      = 9,
                                    ) -> str:
    """
    Optimized version to insert '<br>' into the input string every n characters, 
    ensuring that '<br>' is not inserted immediately before or after a '・'.
    This is repeated for the entire string.

    :param input_string: The string where '<br>' will be inserted.
    :param n: Number of characters after which '<br>' will be inserted, if no '・' is found.
    :return: The modified string with '<br>' inserted as described.
    """
    parts = []
    while input_string:
        split_index = n

        # Adjust split_index to avoid breaking at '・'
        if '・' in input_string[:n+1]:
            dot_index = input_string.find('・', 0, n+1)
            # Check if dot is at the splitting point or one character before it
            if dot_index in [n-1, n]:
                split_index = dot_index  # Split at the dot index

        # Ensure the split index does not exceed the string length
        split_index = min(split_index, len(input_string))

        # Append the substring to the list
        parts.append(input_string[:split_index])
        # Update the input_string to process the remaining part
        input_string = input_string[split_index:]

    # Join all parts with '<br>'
    return br_str.join(parts)