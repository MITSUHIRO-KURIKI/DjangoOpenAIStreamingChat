from django.conf import settings
from django.contrib.auth import login
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView
from common.scripts import grecaptcha_request, RequestUtil
from ..models import ActivateToken
from ..forms import SignUpForm

# サインアップ
class SignUpView(CreateView):
    
    form_class = SignUpForm
    template_name = 'accounts/SignUp/signup.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY if settings.IS_USE_RECAPTCHA else None,
            'IS_USE_RECAPTCHA':     settings.IS_USE_RECAPTCHA,
            'IS_USE_SOCIAL_LOGIN':  settings.IS_USE_SOCIAL_LOGIN,
        })
        return context

    def post(self, request, *args, **kwargs):
        # reCaptcha_token の検証▽
        if settings.IS_USE_RECAPTCHA:
            recaptcha_token = self.request.POST.get('g-recaptcha-response')
            if recaptcha_token is None or recaptcha_token == '':
                messages.add_message(self.request, messages.WARNING,
                                     f'不正なPOSTです - reCaptcha ERROR',)
                # reCaptcha ERROR の場合に入力された内容を返す
                request.session['invalid_unique_account_id'] = self.request.POST['unique_account_id']
                request.session['invalid_email']             = self.request.POST['email']
                return redirect('accounts:signup')
            else:
                res = grecaptcha_request(recaptcha_token)
                if res:  # reCaptcha SUCCESS
                    return super().post(request, *args, **kwargs)
                else:    # reCaptcha FALSE
                    messages.add_message(self.request, messages.WARNING,
                                         f'不正なPOSTです - reCaptcha ERROR',)
                    # reCaptcha ERROR の場合に入力された内容を返す
                    request.session['invalid_unique_account_id'] = self.request.POST['unique_account_id']
                    request.session['invalid_email']             = self.request.POST['email']
                    return redirect('accounts:signup')
        # reCaptcha_token の検証△
        else:
            return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        # self.object に save() されたユーザーオブジェクトが格納される
        valid = super().form_valid(form)
        # ADD social-auth-app-django Required 'backend='
        login(self.request, self.object, backend='django.contrib.auth.backends.ModelBackend')
        return valid

    def form_invalid(self, form):
        context = self.get_context_data()
        # invalid の場合に入力された内容を返す
        context.update({
            'invalid_unique_account_id': self.request.POST['unique_account_id'],
            'invalid_email':             self.request.POST['email'],
        })
        return self.render_to_response(context)

    def get_success_url(self):
        # メール認証する場合としない場合のサインアップ後のページ遷移の分岐
        if settings.IS_USE_EMAIL_CERTIFICATION:
            success_url = reverse_lazy('accounts:signup_tmp_recept')
        else:
            messages.add_message(self.request, messages.INFO,
                                 f'登録が完了しました',)
            success_url = reverse_lazy('home')
        return success_url

class SignUpTmpReceptView(TemplateView):
    
    template_name='accounts/SignUp/signup_tmp_recept.html'
    
    # 想定ルート(crrect_ref)から以外のアクセスを遮断
    def get(self, request, *args, **kwargs):
        siteurl    = request._current_scheme_host
        crrect_ref = reverse('accounts:signup')
        referer    = RequestUtil.get_request_host_url(self)
        if not siteurl+crrect_ref == referer:
            reverse_url = reverse_lazy('home')
            return HttpResponseRedirect(reverse_url)
        return super().get(request, *args, **kwargs)

def ActivateUserView(request, token):
    res, msg = ActivateToken.objects.activate_user_by_token(token)
    if res:
        messages.add_message(request, messages.INFO, msg)
        return redirect('home')
    else:
        messages.add_message(request, messages.WARNING, msg)
        return redirect('accounts:signup')