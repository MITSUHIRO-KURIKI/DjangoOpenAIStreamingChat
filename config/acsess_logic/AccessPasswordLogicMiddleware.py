# https://qiita.com/shirakiya/items/1503eaffe81f91af5b9d
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

# どのページにでもアクセスするたびに何か実行する必要がある場合に使用
class AccessPasswordLogicMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_arts, view_kwargs):
        # パスワード設定日時が None (管理者によるリセット実行)
        if request.user.is_authenticated and not request.user.is_social_login and request.user.date_password_change is None:
            request_url = request.path
            siteurl     = request._current_scheme_host

            # 以下のURL(+static,+media)にアクセスする際にはパスワード変更画面にリダイレクトしない▽
            passwordchange_url = reverse('accounts:password_change_one_step')
            logout_url         = reverse('accounts:logout')
            # 以下のURL(+static,+media)にアクセスする際にはパスワード変更画面にリダイレクトしない△
            if siteurl+passwordchange_url == request_url or \
                siteurl+logout_url        == request_url or \
                passwordchange_url        == request_url or \
                logout_url                == request_url or \
                request.path_info.startswith('/static/') or \
                request.path_info.startswith('/media/'):
                return None
            else:
                messages.add_message(request, messages.WARNING,
                                        """パスワードの変更をお願いします""",)
                return HttpResponseRedirect(passwordchange_url)
        else:
            return None