from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from encrypted_fields.fields import (
    EncryptedFieldMixin, SearchField, EncryptedCharField,
)

class  EncryptedTextField(EncryptedFieldMixin, models.TextField): 
    pass
class  EncryptedIPAddressField(EncryptedFieldMixin, models.GenericIPAddressField): 
    pass

class AccessBase(models.Model):
    
    _user_agent = EncryptedCharField(
                    _("User Agent"),
                    max_length = 255, 
                    )
    
    user_agent = SearchField(
                    hash_key             = settings.ENCRYPTION_HASH_KEY,
                    encrypted_field_name = "_user_agent",)

    _ip_address = EncryptedIPAddressField(
                    _("IP Address"),
                    null=True,
                    )

    ip_address = SearchField(
                    hash_key             = settings.ENCRYPTION_HASH_KEY,
                    encrypted_field_name = "_ip_address",)

    _username = EncryptedCharField(
                    _("Username"),
                    max_length = 255,
                    null       = True,
                    )
    
    username = SearchField(
                    hash_key             = settings.ENCRYPTION_HASH_KEY,
                    encrypted_field_name = "_username",)

    _http_accept = EncryptedCharField(
                    _("HTTP Accept"),
                    max_length = 1025,)
    
    http_accept = SearchField(
                    hash_key             = settings.ENCRYPTION_HASH_KEY,
                    encrypted_field_name = "_http_accept",)

    _path_info = EncryptedCharField(
                    _("Path"),
                    max_length = 255,)
    
    path_info = SearchField(
                    hash_key             = settings.ENCRYPTION_HASH_KEY,
                    encrypted_field_name = "_path_info",)

    attempt_time = models.DateTimeField(
                    _("Attempt Time"),
                    auto_now_add = True,)

    class Meta:
        app_label = "axes"
        abstract  = True
        ordering  = ["-attempt_time"]


class AccessFailureLog(AccessBase):
    
    locked_out = models.BooleanField(
                    _("Access lock out"),
                    null=False,
                    blank=True,
                    default=False,)

    def __str__(self):
        locked_out_str = " locked out" if self.locked_out else ""
        return f"Failed access: user {self.username}{locked_out_str} on {self.attempt_time} from {self.ip_address}"

    class Meta:
        verbose_name = verbose_name_plural = '03_AccessFailure'


class AccessAttempt(AccessBase):

    _get_data = EncryptedTextField(_("GET Data"))
    get_data = SearchField(
                    hash_key             = settings.ENCRYPTION_HASH_KEY,
                    encrypted_field_name = "_get_data",)
    _post_data = EncryptedTextField(_("POST Data"))
    post_data = SearchField(
                    hash_key             = settings.ENCRYPTION_HASH_KEY,
                    encrypted_field_name = "_get_data",)
    failures_since_start = models.PositiveIntegerField(_("Failed Logins"))

    def __str__(self):
        return f"Attempted Access: {self.attempt_time}"

    class Meta:
        verbose_name = verbose_name_plural = '01_認証失敗/アカウントロックログ(解除の場合には本ログを削除)'
        unique_together = [["username", "ip_address", "user_agent"]]


class AccessLog(AccessBase):
    logout_time = models.DateTimeField(_("Logout Time"), null=True, blank=True)

    def __str__(self):
        return f"Access Log for {self.username} @ {self.attempt_time}"

    class Meta:
        verbose_name = verbose_name_plural = '02_認証成功ログ'