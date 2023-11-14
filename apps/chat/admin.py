from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Room, RoomSettings, Message

class RoomAdmin(admin.ModelAdmin):

    # 一覧画面
    list_display_ = ('room_id',
                     'create_user',
                     'date_create',)
    list_filter   = []
    list_display       = list_display_
    list_display_links = list_display_
    search_fields      = ('room_id', 'unique_account_id',)
    ordering           = ('-date_create',)
    
    # 日付のドリルダウンメニュー
    date_hierarchy = 'date_create'
    
    # 表示件数設定
    list_per_page     = 500
    list_max_show_all = 10000
    
    # 作成画面
    add_form      = None
    add_fieldsets = None
    
    # 編集画面
    fieldsets = (
        ('ルーム情報', {'fields': (
            'room_id',
            'create_user',
            'date_create',
            )}),
    )

    # 権限設定
    # CRUD を True で is_superuser に制限(is_stuff の権限剥奪)
    is_only_superuser_Create = True
    is_only_superuser_Read   = True
    is_only_superuser_Update = True
    is_only_superuser_Delete = True
    
    if is_only_superuser_Create:
        def has_add_permission(self, request) -> bool:
            return request.user.is_superuser
    else:
        def has_add_permission(self, request) -> bool:
            return request.user.is_superuser or request.user.is_staff
    if is_only_superuser_Read:
        def has_module_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser
        def has_view_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser
    else:
        def has_module_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser or request.user.is_staff
        def has_view_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser or request.user.is_staff
    if is_only_superuser_Update:
        def has_change_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser
    else:
        def has_change_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser or request.user.is_staff
    if is_only_superuser_Delete:
        def has_delete_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser
    else:
        def has_delete_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser or request.user.is_staff

class RoomSettingsAdmin(admin.ModelAdmin):

    # AIアイコンの表示
    def ai_icon_preview(self, obj):
        try:
             return mark_safe(f'<img src="{obj.ai_icon.url}" style="width:25px;height:25px;">')
        except: pass
    ai_icon_preview.short_description = 'AIアイコン'
    # 表示する文字数の制限▽
    def character_limit_system_sentence(self, obj):
        limit=20
        character = obj.system_sentence
        if len(character)>limit:
            character=character[:limit]+'...'
        return character
    def character_limit_assistant_sentence(self, obj):
        limit=20
        character = obj.assistant_sentence
        if len(character)>limit:
            character=character[:limit]+'...'
        return character
    def character_limit_comment(self, obj):
        limit=20
        character = obj.assistant_sentence
        if len(character)>limit:
            character=character[:limit]+'...'
        return character
    # 表示する文字数の制限△

    # 一覧画面
    list_display_ = ('room_id',
                     'room_name',
                     'ai_icon_preview',
                     'character_limit_system_sentence',
                     'character_limit_assistant_sentence',
                     'history_len',
                     'max_tokens',
                     'temperature',
                     'top_p',
                     'presence_penalty',
                     'frequency_penalty',
                     'character_limit_comment',)
    list_filter   = []
    list_display       = list_display_
    list_display_links = list_display_
    search_fields      = ('room_id',
                          'room_name',
                          'system_sentence',
                          'assistant_sentence',
                          'comment')
    ordering           = ('-pk',)
    
    # 日付のドリルダウンメニュー
    date_hierarchy = None
    
    # 表示件数設定
    list_per_page     = 500
    list_max_show_all = 10000
    
    # 作成画面
    add_form      = None
    add_fieldsets = None
    
    # 編集画面
    fieldsets = (
        ('ルーム情報', {'fields': (
            'room_id',
            'room_name',
            'ai_icon',
            )}),
        ('プロンプト', {'fields': (
            'system_sentence',
            'assistant_sentence',
            'history_len',
            )}),
        ('ハイパラメータ', {'fields': (
            'max_tokens',
            'temperature',
            'top_p',
            'presence_penalty',
            'frequency_penalty',
            )}),
        ('その他', {'fields': (
            'comment',
            )}),
    )

    # 権限設定
    # CRUD を True で is_superuser に制限(is_stuff の権限剥奪)
    is_only_superuser_Create = True
    is_only_superuser_Read   = True
    is_only_superuser_Update = True
    is_only_superuser_Delete = True
    
    if is_only_superuser_Create:
        def has_add_permission(self, request) -> bool:
            return request.user.is_superuser
    else:
        def has_add_permission(self, request) -> bool:
            return request.user.is_superuser or request.user.is_staff
    if is_only_superuser_Read:
        def has_module_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser
        def has_view_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser
    else:
        def has_module_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser or request.user.is_staff
        def has_view_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser or request.user.is_staff
    if is_only_superuser_Update:
        def has_change_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser
    else:
        def has_change_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser or request.user.is_staff
    if is_only_superuser_Delete:
        def has_delete_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser
    else:
        def has_delete_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser or request.user.is_staff

class MessageAdmin(admin.ModelAdmin):

    # 表示する文字数の制限▽
    def character_limit_user_message(self, obj):
        limit=20
        character = obj.user_message
        if len(character)>limit:
            character=character[:limit]+'...'
        return character
    def character_limit_user_settings(self, obj):
        limit=20
        character = obj.user_settings
        if len(character)>limit:
            character=character[:limit]+'...'
        return character
    def character_limit_llm_response(self, obj):
        limit=20
        character = obj.llm_response
        if len(character)>limit:
            character=character[:limit]+'...'
        return character
    # 表示する文字数の制限△

    # 一覧画面
    list_display_ = ('room_id',
                     'character_limit_user_message',
                     'character_limit_user_settings',
                     'character_limit_llm_response',
                     'response_info',
                     'date_create',)
    list_filter   = []
    list_display       = list_display_
    list_display_links = list_display_
    search_fields      = ('room_id', 'user_message', 'llm_response',)
    ordering           = ('-date_create',)
    
    # 日付のドリルダウンメニュー
    date_hierarchy = 'date_create'
    
    # 表示件数設定
    list_per_page     = 500
    list_max_show_all = 10000
    
    # 作成画面
    add_form      = None
    add_fieldsets = None
    
    # 編集画面
    fieldsets = (
        ('ルーム情報', {'fields': (
            'room_id',
            )}),
        ('内容', {'fields': (
            'user_message',
            'llm_response',
            )}),
        ('その他', {'fields': (
            'user_settings',
            'response_info',
            'date_create',
            )}),
    )

    # 権限設定
    # CRUD を True で is_superuser に制限(is_stuff の権限剥奪)
    is_only_superuser_Create = True
    is_only_superuser_Read   = True
    is_only_superuser_Update = True
    is_only_superuser_Delete = True
    
    if is_only_superuser_Create:
        def has_add_permission(self, request) -> bool:
            return request.user.is_superuser
    else:
        def has_add_permission(self, request) -> bool:
            return request.user.is_superuser or request.user.is_staff
    if is_only_superuser_Read:
        def has_module_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser
        def has_view_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser
    else:
        def has_module_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser or request.user.is_staff
        def has_view_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser or request.user.is_staff
    if is_only_superuser_Update:
        def has_change_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser
    else:
        def has_change_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser or request.user.is_staff
    if is_only_superuser_Delete:
        def has_delete_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser
    else:
        def has_delete_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser or request.user.is_staff

admin.site.register(Room,         RoomAdmin)
admin.site.register(RoomSettings, RoomSettingsAdmin)
admin.site.register(Message,      MessageAdmin)