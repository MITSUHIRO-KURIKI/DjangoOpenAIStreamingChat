from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import ActivateToken
from .forms import AdminCustomUserCreationForm

User = get_user_model()

class CustomUserAdmin(UserAdmin):

    # 一覧画面
    list_display_ = ('unique_account_id',
                     'email',
                     'change_email',
                     'is_change_email_request',
                     'is_social_login',
                     'is_set_password',
                     'is_active',
                     'is_staff',
                     'is_superuser',
                     'date_create',)
    list_filter   = ['is_change_email_request',
                     'is_social_login',
                     'is_set_password',
                     'is_active',
                     'is_staff',
                     'is_superuser',
                     'date_create',]
    list_display       = list_display_
    list_display_links = list_display_
    search_fields      = ('unique_account_id',)
    ordering           = ('-date_create',)
    
    # 日付のドリルダウンメニュー
    date_hierarchy = 'date_create'
    
    # 表示件数設定
    list_per_page     = 500
    list_max_show_all = 10000

    # 作成画面
    add_form = AdminCustomUserCreationForm
    add_fieldsets = (
        ('アカウント情報', {'fields': (
            'unique_account_id',
            'email',
            'password',
            'confirm_password',
            )}),
    )

    # 編集画面
    fieldsets = (
        ('ユーザ情報', {'fields': (
            'unique_account_id',
            'email',
            'is_change_email_request',
            )}),
        ('認証情報', {'fields': (
            'password',
            'change_email',
            'is_set_password',
            'is_social_login',
            'is_active',
            )}),
        ('権限情報(管理者権限の設定のため操作注意)', {'fields': (
            'is_staff',
            'is_superuser',
            )}),
        ('その他', {'fields': (
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

class ActivateTokenAdmin(admin.ModelAdmin):

    # 一覧画面
    list_display_ = ('user',
                     'token',
                     'expired_at',)
    list_filter   = ['expired_at',]
    list_display       = list_display_
    list_display_links = list_display_
    search_fields      = ()
    ordering           = ('-expired_at',)
    
    # 日付のドリルダウンメニュー
    date_hierarchy = 'expired_at'
    
    # 表示件数設定
    list_per_page     = 500
    list_max_show_all = 10000
    
    # 作成画面
    add_form      = None
    add_fieldsets = None
    
    # 編集画面
    fieldsets = (
        ('発行済みToken', {'fields': (
            'user',
            'token',
            'expired_at',
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

admin.site.register(User,          CustomUserAdmin)
admin.site.register(ActivateToken, ActivateTokenAdmin)
admin.site.unregister(Group) # AdminSite GROUR unregister