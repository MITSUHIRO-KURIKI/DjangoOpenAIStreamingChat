from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()


# 管理画面での新規登録フォーム(メール認証は行わない)
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
        user.is_active = True # メール認証を行わない
        user.save()
        return user

    class Meta:
        model  = User
        fields = ('unique_account_id', 'email', 'password',)