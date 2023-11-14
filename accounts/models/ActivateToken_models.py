from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from encrypted_fields.fields import (
    SearchField, EncryptedTextField,
)
from datetime import datetime, timedelta
from uuid import uuid4

User = get_user_model()


# 仮登録/本登録機能
# TOKEN発行用モデル
class ActivateTokenManager(models.Manager):
    
    # サインアップ時のメールアドレスの認証
    def activate_user_by_token(self, token):
        user_activate_token = self.filter(
                                token           = token,
                                expired_at__gte = datetime.now(),
                                ).first()
        # 認証URLの有効期限判定
        if user_activate_token is None:
            # アクセスされた無効な Token を削除
            user_activate_token = self.filter(token=token)
            if user_activate_token:
                user_activate_token.delete()
            res = False
            msg ='仮登録URLの有効期限が切れています 再度サインアップしてください'
            return res, msg
        else:
            user           = user_activate_token.user
            user.is_active = True
            user.save()
            res = True
            msg ='本登録が完了しました'
            # 使用した Token の破棄  
            user_activate_token.delete()
            return res, msg
    
    # メールアドレス変更時のメールアドレスの認証
    def activate_change_email_by_token(self, token):
        user_email_activate_token = self.filter(
                                        token           = token,
                                        expired_at__gte = datetime.now(),
                                    ).first()
        # 認証URLの有効期限判定
        if user_email_activate_token is None:
            # アクセスされた無効な Token を削除
            user_email_activate_token = self.filter(token=token)
            if user_email_activate_token:
                user_email_activate_token.delete()
            res = False
            msg = '仮登録URLの有効期限が切れています'
            return res, msg
        else:
            user = user_email_activate_token.user
            
            if user.is_change_email_request is True:
                user.is_change_email_request = False
                user.save() # 同じアドレスによって弾かれた場合に備えて一旦モデル保存
                user.email        = user.change_email  # email の変更
                user.change_email = 'dummy@mail.com' # 変更後の email を認証したら change_email フィールドをリセット
                user.save()  # SUCCESS
                res = True
                msg = 'メールアドレスの変更が完了しました\n\
                       変更したメールアドレスでログインしてください。'
                # 使用した Token の破棄
                user_email_activate_token.delete()
                return res, msg
            else:
                # アクセスされた無効な Token を削除
                user_email_activate_token.delete()
                res = False
                msg = '再度メールアドレスの変更を行ってください'
                return res, msg

class ActivateToken(models.Model):
    
    user = models.ForeignKey(
                    User,
                    on_delete    = models.CASCADE, # [Memo] CASCADE:親削除->子削除, SET_DEFAULT/SET_NULL:親削除->子保持
                    related_name = 'related_activate_tokens_user',)
    _token = EncryptedTextField(
                    verbose_name = 'Token(Encrypted:Form使用不可)',
                    blank        = False,
                    null         = False,
                    default      = uuid4().hex,)
    token  = SearchField(
                    verbose_name   = 'Token',
                    hash_key       = settings.ENCRYPTION_HASH_KEY,
                    db_index       = True,
                    unique         = True,
                    encrypted_field_name = '_token',)
    expired_at = models.DateTimeField(
                    default = datetime.now()+timedelta(seconds=settings.EMAIL_CERTIFICATION_TOKEN_AGE),)
    
    objects = ActivateTokenManager()

    def __str__(self):
        return self.user.email
    
    class Meta:
        app_label    = 'accounts'
        db_table     = 'activate_token_model'
        verbose_name = verbose_name_plural = '02_認証トークン発行'