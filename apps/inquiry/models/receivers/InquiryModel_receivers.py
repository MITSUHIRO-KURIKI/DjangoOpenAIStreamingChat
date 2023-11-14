from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template import loader
from ...models import Inquiry

@receiver(post_save, sender=Inquiry)
def inquirer_notice_admin(sender, instance, **kwargs) -> None:
    if kwargs['created']:
        if settings.IS_NOTIFICATION_ADMIN:
            subject_template_name    = 'apps/inquiry/inquiry_form/notice_admin_mail_template/subject.html'
            email_template_name      = 'apps/inquiry/inquiry_form/notice_admin_mail_template/text_message.html'
            html_email_template_name = 'apps/inquiry/inquiry_form/notice_admin_mail_template/html_message.html'
            context                  = {
                'DATE_CREATE':       instance.date_create,
                'INQUIRY_TEXT':      instance.inquiry_text,
                'UNIQUE_ACCOUNT_ID': instance.unique_account_id.unique_account_id if instance.unique_account_id else None,
                'EMAIL':             instance.email,
                'IP_ADDRESS':        instance.ip_address,
            }
            from_email  = settings.DEFAULT_FROM_EMAIL
            to_email    = settings.ADMIN_NOTICE_EMAIL
    
            subject = loader.render_to_string(subject_template_name, context)
            subject = ''.join(subject.splitlines())
            body    = loader.render_to_string(email_template_name, context)

            email_message = EmailMultiAlternatives(
                                subject    = subject,
                                body       = body,
                                from_email = from_email,
                                to         = [to_email],)
            if html_email_template_name is not None:
                html_email = loader.render_to_string(html_email_template_name, context)
                email_message.attach_alternative(html_email, 'text/html')
            email_message.send(fail_silently=False)