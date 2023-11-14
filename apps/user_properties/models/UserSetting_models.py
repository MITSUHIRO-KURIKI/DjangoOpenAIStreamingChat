from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class UserReceptionSetting(models.Model):
    
    unique_account_id = models.OneToOneField(
                    User,
                    db_index     = True,
                    primary_key  = True,
                    on_delete    = models.CASCADE, # [Memo] CASCADE:親削除子削除, SET_DEFAULT/SET_NULL:親削除子保持
                    blank        = False,
                    null         = False,
                    related_name = 'related_user_reception_setting_unique_account_id',
                    help_text    = '紐づくアカウントID',)
    is_receive_all = models.BooleanField(
                    verbose_name = '全ての案内を受信する',
                    default      = True,)
    is_receive_important_only = models.BooleanField(
                    verbose_name = '重要な案内のみ受信する',
                    default      = False,)
    
    def get_absolute_url(self):
        return self
    
    class Meta:
        app_label    = 'user_properties'
        db_table     = 'user_reception_setting_model'
        verbose_name = verbose_name_plural = '90_メール受信設定'