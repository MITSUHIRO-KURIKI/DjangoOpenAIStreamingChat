# https://qiita.com/shirakiya/items/1503eaffe81f91af5b9d
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

# どのページにでもアクセスするたびに何か実行する必要がある場合に使用
class AccessUseridLogicMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_arts, view_kwargs):
        # ユーザIDが設定されずにログインした場合に設定を要求する
        if request.user.is_authenticated and (request.user.unique_user_id is None or request.user.unique_user_id == ''):
            request_url = request.path
            siteurl     = request._current_scheme_host

            # 以下のURL(+static,+media)にアクセスする際にはユーザID設定画面にリダイレクトしない▽
            unique_user_id_change_url = reverse('accounts:uset_ser_id')
            logout_url                = reverse('accounts:logout')
            # 以下のURL(+static,+media)にアクセスする際にはユーザID設定画面にリダイレクトしない△
            if siteurl+unique_user_id_change_url == request_url or \
                siteurl+logout_url               == request_url or \
                unique_user_id_change_url        == request_url or \
                logout_url                       == request_url or \
                request.path_info.startswith('/static/') or \
                request.path_info.startswith('/media/'):
                return None
            else:
                messages.add_message(request, messages.WARNING,
                                        """ユーザ名の設定をお願いします""",)
                return HttpResponseRedirect(unique_user_id_change_url)
        else:
            return None