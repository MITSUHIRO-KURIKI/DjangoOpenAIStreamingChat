from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from common.scripts.DjangoUtils import generate_uuid_hex
from .ModelNameChoice import MODEL_NAME_CHOICES
from ..settings import (
    MIN_TOKENS, MAX_TOKENS, MAX_HISSTORY_N,
    MAX_LEN_SYSTEM_SENTENCE, MAX_LEN_ASSISTANT_SENTENCE,
    DEFAULT_ROOM_NAME, MAX_LEN_ROOM_NAME,
)

User = get_user_model()


MODEL_NAME_CHOICES_TUPLE = MODEL_NAME_CHOICES()

def get_ai_icon_image_path(instance, filename):
    return f'apps/chat/ai_icon/{instance.room_id.pk}/{filename}'

class Room(models.Model):
    room_id  = models.SlugField(
                    verbose_name   = 'ルームID',
                    db_index       = True,
                    unique         = True,
                    blank          = False,
                    null           = False,
                    default        = generate_uuid_hex,)
    create_user = models.ForeignKey(
                    User,
                    verbose_name = '作成者',
                    on_delete    = models.CASCADE, # [Memo] CASCADE:親削除子削除, SET_DEFAULT/SET_NULL:親削除子保持
                    blank        = False,
                    null         = False,
                    related_name = 'related_room_model_create_user',
                    help_text    = '紐づくアカウントID',)
    is_active = models.BooleanField(
                    verbose_name = 'ルームが有効',
                    default      = True,
                    help_text    = '無効の場合にはデータは保持されるがユーザには非表示',)
    date_create = models.DateTimeField(
                    verbose_name = '作成日時',
                    default      = timezone.now,
                    help_text    = '作成日時',)

    class Meta:
        app_label    = 'chat'
        db_table     = 'room_model'
        verbose_name = verbose_name_plural = '01_ルーム情報'


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
                    default      = DEFAULT_ROOM_NAME,
                    max_length   = MAX_LEN_ROOM_NAME,
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
    model_name = models.IntegerField(
                    verbose_name = '使用モデル',
                    choices      = MODEL_NAME_CHOICES_TUPLE,
                    default      = 0,
                    blank        = False,
                    null         = False,
                    help_text    = '会話の途中でも変更可能',)
    system_sentence = models.TextField(
                    verbose_name = 'システムメッセージ',
                    max_length   = MAX_LEN_SYSTEM_SENTENCE,
                    blank        = True,
                    null         = True,
                    default      = '',
                    help_text    = f'最大{MAX_LEN_SYSTEM_SENTENCE}文字')
    assistant_sentence = models.TextField(
                    verbose_name = 'アシスタントメッセージ',
                    max_length   = MAX_LEN_ASSISTANT_SENTENCE,
                    blank        = True,
                    null         = True,
                    default      = '',
                    help_text    = f'最大{MAX_LEN_ASSISTANT_SENTENCE}文字')
    history_len = models.IntegerField(
                    verbose_name = 'history_len',
                    blank        = False,
                    null         = False,
                    default      = 1,
                    validators   = [MinValueValidator(0), MaxValueValidator(MAX_HISSTORY_N)],
                    help_text    = f'ヒストリーに含める直近の会話数(最大{MAX_HISSTORY_N})',)
    max_tokens = models.IntegerField(
                    verbose_name = 'max_tokens',
                    blank        = False,
                    null         = False,
                    default      = 256,
                    validators   = [MinValueValidator(MIN_TOKENS), MaxValueValidator(MAX_TOKENS)],
                    help_text    = f'生成されるトークンの最大長(最大{MAX_TOKENS})',)
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
        verbose_name = verbose_name_plural = '02_ルーム設定'

# Room 作成と同時に RoomSettings を作成
@receiver(post_save, sender=Room)
def create_related_model_for_room_model(sender, instance, created, **kwargs):
    # Room モデルの新規作成時のみ実行
    if created:
        # レコードが存在しない場合作成 / 存在する場合はレコードを返す
        _ = RoomSettings.objects.get_or_create(room_id = instance)