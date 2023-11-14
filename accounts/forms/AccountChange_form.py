from django.conf import settings
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    SetPasswordForm, PasswordResetForm, _unicode_ci_compare,
)

User = get_user_model()

# パスワードの変更
class OverlapPasswordChangeForm(SetPasswordForm):

    field_order = ['new_password1', 'new_password2']

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.is_change_email_request = False # メールアドレス変更の要求をリセット
            self.user.is_set_password         = True  # ソーシャルIDの場合初期 is_set_password=False のため、ここでパスワードセットを確認
            self.user.save()
        return self.user

# パスワードの再設定
class OverlapSetPasswordForm(SetPasswordForm):

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.change_email_on_request = False # メールアドレス変更の要求をリセット
            self.user.save()
        return self.user

# パスワードのリセット
class OverlapPasswordResetForm(PasswordResetForm):

    def get_users(self, email):
        email_field_name = User.get_email_field_name()
        active_users = User._default_manager.filter(
            **{
                'email':     email,
                'is_active': True,
            }
        )
        return (
            u
            for u in active_users
            if u.has_usable_password()
            and _unicode_ci_compare(email, getattr(u, email_field_name))
        )

# メールアドレスの変更
class EmailChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['change_email',]

# アカウントの削除
class UserDeleteForm(forms.Form):
    check_text = forms.CharField(
                    label     = "確認",
                    required  = True,
                    help_text = '削除するには「delete」と入力してボタンを押してください',)