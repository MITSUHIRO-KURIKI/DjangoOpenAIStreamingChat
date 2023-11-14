from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from encrypted_fields.fields import (
    EncryptedFieldMixin, SearchField, EncryptedEmailField,
)
from .Inquiry_ChoiceList import SITUATION_CHOICES_LIST

User = get_user_model()
SITUATION_CHOICES_LIST = SITUATION_CHOICES_LIST()


class EncryptedTextField(EncryptedFieldMixin, models.TextField):
    pass

class  EncryptedIPAddressField(EncryptedFieldMixin, models.GenericIPAddressField): 
    pass

class Inquiry(models.Model):

    unique_account_id = models.ForeignKey(
                    User,
                    db_index     = False,
                    primary_key  = False,
                    on_delete    = models.SET_NULL, # [Memo] CASCADE:親削除子削除, SET_DEFAULT/SET_NULL:親削除子保持
                    blank        = True,
                    null         = True,
                    related_name = 'related_inquiry_unique_account_id',
                    help_text    = '紐づくアカウントID',)
    _email = EncryptedEmailField(
                    verbose_name = 'メールアドレス(Encrypted:Form使用不可)',
                    blank        = False,
                    null         = False,
                    max_length   = 255,)
    email = SearchField(
                    verbose_name ='メールアドレス',
                    hash_key     = settings.ENCRYPTION_HASH_KEY,
                    db_index     = False,
                    unique       = False,
                    help_text    = '内容によっては私たちからお問い合わせ内容について連絡させて頂きます',
                    encrypted_field_name = '_email',)
    _inquiry_text = EncryptedTextField(
                    verbose_name = '問い合わせ内容(Encrypted:Form使用不可)',
                    blank        = False,
                    null         = False,
                    max_length   = 2000,)
    inquiry_text = SearchField(
                    verbose_name = '問い合わせ内容',
                    hash_key     = settings.ENCRYPTION_HASH_KEY,
                    db_index     = False,
                    unique       = False,
                    encrypted_field_name = '_inquiry_text',)
    date_create   = models.DateTimeField(
                    verbose_name = '問い合わせ日時',
                    default      = timezone.now,)
    _ip_address = EncryptedIPAddressField(
                    verbose_name = '照会者IPアドレス(Encrypted:Form使用不可)',
                    blank        = True,
                    null         = True,)
    ip_address = SearchField(
                    verbose_name = '照会者IPアドレス',
                    hash_key     = settings.ENCRYPTION_HASH_KEY,
                    db_index     = False,
                    unique       = False,
                    encrypted_field_name = "_ip_address",)
    situation     = models.IntegerField(
                    verbose_name = '対応状況',
                    blank        = False,
                    null         = False,
                    choices      = SITUATION_CHOICES_LIST,
                    default      = 0,)
    date_complete = models.DateTimeField(
                    verbose_name = '対応完了日時',
                    blank        = True,
                    null         = True,
                    default      = None,)
    
    class Meta:
        app_label    = 'inquiry'
        db_table     = 'inquiry_model'
        verbose_name = verbose_name_plural = '問い合わせ一覧'