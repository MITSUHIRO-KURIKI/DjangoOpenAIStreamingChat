from typing import Dict, Union

def decompression(json_data) -> Dict[str, Union[str, int, float]]:
    return_dict = dict()
    try:    return_dict['user_sentence'] = json_data['user_sentence']
    except: return_dict['user_sentence'] = ''
    
    try:    return_dict['system_sentence'] = json_data['system_sentence']
    except: return_dict['system_sentence'] = ''
    
    try:    return_dict['assistant_sentence'] = json_data['assistant_sentence']
    except: return_dict['assistant_sentence'] = ''
    
    try:    return_dict['history_len'] = json_data['history_len']
    except: return_dict['history_len'] = 0
    
    try:    return_dict['model_name'] = json_data['model_name']
    except: return_dict['model_name'] = 'gpt-3.5-turbo'
    
    try:    return_dict['max_tokens'] = json_data['max_tokens']
    except: return_dict['max_tokens'] = 256
    
    try:    return_dict['temperature'] = json_data['temperature']
    except: return_dict['temperature'] = 1.0
    
    try:    return_dict['top_p'] = json_data['top_p']
    except: return_dict['top_p'] = 1.0
    
    try:    return_dict['presence_penalty'] = json_data['presence_penalty']
    except: return_dict['presence_penalty'] = 1.0
    
    try:    return_dict['frequency_penalty'] = json_data['frequency_penalty']
    except: return_dict['frequency_penalty'] = 1.0
    
    return return_dict