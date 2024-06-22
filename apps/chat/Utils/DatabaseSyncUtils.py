from channels.db import database_sync_to_async
from common.scripts.LlmUtils import text_modify_fnc
from typing import Dict, List, Optional, Union
from ..models import Room, RoomSettings
from ..settings import DEFAULT_ROOM_NAME, MAX_LEN_ROOM_NAME

@database_sync_to_async
def get_room_settings(room_model_objects,
                      room_id:str,
                      ) -> Dict[str, str]:
    room                       = room_model_objects.get(room_id=room_id)
    room_settings_model_object = RoomSettings.objects.get(room_id=room)
    
    room_settings_dict = {}
    room_settings_dict['system_sentence']    = room_settings_model_object.system_sentence
    room_settings_dict['assistant_sentence'] = room_settings_model_object.assistant_sentence
    room_settings_dict['history_len']        = room_settings_model_object.history_len
    room_settings_dict['model_name']         = room_settings_model_object.model_name
    room_settings_dict['max_tokens']         = room_settings_model_object.max_tokens
    room_settings_dict['temperature']        = room_settings_model_object.temperature
    room_settings_dict['top_p']              = room_settings_model_object.top_p
    room_settings_dict['presence_penalty']   = room_settings_model_object.presence_penalty
    room_settings_dict['frequency_penalty']  = room_settings_model_object.frequency_penalty
    
    return room_settings_dict

@database_sync_to_async
def get_history(message_model_object,
                room_id:str,
                history_len:int = 3,
                ) -> Optional[List[Dict[str, str]]]:

    if history_len != 0:
        return_history_list = []
        message_objects     = message_model_object.filter(room_id__room_id = room_id,
                                                          is_active        = True,
                                                          ).order_by('-date_create')[:history_len]
        return_history_text = ''
        for message_object in reversed(message_objects):
            # return_history_list
            history_dict_tmp            = {}
            history_dict_tmp['role']    = 'user'
            history_dict_tmp['content'] = message_object.user_message
            return_history_list.append(history_dict_tmp)
            
            history_dict_tmp            = {}
            history_dict_tmp['role']    = 'assistant'
            history_dict_tmp['content'] = message_object.llm_response
            return_history_list.append(history_dict_tmp)
            
            # return_history_text
            return_history_text += f'## HUMAN ({message_object.date_create})\n````\n'
            return_history_text += message_object.user_message
            return_history_text += '\n````\n\n'
            return_history_text += f'## ASSISTANT AI ({message_object.date_create})\n````\n'
            return_history_text += message_object.llm_response
            return_history_text += '\n````\n\n'

        return return_history_list, return_history_text

    # ヒストリーに含める会話数が0の場合
    return None, ''

@database_sync_to_async
def is_create_user_room(user, room_id) -> bool:
    return Room.objects.filter(room_id     = room_id,
                               create_user = user,
                               is_active   = True,).exists()

@database_sync_to_async
def save_data(message_model_objects,
              room_model_objects,
              room_id:str,
              message_id:str,
              data_dict:Dict[str, Union[str,List]],
              ) -> None:
    
    user_settings = {k: v for k, v in data_dict.items()\
                     if (k.lower() != 'user_sentence' and\
                         k.lower() != 'llm_response' and\
                         k.lower() != 'tokens_info_dict' and\
                         k.lower() != 'history_list' and\
                         k.lower() != 'next_question_assist_data_list')}
    
    message_model_objects.create(
        room_id                        = room_model_objects.get(room_id=room_id),
        message_id                     = message_id,
        user_message                   = data_dict['user_sentence'],
        llm_response                   = text_modify_fnc(data_dict['llm_response']),
        user_settings                  = user_settings,
        tokens_info_dict               = data_dict['tokens_info_dict'],
        history_list                   = data_dict['history_list'],
        next_question_assist_data_list = data_dict['next_question_assist_data_list'],)

@database_sync_to_async
def save_room_name(room_model_objects, room_id:str, room_name:str,) -> None:
    room                       = room_model_objects.get(room_id=room_id)
    room_settings_model_object = RoomSettings.objects.get(room_id=room)
    
    # room_name がデフォルトの場合には最初の質問を room_name に設定する
    if room_settings_model_object.room_name == DEFAULT_ROOM_NAME:
        if len(room_name) > MAX_LEN_ROOM_NAME:
            room_name = room_name[:MAX_LEN_ROOM_NAME-4] + '...'
        room_settings_model_object.room_name = room_name
        room_settings_model_object.save()