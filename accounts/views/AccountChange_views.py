from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.views import (
    PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    TemplateView, FormView, DeleteView
)
from common.lib.axes.utils import reset
from common.scripts import grecaptcha_request, RequestUtil
from ..forms import (
    OverlapPasswordChangeForm, OverlapSetPasswordForm, OverlapPasswordResetForm,
    EmailChangeForm, UserDeleteForm,
)
from ..models import ActivateToken
from ..views.send_mail.send_mail import send_token_for_change_email


User = get_user_model()


# パスワードの変更
class OverlapPasswordChangeView(PasswordChangeView):
    
    template_name = 'accounts/PasswordChange/password_change.html'
    form_class    = OverlapPasswordChangeForm
    success_url   = reverse_lazy("accounts:password_change_done")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'IS_USE_SIDENAV': True,
        })
        return context

class OverlapPasswordChangeDoneView(PasswordChangeDoneView):
    
    template_name = 'accounts/PasswordChange/password_change_done.html'
    success_url   = reverse_lazy('accounts:password_reset_done')

    # 想定ルート(crrect_ref)から以外のアクセスを遮断
    def get(self, request, *args, **kwargs):
        siteurl    = request._current_scheme_host
        crrect_ref = reverse('accounts:password_change')
        referer    = RequestUtil.get_request_host_url(self)
        if not siteurl+crrect_ref == referer:
            reverse_url = reverse_lazy('home')
            return HttpResponseRedirect(reverse_url)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'IS_USE_SIDENAV': True,
        })
        return context

# パスワードの再設定
# Referrer
# https://stackoverflow.com/questions/56015855/how-to-perform-additional-actions-on-passwordreset-in-django
# https://www.reddit.com/r/django/comments/q1ao3l/here_is_how_you_add_google_recaptcha_to_password/
class OverlapPasswordResetView(PasswordResetView):
    
    form_class               = OverlapPasswordResetForm
    from_email               = settings.DEFAULT_REPLY_EMAIL
    subject_template_name    = 'accounts/PasswordReset/mail_template/subject.html'
    email_template_name      = 'accounts/PasswordReset/mail_template/text_message.html'
    html_email_template_name = 'accounts/PasswordReset/mail_template/html_message.html'
    extra_email_context      = {'TOKEN_EXPIRED' : int(settings.PASSWORD_RESET_TIMEOUT / 60)}
    success_url              = reverse_lazy("accounts:password_reset_done")
    
    if settings.IS_USE_EMAIL_CERTIFICATION:
        template_name = 'accounts/PasswordReset/password_reset.html'
    else:
        # メール認証を使用しない場合にはパスワードリセットは管理者にて行う
        template_name = 'accounts/PasswordReset/password_reset_.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY if settings.IS_USE_RECAPTCHA else None,
            'IS_USE_RECAPTCHA':     settings.IS_USE_RECAPTCHA,
        })
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        # ソーシャルログイン の検証▽
        email = form['email'].value()
        user_or_none = User.objects.filter(email=email).first()
        try:
            is_set_password = user_or_none.is_set_password
        except:
            # user が null の場合にはいないことを伝えないために判定をスルーする(メールは送信されない)
            is_set_password = True
        if not is_set_password:
            messages.add_message(self.request, messages.WARNING,
                                 f'ソーシャルログインの場合には使用したサービスからパスワードをリセットしてください',)
            reverse_url = reverse_lazy('accounts:password_reset')
            return HttpResponseRedirect(reverse_url)
        # ソーシャルログイン の検証△
        # reCaptcha_token の検証▽
        if settings.IS_USE_RECAPTCHA:
            recaptcha_token = self.request.POST.get('g-recaptcha-response')
            if recaptcha_token is None or recaptcha_token == '':
                messages.add_message(self.request, messages.WARNING,
                                     f'不正なPOSTです - reCaptcha ERROR',)
                reverse_url = reverse_lazy('accounts:password_reset')
                return HttpResponseRedirect(reverse_url)
            else:
                res = grecaptcha_request(recaptcha_token)
                if res:  # reCaptcha SUCCESS
                    if form.is_valid():
                        return self.form_valid(form)
                    else:
                        return self.form_invalid(form)
                else:    # reCaptcha FALSE
                    messages.add_message(self.request, messages.WARNING,
                                         f'不正なPOSTです - reCaptcha ERROR',)
                    reverse_url = reverse_lazy('accounts:password_reset')
                    return HttpResponseRedirect(reverse_url)
        else:
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        # reCaptcha_token の検証△

    def get_success_url(self):
        return self.success_url

class OverlapPasswordResetDoneView(PasswordResetDoneView):
    
    template_name = 'accounts/PasswordReset/password_reset_done.html'

    # 想定ルート(crrect_ref)から以外のアクセスを遮断
    def get(self, request, *args, **kwargs):
        siteurl    = request._current_scheme_host
        crrect_ref = reverse('accounts:password_reset')
        referer    = RequestUtil.get_request_host_url(self)
        if not siteurl+crrect_ref == referer:
            reverse_url = reverse_lazy('home')
            return HttpResponseRedirect(reverse_url)
        return super().get(request, *args, **kwargs)

class OverlapPasswordResetConfirmView(PasswordResetConfirmView):
    
    template_name = 'accounts/PasswordReset/password_reset_confilm.html'
    form_class    = OverlapSetPasswordForm
    success_url   = reverse_lazy('accounts:login')

    def form_valid(self, form):
        user = form.save()
        reset(username=user.email) # パスワードリセットで django-axes もリセット
        messages.add_message(self.request, messages.INFO,
                                f'パスワードを変更しました。\n\
                                  新しいパスワードで再度ログインしてください。')
        return super().form_valid(form)

# メールアドレスの変更
class EmailChangeView(LoginRequiredMixin, FormView):

    model         = User
    template_name = 'accounts/EmailChange/email_change.html'
    form_class    = EmailChangeForm

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY if settings.IS_USE_RECAPTCHA else None,
            'IS_USE_RECAPTCHA':     settings.IS_USE_RECAPTCHA,
            'IS_USE_SIDENAV':       True,
        })
        return context

    def post(self, request, *args, **kwargs):
        # reCaptcha_token の検証▽
        if settings.IS_USE_RECAPTCHA:
            recaptcha_token = self.request.POST.get('g-recaptcha-response')
            if recaptcha_token is None or recaptcha_token == '':
                messages.add_message(self.request, messages.WARNING,
                                     f'不正なPOSTです - reCaptcha ERROR',)
                reverse_url = reverse_lazy('accounts:email_change')
                return HttpResponseRedirect(reverse_url)
            else:
                res = grecaptcha_request(recaptcha_token)
                if res:  # reCaptcha SUCCESS
                    pass
                else:    # reCaptcha FALSE
                    messages.add_message(self.request, messages.WARNING,
                                         f'不正なPOSTです - reCaptcha ERROR',)
                    reverse_url = reverse_lazy('accounts:email_change')
                    return HttpResponseRedirect(reverse_url)
        # reCaptcha_token の検証△
        user         = self.request.user
        change_email = self.request.POST['change_email']
        if user.is_set_password:
            if User.objects.filter(email=change_email).exists():
                messages.add_message(self.request, messages.WARNING,
                                     f'既に登録済みのメールアドレスです',)
                reverse_url = reverse_lazy('accounts:email_change')
                return HttpResponseRedirect(reverse_url)
            else: # SUCCESS
                return super().post(request, *args, **kwargs)
        else:
            messages.add_message(self.request, messages.WARNING,
                                 f'ソーシャルIDで作成されたユーザーのメールアドレスをするには、先にパスワードを設定してください。',)
            reverse_url = reverse_lazy('accounts:password_change')
            return HttpResponseRedirect(reverse_url)

    def form_valid(self, form):
        user         = self.request.user
        change_email = self.request.POST['change_email']
        # メール認証を行う場合と行わない場合
        if settings.IS_USE_EMAIL_CERTIFICATION:
            user.is_change_email_request = True
            user.change_email            = change_email
            user.save()
            send_token_for_change_email(user)
        else:
            user.is_change_email_request = False
            user.email                   = change_email     # emailを変更
            user.change_email            = 'dummy@mail.com' # ダミーデータの設定
            user.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        # メール認証する場合としない場合のサインアップ後のページ遷移の分岐
        if settings.IS_USE_EMAIL_CERTIFICATION:
            success_url = reverse_lazy('accounts:email_change_tmp_recept')
        else:
            messages.add_message(self.request, messages.INFO,
                                 f'メールアドレスの変更が完了しました',)
            success_url = reverse_lazy('accounts:email_change')
        return success_url

class EmailChangeTmpReceptView(LoginRequiredMixin, TemplateView):
    
    template_name='accounts/EmailChange/email_change_tmp_recept.html'

    # メールアドレスの変更をしていないユーザからのアクセスを遮断
    def get(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_change_email_request:
            reverse_url = reverse_lazy('home')
            return HttpResponseRedirect(reverse_url)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'IS_USE_SIDENAV': True,
        })
        return context

def ActivateEmailView(request, token):
    res, msg = ActivateToken.objects.activate_change_email_by_token(token)
    if res:
        logout(request)
        messages.add_message(request, messages.INFO, msg)
        reverse_url = reverse_lazy('accounts:login')
    else:
        messages.add_message(request, messages.WARNING, msg)
        reverse_url = reverse_lazy('home')
    return HttpResponseRedirect(reverse_url)

# アカウント削除
class UserDeleteView(LoginRequiredMixin, DeleteView):
    
    model         = User
    template_name = 'accounts/AccountDelete/delete.html'
    form_class    = UserDeleteForm
    success_url   = reverse_lazy('accounts:login')

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'IS_USE_SIDENAV': True,
        })
        return context
    
    def post(self, request, *args, **kwargs):

        check_text = self.request.POST['check_text']

        if check_text == 'delete':
            return super().post(request, *args, **kwargs)
        else:
            messages.add_message(self.request, messages.WARNING,
                                 f'チェックテキストエラー',)
            reverse_url = reverse_lazy('accounts:delete')
            return HttpResponseRedirect(reverse_url)

    def form_valid(self, form):
        self.object.delete()
        messages.add_message(self.request, messages.INFO,
                             f'アカウントを削除しました。\n\
                               ご利用いただきましてありがとうございました。',)
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return self.success_url