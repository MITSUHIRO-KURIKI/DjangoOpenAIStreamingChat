from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from common.scripts.DjangoUtils import generate_uuid_hex
from datetime import datetime

User = get_user_model()


# サインアップ
class SignUpForm(UserCreationForm):

    def save(self, commit=False):
        
        # フォームからメールアドレスとパスワードを取得
        unique_user_id       = self.cleaned_data.get('unique_user_id')
        email                = self.cleaned_data.get('email')
        password             = self.cleaned_data.get('password1')
        date_password_change = datetime.now()

        # メール認証を行う場合と行わない場合
        if settings.IS_USE_EMAIL_CERTIFICATION:
            is_active = False
        else:
            is_active = True

        # ユーザーの作成
        user = User.objects.create_user(unique_user_id       = unique_user_id,
                                        email                = email,
                                        password             = password,
                                        is_active            = is_active,
                                        date_password_change = date_password_change,)

        return user

    # 同じメールアドレスで仮登録の場合レコードを消去
    def clean_email(self):
        email = self.cleaned_data['email']
        
        if User.objects.filter(email=email,  is_active=False).exists():
            User.objects.filter(email=email, is_active=False).delete()
            
        return email

    class Meta(UserCreationForm.Meta):
        model  = User
        fields = ('email','unique_user_id')