from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import UserProfile, UserReceptionSetting


class UserProfileAdmin(admin.ModelAdmin):

    # ユーザアイコンの表示
    def user_icon_preview(self, obj):
        try:
             return mark_safe(f'<img src="{obj.user_icon.url}" style="width:25px;height:25px;">')
        except: pass
    user_icon_preview.short_description = 'ユーザアイコン'

    # 一覧画面
    list_display_ = ('unique_account_id',
                     'display_name',
                     'user_icon_preview',)
    list_filter   = []
    list_display       = list_display_
    list_display_links = list_display_
    search_fields      = ('display_name',)
    ordering           = ('-unique_account_id',)
    
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
        ('ユーザ情報', {'fields': (
            'unique_account_id',
            'display_name',
            'user_icon',
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

class UserReceptionSettingAdmin(admin.ModelAdmin):

    # 一覧画面
    list_display_ = ('unique_account_id',
                     'is_receive_all',
                     'is_receive_important_only',)
    list_filter   = []
    list_display       = list_display_
    list_display_links = list_display_
    search_fields      = ()
    ordering           = ('-unique_account_id',)
    
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
        ('ユーザ情報', {'fields': (
            'unique_account_id',
            )}),
        ('メール受信設定', {'fields': (
            'is_receive_all',
            'is_receive_important_only',
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

admin.site.register(UserProfile,          UserProfileAdmin)
admin.site.register(UserReceptionSetting, UserReceptionSettingAdmin)