from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from ..forms import LogInForm


# ログイン
class OverlapLoginView(LoginView):
    
    authentication_form = LogInForm
    template_name       = 'accounts/LogIn/login.html'
    success_url         = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'IS_USE_SOCIAL_LOGIN': settings.IS_USE_SOCIAL_LOGIN,
        })
        return context

    def form_valid(self, form):
        # ログイン状態の保持機能
        login_remember = form.cleaned_data['is_login_remember']
        if login_remember:
            self.request.session.set_expiry(settings.SESSION_COOKIE_SET_EXPIRY_AGE)
        else:
            # SESSION_EXPIRE_AT_BROWSER_CLOSE が設定されている場合には0秒セット
            if settings.SESSION_EXPIRE_AT_BROWSER_CLOSE:
                self.request.session.set_expiry(0)
            else:
                self.request.session.set_expiry(settings.SESSION_COOKIE_AGE)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

# ログアウト
class OverlapLogoutView(LogoutView):
    
    success_url = reverse_lazy('accounts:login')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.add_message(self.request, messages.INFO,
                             f'ログアウトしました',)
        return response

    def get_success_url(self):
        return self.success_url