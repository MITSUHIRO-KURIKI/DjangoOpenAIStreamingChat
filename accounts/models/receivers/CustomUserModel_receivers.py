from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.user_properties.models import (
    UserProfile, UserReceptionSetting,
)
from common.scripts.DjangoUtils import generate_uuid_hex
from datetime import datetime, timedelta
from ...models.ActivateToken_models import ActivateToken

User = get_user_model()


# CustomUser 作成と同時に UserProfile と UserReceptionSetting を作成
@receiver(post_save, sender=User)
def create_related_model_for_custom_user_model(sender, instance, created, **kwargs):
    # User モデルの新規作成時のみ実行
    if created:
        # レコードが存在しない場合作成 / 存在する場合はレコードを返す(通常発生しない)
        _ = UserProfile.objects.get_or_create(unique_account_id = instance)
        _ = UserReceptionSetting.objects.get_or_create(unique_account_id = instance)

# ログイン時の処理
## 前々回のログイン日時を記録する
@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    user.before_last_login = user.last_login
    user.save()

# 認証のメール送信機能
@receiver(post_save, sender=User)
def send_token_for_activate_user(sender, instance, **kwargs):
    # サインアップ時のメールアドレスの認証
    # User モデルの新規作成時のみ実行
    if kwargs['created']:
        if instance.is_active is False and settings.IS_USE_EMAIL_CERTIFICATION:
            activate_token = ActivateToken.objects.create(
                user       = instance,
                token      = generate_uuid_hex(),
                expired_at = datetime.now()+timedelta(seconds=settings.EMAIL_CERTIFICATION_TOKEN_AGE),
            )
            subject_template_name    = 'accounts/SignUp/mail_template/subject.html'
            email_template_name      = 'accounts/SignUp/mail_template/text_message.html'
            html_email_template_name = 'accounts/SignUp/mail_template/html_message.html'
            ACTIVATE_URL             = f'{settings.FRONTEND_URL}/accounts/activate_user/{activate_token.token}'
            TOKEN_DELETE_URL         = f'{settings.FRONTEND_URL}/accounts/token_delete/{activate_token.token}'
            context                  = {
                'ACTIVATE_URL':     ACTIVATE_URL,
                'TOKEN_DELETE_URL': TOKEN_DELETE_URL,
                'TOKEN_EXPIRED':    int(settings.EMAIL_CERTIFICATION_TOKEN_AGE / (60)),
            }
            instance.send_mail_user(
                subject_template_name    = subject_template_name,
                email_template_name      = email_template_name,
                html_email_template_name = html_email_template_name,
                context                  = context,
            )