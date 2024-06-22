from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from common.scripts.DjangoUtils import generate_uuid_hex
from .Room_models import Room


class Message(models.Model):
    room_id = models.ForeignKey(
                    Room,
                    verbose_name = 'ルームID',
                    db_index     = True,
                    on_delete    = models.CASCADE, # [Memo] CASCADE:親削除子削除, SET_DEFAULT/SET_NULL:親削除子保持
                    blank        = False,
                    null         = False,
                    related_name = 'related_message_model_room_id',
                    help_text    = '紐づくルームID',)
    message_id  = models.SlugField(
                    verbose_name   = 'メッセージID',
                    db_index       = True,
                    unique         = True,
                    blank          = False,
                    null           = False,
                    default        = generate_uuid_hex(),)
    user_message = models.TextField(
                    verbose_name = 'ユーザメッセージ',
                    blank        = True,
                    null         = True,)
    llm_response = models.TextField(
                    verbose_name = 'LLM回答',
                    blank        = True,
                    null         = True,)
    user_settings = models.TextField(
                    verbose_name = 'ユーザのLLM設定',
                    blank        = True,
                    null         = True,)
    tokens_info_dict = models.TextField(
                    verbose_name = 'トークン情報',
                    blank        = True,
                    null         = True,)
    history_list = models.TextField(
                    verbose_name = '参照した過去の会話履歴',
                    blank        = True,
                    null         = True,)
    next_question_assist_data_list = models.TextField(
                    verbose_name = '提示した次の質問候補',
                    blank        = True,
                    null         = True,)
    is_active = models.BooleanField(
                    verbose_name = 'メッセージが有効',
                    default      = True,
                    help_text    = '無効の場合にはデータは保持されるがユーザには非表示',)
    date_create = models.DateTimeField(
                    verbose_name = '作成日時',
                    default      = timezone.now,
                    help_text    = '作成日時',)

    class Meta:
        app_label    = 'chat'
        db_table     = 'message_model'
        verbose_name = verbose_name_plural = '10_メッセージ一覧'


class MessageFeedback(models.Model):
    message_id = models.OneToOneField(
                    Message,
                    verbose_name = 'メッセージID',
                    db_index     = True,
                    on_delete    = models.CASCADE, # [Memo] CASCADE:親削除子削除, SET_DEFAULT/SET_NULL:親削除子保持
                    blank        = False,
                    null         = False,
                    related_name = 'related_message_feedback_model_message_id',
                    help_text    = '紐づくルームID',)
    dissatisfaction = models.BooleanField(
                    verbose_name = '不満フラグ',
                    default      = False,
                    help_text    = '不満ボタンを押した場合にTrue',)
    dissatisfaction_comment = models.TextField(
                    verbose_name = 'コメント',
                    default      = '',
                    max_length   = 3000,
                    blank        = True,
                    null         = True,
                    help_text    = '半角英数字 3000文字以下',)
    date_create = models.DateTimeField(
                    verbose_name = '更新日時',
                    default      = None,
                    blank        = True,
                    null         = True,
                    help_text    = '更新日時',)
    
    class Meta:
        app_label    = 'chat'
        db_table     = 'message_feedback_model'
        verbose_name = verbose_name_plural = '11_メッセージへのフィードバック'

# Room 作成と同時に RoomSettings を作成
@receiver(post_save, sender=Message)
def create_related_model_for_message_model(sender, instance, created, **kwargs):
    # Message モデルの新規作成時のみ実行
    if created:
        # レコードが存在しない場合作成 / 存在する場合はレコードを返す
        _ = MessageFeedback.objects.get_or_create(message_id = instance)