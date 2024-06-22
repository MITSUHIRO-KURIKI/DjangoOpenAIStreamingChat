from django.conf import settings
import openai
from typing import Any, Dict, Optional, Tuple, Union

class Llm:

    def __init__(self,
                 model_name:str = 'gpt-3.5-turbo',
                 api_key:str    = None,
                 *,
                 azure_endpoint:str      = None,
                 azure_api_version:str   = None,
                 temperature:float       = 1.2,
                 max_tokens:int          = 128,
                 top_p:float             = 1.0,
                 frequency_penalty:float = 0.0,
                 presence_penalty:float  = 0.0,):
        # Verify the input is valid.
        if not api_key:
            raise ValueError('Please set api_key.')
        if settings.IS_USE_AZURE_OPENAI:
            if not azure_endpoint:
                raise ValueError('Please set azure_endpoint.')
            if not azure_api_version:
                raise ValueError('Please set azure_api_version.')
        # 想定外のパラメータが設定された場合の処理▽
        if not (0.0 <= temperature <= 2.0) or not (0.0 <= top_p <= 1.0) or not (-2.0 <= presence_penalty <= 2.0) or not (-2.0 <= frequency_penalty <= 2.0):
            raise ValueError("llm parameter values error")
        # 想定外のパラメータが設定された場合の処理△

        if settings.IS_USE_AZURE_OPENAI:
            self.client = openai.AzureOpenAI(
                                    azure_endpoint = azure_endpoint,
                                    api_key        = api_key,
                                    api_version    = azure_api_version,
                                    http_client    = None,) # IF USE ProxyServer: httpx.Client(proxies=settings.HTTP_PROXY)
        else:
            self.client = openai.OpenAI(api_key     = api_key,
                                        http_client = None,) # IF USE ProxyServer: httpx.Client(proxies=settings.HTTP_PROXY)
        
        self.model_name        = model_name
        self.temperature       = temperature
        self.max_tokens        = max_tokens
        self.top_p             = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty  = presence_penalty
        
    def get_response(self,
                     user_sentence:str,
                     system_sentence:str    = None,
                     assistant_sentence:str = None,
                     *,
                     functions:Optional[Dict[str, Any]] = None,
                     function_call:Optional[str]        = None,
                     is_return_useage_dict:bool         = False,
                     timeout:int                        = 60,
                     ) -> Union[None, str, Tuple[str, Dict[str, int]]]:

        if not user_sentence:
            return None

        messages = []
        if system_sentence:
            messages.append({ 'role': 'system', 'content': system_sentence,})
        messages.append({ 'role': 'user', 'content': user_sentence,})

        if not functions:
            response = self.client.chat.completions.create(
                            model       = self.model_name,
                            messages    = messages,
                            temperature = self.temperature,
                            max_tokens  = self.max_tokens,
                            top_p       = self.top_p,
                            stream      = False,
                            timeout     = timeout,)
            return_responce = response.choices[0].message.content
        else:
            response = self.client.chat.completions.create(
                            model         = self.model_name,
                            messages      = messages,
                            temperature   = self.temperature,
                            max_tokens    = self.max_tokens,
                            top_p         = self.top_p,
                            stream        = False,
                            timeout       = timeout,
                            functions     = functions,
                            function_call = function_call,)
            return_responce = response.choices[0].message.function_call.arguments

        if is_return_useage_dict:
            useage_dict = {
                'prompt_tokens':     response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens':      response.usage.total_tokens,
            }
            return return_responce, useage_dict

        return return_responce