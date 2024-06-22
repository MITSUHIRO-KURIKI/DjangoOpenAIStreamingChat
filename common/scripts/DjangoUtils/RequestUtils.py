# Referrer
# https://qiita.com/kin292929/items/92aa0f6f5e1fbca553ee
from django.http import HttpRequest

class RequestUtil:

    request = None

    def __init__(self, request:HttpRequest,):
        self.request = request

    # CSRF COOKIE取得
    def get_csrf_cookie(self, request:HttpRequest=None,) -> str:
        if request:
            return request.META.get('CSRF_COOKIE')
        else:
            return self.request.META.get('CSRF_COOKIE')

    # リクエストURL取得
    def get_request_url(self, request:HttpRequest=None,) -> str:
        print(self)
        if request:
            return request.path
        else:
            return self.request.path
    
    # リクエストホストURL（送信元）取得
    def get_request_host_url(self, request:HttpRequest=None,) -> str:
        if request:
            return request.META.get('HTTP_REFERER')
        else:
            return self.request.META.get('HTTP_REFERER')

    # タイムゾーン取得
    def get_time_zone(self, request:HttpRequest=None,) -> str:
        if request:
            return request.META.get('TZ')
        else:
            return self.request.META.get('TZ')

    # ユーザーエージェント取得
    def get_user_agent(self, request:HttpRequest=None,) -> str:
        if request:
            return request.META.get('HTTP_USER_AGENT')
        else:
            return self.request.META.get('HTTP_USER_AGENT')

    # アクセスIP取得
    def get_ip(self, request:HttpRequest=None,) -> str:
        if request:
            forwarded_addresses = request.META.get('HTTP_X_FORWARDED_FOR')
        else:
            forwarded_addresses = self.request.META.get('HTTP_X_FORWARDED_FOR')
        
        if forwarded_addresses:
            client_addr = forwarded_addresses.split(',')[0]
        else:
            if request:
                client_addr = request.META.get('REMOTE_ADDR')
            else:
                client_addr = self.request.META.get('REMOTE_ADDR')
        return client_addr