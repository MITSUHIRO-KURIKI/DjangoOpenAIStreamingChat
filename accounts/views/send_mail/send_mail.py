from django.conf import settings
from common.scripts.DjangoUtils import generate_uuid_hex
from datetime import datetime, timedelta
from ...models.ActivateToken_models import ActivateToken

def send_token_for_change_email(instance) -> None:
    # メールアドレス変更時のメールアドレスの認証
    if instance.is_change_email_request and settings.IS_USE_EMAIL_CERTIFICATION:
        activate_token = ActivateToken.objects.create(
            user       = instance,
            token      = generate_uuid_hex(),
            expired_at = datetime.now() + timedelta(seconds=settings.EMAIL_CERTIFICATION_TOKEN_AGE),
        )
        subject_template_name    = 'accounts/EmailChange/mail_template/subject.html'
        email_template_name      = 'accounts/EmailChange/mail_template/text_message.html'
        html_email_template_name = 'accounts/EmailChange/mail_template/html_message.html'
        ACTIVATE_URL             = f'{settings.FRONTEND_URL}/accounts/activate_email/{activate_token.token}'
        TOKEN_DELETE_URL         = f'{settings.FRONTEND_URL}/accounts/token_delete/{activate_token.token}'
        context                  = {
            'ACTIVATE_URL':     ACTIVATE_URL,
            'TOKEN_DELETE_URL': TOKEN_DELETE_URL,
            'TOKEN_EXPIRED':    int(settings.EMAIL_CERTIFICATION_TOKEN_AGE / (60)),
        }
        instance.send_mail_user(
            subject_template_name        = subject_template_name,
            email_template_name          = email_template_name,
            html_email_template_name     = html_email_template_name,
            context                      = context,
            is_send_change_email_address = True,
        )