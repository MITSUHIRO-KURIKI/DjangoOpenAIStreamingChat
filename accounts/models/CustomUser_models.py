from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin,
)
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils import timezone
from encrypted_fields.fields import (
    SearchField, EncryptedEmailField,
)
from typing import Dict, List, Union, Any
from uuid import uuid4


# 拡張ユーザモデル
class CustomUserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields): 
        if not email:
            raise ValueError('メールアドレスの入力は必須です')
        
        email = self.normalize_email(email)
        user  = self.model(email=email, **extra_fields) 
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        
        # 管理者権限が付与されないよう念のためdefault値を再設定
        extra_fields.setdefault('is_staff',     False) 
        extra_fields.setdefault('is_superuser', False)

        # social_login: password == None を判定条件としてフラグを付与
        ## social_login フラグを立てる
        ## email を変更する際、password を先に設定させるようにフラグを付与 is_set_password
        if password is None:
            extra_fields.setdefault('unique_account_id', uuid4().hex) # unique_account_id を自動付与
            extra_fields.setdefault('is_social_login',   True)
            extra_fields.setdefault('is_set_password',   False)
            extra_fields.setdefault('is_active',         True)        # メール認証を行わない

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        
        # 管理者権限の付与
        extra_fields.setdefault('is_active',    True) # メール認証を行わない
        extra_fields.setdefault('is_staff',     True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True: 
            raise ValueError('Superuser must have is_staff=True.') 
        if extra_fields.get('is_superuser') is not True: 
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self._create_user(email, password, **extra_fields) 

class CustomUser(AbstractBaseUser, PermissionsMixin):

    unique_account_id  = models.SlugField(
                    verbose_name   = 'アカウント名(日本語不可)',
                    db_index       = True,
                    unique         = True,
                    blank          = False,
                    null           = False,
                    default        = uuid4().hex,
                    error_messages = {'unique': 'このアカウント名は既に利用されています',},
                    help_text      = 'アルファベット、数字、アンダーバー、ハイフン 32文字以下',)
    _email = EncryptedEmailField(
                    verbose_name = 'メールアドレス(Encrypted:Form使用不可)',
                    blank        = False,
                    null         = False,
                    max_length   = 255,)
    email  = SearchField(
                    verbose_name   = 'メールアドレス',
                    hash_key       = settings.ENCRYPTION_HASH_KEY,
                    db_index       = True,
                    unique         = True,
                    error_messages = {'unique': 'このメールアドレスは既に使用されています',},
                    help_text      = 'メールアドレス(ユニーク、255文字以下)',
                    encrypted_field_name = '_email',)
    change_email = EncryptedEmailField(
                    verbose_name = '変更したいメールアドレス(Encrypted:Form使用不可)',
                    blank        = False,
                    null         = False,
                    unique       = False,
                    max_length   = 255,
                    default      = 'dummy@mail.com',)
    is_change_email_request = models.BooleanField(
                    verbose_name = 'メール再設定のリクエスト中',
                    default      = False,)
    is_social_login = models.BooleanField(
                    verbose_name = 'ソーシャルログイン',
                    default      = False,)
    is_set_password = models.BooleanField(
                    verbose_name = 'パスワード設定状況',
                    default      = True,)
    is_active = models.BooleanField(
                    verbose_name = 'アカウントが有効',
                    default      = True,
                    help_text    = '無効の場合にはログイン不可になります',)
    is_staff = models.BooleanField(
                    verbose_name = 'ITスタッフ',
                    default      = False,
                    help_text    = 'ITスタッフ権限(通常はチェックをつけない)',)
    is_superuser = models.BooleanField(
                    verbose_name = 'IT管理者',
                    default      = False,
                    help_text    = 'IT管理者権限(通常はチェックをつけない)',)
    date_create = models.DateTimeField(
                    verbose_name = '作成日時',
                    default      = timezone.now,
                    help_text    = '作成日時',)
    last_login = None

    USERNAME_FIELD  = 'email'               # UNIQUE CustomUser
    REQUIRED_FIELDS = ['unique_account_id'] # MUST Create Superuser

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def send_mail_user(
            self,
            subject_template_name:str,
            email_template_name:str,
            from_email:Union[str, None]               = None,
            reply_email:Union[str, None]              = None,
            bcc_email:Union[List[str], None]          = None,
            html_email_template_name:Union[str, None] = None,
            context:Union[Dict[str, Any], None]       = None,
            is_send_change_email_address:bool         = False,
            fail_silently:bool                        = False,
        ) -> None:
        
        from_email  = from_email if from_email else settings.DEFAULT_FROM_EMAIL
        reply_email = reply_email if reply_email else settings.DEFAULT_REPLY_EMAIL
        to_email    = self.change_email if is_send_change_email_address else self.email
        
        subject = loader.render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())
        body    = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(
                            subject    = subject,
                            body       = body,
                            from_email = from_email,
                            to         = [to_email],
                            bcc        = bcc_email,
                            reply_to   = [reply_email],)
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')
        email_message.send(fail_silently=fail_silently)

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_absolute_url(self):
        return self

    class Meta(AbstractBaseUser.Meta):
        app_label    = 'accounts'
        db_table     = 'custom_user_model'
        verbose_name = verbose_name_plural = '01_ユーザ情報'