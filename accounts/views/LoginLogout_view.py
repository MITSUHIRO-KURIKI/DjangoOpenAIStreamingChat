from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from ..forms import LogInForm


# ログイン
class LogInView(LoginView):
    
    authentication_form = LogInForm
    template_name       = 'accounts/LogIn/login.html'
    success_url         = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'IS_USE_SOCIAL_LOGIN': settings.IS_USE_SOCIAL_LOGIN,
        })
        return context

    def form_valid(self, form):
        # ログイン状態の保持機能
        login_remenber = form.cleaned_data['is_login_remenber']
        if login_remenber:
            self.request.session.set_expiry(60*60*24*5)
        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        # invalid の場合に入力された内容を返す
        context.update({
            'invalid_username': self.request.POST['username'],
        })
        return self.render_to_response(context)

# ログアウト
class LogoutView(LogoutView):
    
    success_url = reverse_lazy('accounts:login')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.add_message(self.request, messages.INFO,
                             f'ログアウトしました',)
        return response

    def get_success_url(self):
        return self.success_url