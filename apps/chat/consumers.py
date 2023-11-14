import asyncio
from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from common.scripts import print_color
from django.conf import settings
from django.utils import timezone, dateformat
import json
import openai
from typing import Generator
from .models import Room, Message
from .settings import MaxMessageTokens
from .utils import decompression, calc_token, is_tokens_less_than_settings

openai.api_key = settings.OPENAI_API_KEY


class OpenAIChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        if settings.DEBUG:
            print_color('info: Run OpenAIChatConsumer.connect', 3)
        # group_add▽
        self.room_id         = self.scope['url_route']['kwargs']['room_id']
        # self.room_group_name = f'room_{self.room_id}'
        # await self.channel_layer.group_add(
        #                             self.room_group_name,
        #                             self.channel_name,)
        # group_add△
        await self.accept()

    async def disconnect(self, close_code):
        if settings.DEBUG:
            print_color('info: Run OpenAIChatConsumer.disconnect', 3)
        # group_discard▽
        # await self.channel_layer.group_discard(
        #                             self.room_group_name,
        #                             self.channel_name,)
        # group_discard△
        await self.close()
        # raise StopConsumer()

    async def receive(self, text_data=None, bytes_data=None):
        if settings.DEBUG:
            print_color('info: Run OpenAIChatConsumer.receive', 3)
        # post データ取得▽
        text_data_json = json.loads(text_data)
        data_dict      = decompression(text_data_json)
        # post データ取得△
        if settings.DEBUG:
            print_color(f'data_dict: {data_dict}', 3)
        
        # streamingで文字が出力されるためキャッチする
        llm_response = ''
        
        # 何も質問されてないときに返すテキスト▽
        if data_dict['user_sentence'].replace(' ','').replace('　','') == '':
            message_data = {
                'llm_answer': '私は生成AIです。あなたと会話したり、質問に答えたりできます。',
            }
            await self.send(json.dumps(message_data))
            llm_response += message_data['llm_answer']
        # 何も質問されてないときに返すテキスト△
        # メッセージのトークンが設定値を超えた場合の処理▽
        elif not is_tokens_less_than_settings(
                    sentence   = data_dict['user_sentence']+data_dict['system_sentence']+data_dict['assistant_sentence'],
                    model_name = data_dict['model_name'],
                    max_tokens = MaxMessageTokens):
            message_data = {
                'llm_answer': f'入力されている文字数が設定値を超えたみたいです。\nシステムメッセージやアシスタントメッセージも含めて最大トークンは{MaxMessageTokens}に設定されています。',
            }
            await self.send(json.dumps(message_data))
            llm_response += message_data['llm_answer']
        # メッセージのトークンが設定値を超えた場合の処理△
        else:
            # ルームに紐づくヒストリーメッセージ時の取得
            history_message = await self.get_history(self.scope['url_route']['kwargs']['room_id'], data_dict['history_len'])

            async for llm_answer in self.generater(
                                            data_dict['user_sentence'],
                                            data_dict['system_sentence'],
                                            data_dict['assistant_sentence'],
                                            history_message   = history_message,
                                            model_name        = data_dict['model_name'],
                                            max_tokens        = data_dict['max_tokens'],
                                            temperature       = data_dict['temperature'],
                                            top_p             = data_dict['top_p'],
                                            presence_penalty  = data_dict['presence_penalty'],
                                            frequency_penalty = data_dict['frequency_penalty'],):
                message_data = {
                    'llm_answer': llm_answer,
                }
                await self.send(json.dumps(message_data))
                llm_response += message_data['llm_answer']
        
        # 追加情報(消費トークン数)の取得
        response_info_dict = {
            'sent_tokens':      calc_token(
                                    sentence   = data_dict['user_sentence']+data_dict['system_sentence']+data_dict['assistant_sentence'],
                                    model_name = data_dict['model_name']),
            'generated_tokens': calc_token(
                                    sentence   = llm_response,
                                    model_name = data_dict['model_name']),
        }
        # Model保存▽
        await self.save_message(data_dict, llm_response, response_info_dict)
        # Model保存△

    @database_sync_to_async
    def get_history(self, room_id, history_len):
        # ヒストリーに含める会話数が0の場合にはNoneを返す
        if history_len == 0:
            return None
        else:
            return_history = ''
            message_objects = Message.objects.filter(room_id__room_id=room_id).order_by('-date_create')
            for i, message_object in enumerate(message_objects):
                # ヒストリーに含める会話数の制御
                if i+1 >= history_len:
                    break
                return_history += '\n\n### Human: '
                return_history += message_object.user_message
                return_history += '\n### AI: '
                return_history += message_object.llm_response
                return_history += '\n### TimeStamp: '
                return_history += str(dateformat.format(
                                        timezone.localtime(message_object.date_create),
                                        'Y年m月d日 H時i分s秒'))
            return return_history

    @database_sync_to_async
    def save_message(self, data_dict, llm_response, response_info_dict):
        Message.objects.create(
            room_id       = Room.objects.filter(room_id=self.room_id).first(),
            user_message  = data_dict['user_sentence'],
            user_settings = {k: v for k, v in data_dict.items() if k.lower() != 'user_sentence'},
            llm_response  = llm_response,
            response_info = response_info_dict)

    async def generater(self,
                        user_sentence:str,
                        system_sentence:str     = None,
                        assistant_sentence:str  = None,
                        *,
                        history_message:str     = None,
                        model_name:str          = 'gpt-3.5-turbo',
                        max_tokens:int          = 256,
                        temperature:float       = 1.0,
                        top_p:float             = 1.0,
                        presence_penalty:float  = 1.0,
                        frequency_penalty:float = 1.0,
                        ) -> Generator[str, None, None]:

        # 想定外のパラメータが設定された場合の処理▽
        if not (0.0 <= temperature <= 2.0) or not (0.0 <= top_p <= 1.0) or not (-2.0 <= presence_penalty <= 2.0) or not (-2.0 <= frequency_penalty <= 2.0):
            raise ValueError("llm parameter values error")
        # 想定外のパラメータが設定された場合の処理△
        
        # ヒストリーメッセージ時の処理▽
        if history_message:
            _user_sentence = 'Please answer in Japanese. Answer the following questions as best you can.\n\nYou have refer to the following previous conversation historys:.\n\n## historys'
            _user_sentence += history_message
            _user_sentence += "\n\nLet's start a conversation.\n\n## Human: "
            _user_sentence += user_sentence
            _user_sentence += "\n\n## AI: "
            user_sentence = _user_sentence
        # ヒストリーメッセージ時の処理△

        messages = [
            {
                'role':    'system',
                'content': system_sentence if system_sentence != '' else f'質問には最長でも{int(max_tokens*0.8)}文字程度で回答してください。',
            }, {
                'role':    'user',
                'content': user_sentence,
            }, {
                'role':    'assistant',
                'content': assistant_sentence if assistant_sentence != '' else '',
            },
        ]
        if settings.DEBUG:
            print_color(f'messages: {messages}', 3)
        
        response = openai.ChatCompletion.create(
                            model             = model_name,
                            messages          = messages,
                            max_tokens        = max_tokens,
                            temperature       = temperature,
                            top_p             = top_p,
                            presence_penalty  = presence_penalty,
                            frequency_penalty = frequency_penalty,
                            stream            = True,)
        for res in response:
            try:
                content = res['choices'][0]['delta']['content']
            except:
                content = ''
            yield content
            await asyncio.sleep(0.03)