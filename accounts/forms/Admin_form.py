from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from common.lib.axes.utils import reset
from common.scripts.DjangoUtils import generate_uuid_hex

User = get_user_model()


# 管理画面での新規登録フォーム(メール認証は行わない)
# パスワード設定日時は None 設定
class AdminCustomUserCreationForm(forms.ModelForm):

    password         = forms.CharField(
                            label  = 'パスワード',
                            widget = forms.PasswordInput(),)
    confirm_password = forms.CharField(
                            label  = 'パスワード(確認用)',
                            widget = forms.PasswordInput(),)

    def clean(self):
        cleaned_data = super().clean()
        
        password         = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise ValidationError('パスワードが一致しません')
    
    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data.get('password'))
        user.unique_account_id = generate_uuid_hex()
        user.is_active         = True # メール認証を行わない
        # 管理画面からの場合には初回ログインでパスワードを要求
        user.date_password_change = None
        user.save()
        return user

    class Meta:
        model  = User
        fields = ('email', 'password',)

# 管理画面でのパスワード変更フォーム
# パスワード設定日時はNone
class OverlapAdminPasswordChangeForm(AdminPasswordChangeForm):
    
    def save(self, commit=True):
        """Save the new password."""
        password = self.cleaned_data["password1"]
        self.user.set_password(password)
        if commit:
            # 管理画面からの場合には初回ログインでパスワードを要求
            self.user.date_password_change = None
            self.user.save()
            
            # パスワードリセットで django-axes もリセット
            reset(username=self.user.email)
        
        return self.user