from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from uuid import uuid4
from .settings import (
    MaxSystemSentence, MaxAssistantSentence,
    MaxHistoryLen, MinTokens, MaxTokens,
)

User = get_user_model()


def get_ai_icon_image_path(instance, filename):
    return f'apps/chat/ai_icon/{instance.room_id.pk}/{filename}'

class Room(models.Model):
    room_id  = models.SlugField(
                    verbose_name   = 'ルームID',
                    db_index       = True,
                    unique         = True,
                    blank          = False,
                    null           = False,
                    default        = uuid4().hex,)
    create_user = models.ForeignKey(
                    User,
                    verbose_name = '作成者',
                    on_delete    = models.CASCADE, # [Memo] CASCADE:親削除子削除, SET_DEFAULT/SET_NULL:親削除子保持
                    blank        = False,
                    null         = False,
                    related_name = 'related_room_model_create_user',
                    help_text    = '紐づくアカウントID',)
    date_create = models.DateTimeField(
                    verbose_name = '作成日時',
                    default      = timezone.now,
                    help_text    = '作成日時',)

    class Meta:
        app_label    = 'chat'
        db_table     = 'room_model'
        verbose_name = verbose_name_plural = 'ルーム一覧'

class RoomSettings(models.Model):

    staticRoot      = settings.STATIC_URL.split('/')[-1] if settings.IS_USE_GCS else '../' + settings.STATIC_URL
    ai_icon_default = staticRoot + '/apps/chat/ai_icon/default/ai.png'

    room_id = models.OneToOneField(
                    Room,
                    verbose_name = 'ルームID',
                    db_index     = True,
                    on_delete    = models.CASCADE, # [Memo] CASCADE:親削除子削除, SET_DEFAULT/SET_NULL:親削除子保持
                    blank        = False,
                    null         = False,
                    related_name = 'related_room_settings_model_room_id',
                    help_text    = '紐づくルームID',)
    room_name = models.CharField(
                    verbose_name = 'ルーム名',
                    default      = 'NewChatRoom',
                    max_length   = 50,
                    blank        = False,
                    null         = False,
                    unique       = False,
                    help_text    = '半角英数字 50文字以下',)
    ai_icon = models.ImageField(
                    verbose_name = 'AIアイコン',
                    upload_to    = get_ai_icon_image_path,
                    blank        = False,
                    null         = False,
                    default      = ai_icon_default,
                    help_text    = f'画像は {settings.USER_ICON_RESIZE_HEIGHT}(px)x{settings.USER_ICON_RESIZE_WIDTH}(px) にリサイズされます',)
    system_sentence = models.TextField(
                    verbose_name = 'システムメッセージ',
                    max_length   = MaxSystemSentence,
                    blank        = True,
                    null         = True,
                    default      = '',
                    help_text    = f'最大{MaxSystemSentence}文字')
    assistant_sentence = models.TextField(
                    verbose_name = 'アシスタントメッセージ',
                    max_length   = MaxAssistantSentence,
                    blank        = True,
                    null         = True,
                    default      = '',
                    help_text    = f'最大{MaxAssistantSentence}文字')
    history_len = models.IntegerField(
                    verbose_name = 'history_len',
                    blank        = False,
                    null         = False,
                    default      = 0,
                    validators   = [MinValueValidator(0), MaxValueValidator(MaxHistoryLen)],
                    help_text    = f'ヒストリーに含める直近の会話数(最大{MaxHistoryLen})',)
    max_tokens = models.IntegerField(
                    verbose_name = 'max_tokens',
                    blank        = False,
                    null         = False,
                    default      = 256,
                    validators   = [MinValueValidator(MinTokens), MaxValueValidator(MaxTokens)],
                    help_text    = f'生成されるトークンの最大長(最大{MaxTokens})',)
    temperature = models.FloatField(
                    verbose_name = 'temperature',
                    blank        = False,
                    null         = False,
                    default      = 1.0,
                    validators   = [MinValueValidator(0), MaxValueValidator(2)],
                    help_text    = '生成するテキストのランダム性(between 0 and 2)',)
    top_p = models.FloatField(
                    verbose_name = 'top_p',
                    blank        = False,
                    null         = False,
                    default      = 1.0,
                    validators   = [MinValueValidator(0), MaxValueValidator(1)],
                    help_text    = '単語の選択性(between 0 and 1)',)
    presence_penalty = models.FloatField(
                    verbose_name = 'presence_penalty',
                    blank        = False,
                    null         = False,
                    default      = 1.0,
                    validators   = [MinValueValidator(-2), MaxValueValidator(2)],
                    help_text    = '既出単語への一定ペナルティ(between -2 and 2)',)
    frequency_penalty = models.FloatField(
                    verbose_name = 'frequency_penalty',
                    blank        = False,
                    null         = False,
                    default      = 1.0,
                    validators   = [MinValueValidator(-2), MaxValueValidator(2)],
                    help_text    = '既出単語の出現回数へのペナルティ(between -2 and 2)',)
    comment = models.TextField(
                    verbose_name = 'コメント/メモ',
                    blank        = True,
                    null         = True,
                    max_length   = 256,
                    default      = '',
                    help_text    = '半角英数字 256文字以下',)

    class Meta:
        app_label    = 'chat'
        db_table     = 'room_settings_model'
        verbose_name = verbose_name_plural = 'ルーム設定'

# Room 作成と同時に RoomSettings を作成
@receiver(post_save, sender=Room)
def create_related_model_for_custom_user_model(sender, instance, created, **kwargs):
    # Room モデルの新規作成時のみ実行
    if created:
        # レコードが存在しない場合作成 / 存在する場合はレコードを返す
        _ = RoomSettings.objects.get_or_create(room_id = instance)

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
    user_message = models.TextField(
                    verbose_name = 'ユーザメッセージ',
                    blank        = True,
                    null         = True,)
    user_settings = models.TextField(
                    verbose_name = 'ユーザのLLM設定',
                    blank        = True,
                    null         = True,)
    llm_response = models.TextField(
                    verbose_name = 'LLM回答',
                    blank        = True,
                    null         = True,)
    response_info = models.TextField(
                    verbose_name = '追加情報',
                    blank        = True,
                    null         = True,)
    date_create = models.DateTimeField(
                    verbose_name = '作成日時',
                    default      = timezone.now,
                    help_text    = '作成日時',)

    class Meta:
        app_label    = 'chat'
        db_table     = 'message_model'
        verbose_name = verbose_name_plural = 'メッセージ一覧'