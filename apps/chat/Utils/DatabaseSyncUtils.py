from channels.db import database_sync_to_async
from typing import Dict
from ..models import Room, RoomSettings

@database_sync_to_async
def get_room_settings(room_id:str,
                      ) -> Dict[str, str]:
    room                       = Room.objects.get(room_id=room_id)
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
def is_create_user_room(user, room_id) -> bool:
    return Room.objects.filter(room_id     = room_id,
                               create_user = user,
                               is_active   = True,).exists()