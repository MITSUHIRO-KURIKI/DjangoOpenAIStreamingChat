# Referrer
# https://qiita.com/kin292929/items/92aa0f6f5e1fbca553ee
from django.db import models
from django.conf import settings
from django.utils import timezone
from common.scripts.DjangoUtils import RequestUtil
from datetime import datetime, timedelta
from encrypted_fields.fields import (
    SearchField, EncryptedFieldMixin, EncryptedCharField,
)

class  EncryptedTextField(EncryptedFieldMixin, models.TextField): 
    pass
class  EncryptedIPAddressField(EncryptedFieldMixin, models.GenericIPAddressField): 
    pass

class AccessSecurityManager(models.Manager):
    
    @staticmethod
    def insert_access_log(request, type:str):
        request_util = RequestUtil(request)
        ip           = request_util.get_ip()
        # 同じIPからのログは30分に1回ログ記録
        logs = AccessSecurity.objects.filter(
                                        ip               = ip,
                                        type             = type,
                                        date_create__gte = datetime.now()-timedelta(minutes=30),).first()
        if not logs:
            AccessSecurity.objects.create(
                        ip               = request_util.get_ip(),
                        type             = type,
                        request_host_url = request_util.get_request_host_url(),
                        # request_url      = request_util.get_request_url(),
                        # user_agent       = request_util.get_user_agent(),
                        # csrf_token       = request_util.get_csrf_cookie(),
                        # time_zone        = request_util.get_time_zone(),
            )


class AccessSecurity(models.Model):

    _ip = EncryptedIPAddressField(
                    verbose_name = 'ip',
                    blank        = True,
                    null         = True,)
    ip = SearchField(
                    hash_key             = settings.ENCRYPTION_HASH_KEY,
                    encrypted_field_name = "_ip",)
    type = models.CharField(
                    verbose_name = 'type',
                    blank        = True,
                    null         = True,
                    max_length   = 256,)
    request_host_url = EncryptedTextField(
                    verbose_name = 'request_host_url',
                    blank        = True,
                    null         = True,)
    request_url = EncryptedTextField(
                    verbose_name = 'request_url',
                    blank        = True,
                    null         = True,)
    user_agent = EncryptedTextField(
                    verbose_name = 'user_agent',
                    blank        = True,
                    null         = True,)
    csrf_token = EncryptedTextField(
                    verbose_name = 'csrf_token',
                    blank        = True,
                    null         = True,)
    time_zone = EncryptedCharField(
                    verbose_name = 'time_zone',
                    blank        = True,
                    null         = True,
                    max_length   = 256,)
    date_create = models.DateTimeField(
                    verbose_name = '記録日時',
                    blank        = True,
                    null         = True,
                    default      = timezone.now,)
    
    objects = AccessSecurityManager()
    
    class Meta:
        app_label    = 'access_security'
        db_table     = 'access_security_model'
        verbose_name = verbose_name_plural = '02_ブロックログ'