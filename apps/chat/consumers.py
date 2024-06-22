from django.conf import settings
import asyncio
from common.scripts.DjangoUtils import generate_uuid_hex
from common.scripts.LlmUtils import Llm, calc_token, is_tokens_less_than_settings
from common.scripts.PythonCodeUtils import print_color
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
# from google.auth import default as google_default_credentials
import json
import openai
from typing import List, AsyncGenerator
from .models import Room, Message
from .models.ModelNameChoice import MODEL_NAME_CHOICES
from .settings import SEND_MAX_TOKENS, RETRY_LIMIT_N
from .Utils import (
    NextQuestionAssistantPrompt, decompression,
    get_room_settings, get_history, is_create_user_room,
    save_data, save_room_name,
)

openai.api_key          = settings.OPENAI_API_KEY
MODEL_NAME_CHOICES_DICT = dict(MODEL_NAME_CHOICES())


class OpenAIChatConsumer(AsyncWebsocketConsumer):
    
    model = Message

    async def connect(self):
        
        self.connect_user    = self.scope['user']
        self.room_id         = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'room_%s' % self.room_id
        
        # ユーザ認証▽
        if self.connect_user.is_anonymous or not self.connect_user or not await is_create_user_room(self.connect_user, self.room_id):
            if settings.DEBUG:
                print_color('info: ERROR: is_anonymous OpenAIChatConsumer.disconnect', 3)
            await self.channel_layer.group_discard(self.room_group_name,
                                                   self.channel_name,)
            await self.close()
            raise StopConsumer()
        elif settings.DEBUG:
            print_color('info: RUN OpenAIChatConsumer.connect', 3)
        # ユーザ認証△
        
        await self.channel_layer.group_add(self.room_group_name,
                                           self.channel_name,)
        await self.accept()

    async def disconnect(self, close_code):
        if settings.DEBUG:
            print_color('info: Run OpenAIChatConsumer.disconnect', 3)
        await self.channel_layer.group_discard(self.room_group_name,
                                               self.channel_name,)
        await self.close()
        raise StopConsumer()

    async def receive(self, text_data=None, bytes_data=None):
        if settings.DEBUG:
            print_color('info: Run OpenAIChatConsumer.receive', 3)
        
        # post データ取得▽
        text_data_json = json.loads(text_data)
        data_dict      = decompression(text_data_json)
        # post データ取得△
        
        # RoomSettings の取得
        room_settings_dict = await get_room_settings(Room.objects, self.room_id)
        data_dict          = data_dict | room_settings_dict
        
        # model_name の変換
        data_dict['model_name'] = MODEL_NAME_CHOICES_DICT[data_dict['model_name']]
        
        if settings.DEBUG:
            print_color(f'data_dict: {data_dict}', 4)

        # ルームに紐づくヒストリーメッセージ時の取得▽
        history_list, history_text = await get_history(self.model.objects, self.scope['url_route']['kwargs']['room_id'], data_dict['history_len'])
        
        data_dict['history_list'] = history_list
        data_dict['history_text'] = history_text
        # ルームに紐づくヒストリーメッセージ時の取得△
        
        # 入力のバリデーション▽
        ## 何も質問されてないときに返すテキスト▽
        if data_dict['user_sentence'].replace(' ','').replace('　','') == '':
            error_message = '私は生成AIです。あなたと会話したり、質問に答えたりできます。'
            async for llm_answer in self.context_stremer(error_message):
                message_data = {
                    'type':       'llm_answer',
                    'llm_answer': llm_answer,
                }
                await self.send(json.dumps(message_data))
            # 処理の終了をsend
            message_data = {
                'type': 'is_streaming_complete',
            }
            await self.send(json.dumps(message_data))
        ## 何も質問されてないときに返すテキスト△
        
        ## メッセージのトークンが設定値を超えた場合の処理▽
        elif not is_tokens_less_than_settings(
                    sentence   = data_dict['user_sentence']+data_dict['system_sentence']+data_dict['assistant_sentence']+data_dict['history_text'],
                    max_tokens = int(SEND_MAX_TOKENS)):
            error_message = f'入力文字数が設定値を超えたみたいです。\n過去の会話、システムメッセージなども含めて最大トークンは{SEND_MAX_TOKENS}に設定されています。'
            async for llm_answer in self.context_stremer(error_message):
                message_data = {
                    'type':       'llm_answer',
                    'llm_answer': llm_answer,
                }
                await self.send(json.dumps(message_data))
            # 処理の終了をsend
            message_data = {
                'type': 'is_streaming_complete',
            }
            await self.send(json.dumps(message_data))
        ## メッセージのトークンが設定値を超えた場合の処理△
        # 入力のバリデーション△
        
        # メイン処理
        else:
            # streamingで文字が出力されるためキャッチする器▽
            llm_response                                = ''
            data_dict['next_question_assist_data_list'] = None
            # streamingで文字が出力されるためキャッチする器△

            ##################################################
            # 1.LLM 回答の取得とストリーム
            async for llm_answer in self.chat_generater(
                                            data_dict['user_sentence'],
                                            data_dict['system_sentence'],
                                            data_dict['assistant_sentence'],
                                            history_list      = data_dict['history_list'],
                                            model_name        = data_dict['model_name'],
                                            max_tokens        = data_dict['max_tokens'],
                                            temperature       = data_dict['temperature'],
                                            top_p             = data_dict['top_p'],
                                            frequency_penalty = data_dict['frequency_penalty'],
                                            presence_penalty  = data_dict['presence_penalty'],):
                message_data = {
                    'type':       'llm_answer',
                    'llm_answer': llm_answer,
                }
                await self.send(json.dumps(message_data))
                llm_response += message_data['llm_answer']
            ## タスク終了をsend
            message_id   = generate_uuid_hex()
            message_data = {
                'type':       'llm_answer_complete',
                'message_id': message_id,
            }
            await self.send(json.dumps(message_data))
            data_dict['llm_response'] = llm_response

            ##################################################
            # 2.次の質問の候補の取得とストリーム
            async for next_question_list in self.generate_next_question_assist(data_dict, RETRY_LIMIT_N):
                message_data = {
                    'type':                'next_question_assist',
                    'next_question_assist': next_question_list,
                }
                await self.send(json.dumps(message_data))
            data_dict['next_question_assist_data_list'] = next_question_list
            ## タスク終了をsend
            message_data = {
                'type': 'next_question_assist_complete',
            }
            await self.send(json.dumps(message_data))

            ##################################################
            # 3.追加情報(消費トークン数)の取得
            tokens_info_dict = {
                'sent_tokens':      calc_token(
                                        sentence = data_dict['user_sentence']+data_dict['system_sentence']+data_dict['assistant_sentence']+history_text,
                                        ),
                'generated_tokens': calc_token(sentence = llm_response,),
            }
            data_dict['tokens_info_dict'] = tokens_info_dict
            
            ##################################################
            # 4.Modelに結果を保存
            await save_data(self.model.objects, Room.objects, self.room_id, message_id, data_dict)
            await save_room_name(Room.objects, self.room_id, data_dict['user_sentence'])
            ## タスク終了をsend
            message_data = {
                'type': 'save_model_complete',
            }
            await self.send(json.dumps(message_data))
            
            # 処理終了をsend
            message_data = {
                'type': 'is_streaming_complete',
            }
            await self.send(json.dumps(message_data))

    # 回答の生成を行う非同期関数
    async def chat_generater(self,
                             user_sentence:str,
                             system_sentence:str     = None,
                             assistant_sentence:str  = None,
                             *,
                             history_list:list       = None,
                             model_name:str          = 'gpt-3.5-turbo',
                             max_tokens:int          = 256,
                             temperature:float       = 1.0,
                             top_p:float             = 1.0,
                             frequency_penalty:float = 1.0,
                             presence_penalty:float  = 1.0,
                             timeout:int             = 30,
                             asyncio_sleep:float     = 0.03,
                             ) -> AsyncGenerator[str, None]:

        # 想定外のパラメータが設定された場合の処理▽
        if not (0.0 <= temperature <= 2.0) or not (0.0 <= top_p <= 1.0) or not (-2.0 <= presence_penalty <= 2.0) or not (-2.0 <= frequency_penalty <= 2.0):
            raise ValueError("llm parameter values error")
        # 想定外のパラメータが設定された場合の処理△
        
        # gpt-4o 用(ハードコーディングのため適宜関数にいれる前の処理としてもいいかも)
        if model_name.startswith("gpt-4o"):
            asyncio_sleep = 0.01
        
        # プロンプトの生成
        ## ## system_sentence の追加
        messages = [
            {
                'role':    'system',
                'content': system_sentence if system_sentence and system_sentence.replace(' ','').replace('　','') != '' else 'You are an AI assistant that helps people find information.',
            }
        ]
        ## ヒストリーの追加
        if history_list:
            for hist in history_list:
                messages.append(hist)
        ## user_sentence の追加
        messages.append(
            {
                'role':    'user',
                'content': user_sentence,
            }
        )
        ## assistant_sentence の追加
        if assistant_sentence and assistant_sentence.replace(' ','').replace('　','') != '':
            messages.append(
                {
                    'role':    'assistant',
                    'content': assistant_sentence,
                }
            )
        
        # 非同期処理の場合にはclientをUtilでなく定義が必要▽
        if settings.IS_USE_AZURE_OPENAI:
            client = openai.AzureOpenAI(
                                azure_endpoint = settings.AZURE_OPENAI_ENDPOINT,
                                api_key        = settings.OPENAI_API_KEY,
                                api_version    = settings.AZURE_OPENAI_API_VERSION,
                                http_client    = None,) # IF USE ProxyServer httpx.Client(proxies=settings.HTTP_PROXY)))
        else:
            client = openai.OpenAI(api_key     = settings.OPENAI_API_KEY,
                                   http_client = None,) # IF USE ProxyServer httpx.Client(proxies=settings.HTTP_PROXY)))
        # 非同期処理の場合にはclientをUtilでなく定義が必要△
        
        response = client.chat.completions.create(
                            model       = model_name,
                            messages    = messages,
                            temperature = temperature,
                            max_tokens  = max_tokens,
                            stream      = True,
                            timeout     = timeout,)
        for res in response:
            try:
                content = res.choices[0].delta.content
                if content == None:
                    content = ''
            except:
                content = ''
            yield content
            await asyncio.sleep(asyncio_sleep)

    # 次の質問アシストの生成と送信を行う非同期関数
    async def generate_next_question_assist(self,
                                            data_dict:dict,
                                            RETRY_LIMIT_N:int   = 3,
                                            ) -> AsyncGenerator[List[str], None]:
        
        llm = Llm(temperature       = 1.0,
                  model_name        = data_dict['model_name'],
                  api_key           = settings.OPENAI_API_KEY,
                  azure_endpoint    = settings.AZURE_OPENAI_ENDPOINT if settings.IS_USE_AZURE_OPENAI else None,
                  azure_api_version = settings.AZURE_OPENAI_API_VERSION if settings.IS_USE_AZURE_OPENAI else None,)

        next_question_list = []
        c = 0
        while c < RETRY_LIMIT_N:
            try:
                next_question_jsonStr = llm.get_response(
                    NextQuestionAssistantPrompt(data_dict['user_sentence'],
                                                data_dict['llm_response'],
                                                data_dict['history_text'])
                )
                if settings.DEBUG:
                    print_color('*'*30, 4)
                    print_color(f'next_question_jsonStr({c}):\n{next_question_jsonStr}', 4)
                    print_color('*'*30, 4)
                next_question_json = json.loads(next_question_jsonStr.replace('```python','')\
                                                                     .replace('```json','')\
                                                                     .replace('```', ''))
                next_question_list = next_question_json['NextHumanQuestionsList']
                c = RETRY_LIMIT_N
            except:
                c += 1

        yield next_question_list

    # 文字列のストリームを行う非同期関数
    async def context_stremer(self,
                              context:str         = '',
                              asyncio_sleep:float = 0.02,
                              ) -> AsyncGenerator[str, None]:
        if context:
            for char in context:
                yield char
                await asyncio.sleep(asyncio_sleep)