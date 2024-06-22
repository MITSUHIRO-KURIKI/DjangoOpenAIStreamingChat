from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    SetPasswordForm, PasswordChangeForm, PasswordResetForm, _unicode_ci_compare,
)
from django.utils.translation import gettext as _
from datetime import datetime

User = get_user_model()


# パスワードの変更
# パスワード設定日時を記録する
class OverlapPasswordChangeForm(PasswordChangeForm):

    def clean_new_password2(self):

        old_password  = self.cleaned_data.get('old_password')
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')

        # 新しいパスワードは前回とは異なるものに制限する
        if old_password and new_password2:
            if self.user.check_password(old_password) and new_password1 == old_password:
                raise ValidationError(_('新しいパスワードは現在のパスワードと異なる必要があります'),
                                    code='password_no_change')
        return super().clean_new_password2()

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.date_password_change    = datetime.now() # 変更日時を記録
            self.user.is_change_email_request = False          # メールアドレス変更の要求をリセット
            self.user.save()
        return self.user

# ソーシャルログインユーザかつパスワード未設定の場合には、元のパスワードの入力を求めない
class OverlapSocialloginUserPasswordChangeForm(SetPasswordForm):

    field_order = ['new_password1', 'new_password2']

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.date_password_change    = datetime.now() # 変更日時を記録
            self.user.is_change_email_request = False          # メールアドレス変更の要求をリセット
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

# パスワードのリセット後の再設定
class OverlapSetPasswordForm(SetPasswordForm):

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.date_password_change    = datetime.now() # 変更日時を記録
            self.user.change_email_on_request = False          # メールアドレス変更の要求をリセット
            self.user.save()
        return self.user

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