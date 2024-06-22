from django.conf import settings
from django.http import HttpResponseForbidden
from common.scripts.DjangoUtils import RequestUtil
from common.scripts.PythonCodeUtils import print_color

class AdminProtect:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        url = request.get_full_path()
        
        # DEBUGがFalseであり、管理サイトに対するアクセス
        if settings.ADMIN_PATH in url and not settings.DEBUG:

            # 送信元のIPアドレス
            ip = RequestUtil.get_ip(self, request)

            # 許可IPアドレスリストが空の場合には全てのIPを許可
            if settings.ALLOWED_IP_ADMIN == ['']:
                response = self.get_response(request)
                return response

            # 送信元IPが許可IPアドレスリストに含まれていない場合はForbiddenを返す
            if ip not in settings.ALLOWED_IP_ADMIN:
                return HttpResponseForbidden()

        ####################
        # ここの if は動作確認用なので本番は消すこと
        if settings.ADMIN_PATH in url and settings.DEBUG:
            ip = RequestUtil.get_ip(self, request)
            print_color('*'*10 + '[this print config.admin_protect.AdminProtect line:34]' + '*'*10, 4)
            print_color(f'* config.admin_protect.AdominProtect DEBUG CODE [admin access]: {ip}'   , 4)
            if ip not in settings.ALLOWED_IP_ADMIN:
                return HttpResponseForbidden()
        ####################

        response = self.get_response(request)
        return response