from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from import_export.admin import ExportMixin
from import_export.resources import ModelResource
from .models import ActivateToken
from .forms import AdminCustomUserCreationForm, OverlapAdminPasswordChangeForm

User = get_user_model()


class UserAdminResource(ModelResource):
    class Meta:
        model  = User
        fields = ('id',
                  'unique_account_id',
                  'unique_user_id',
                  'email',
                  'change_email',
                  'is_change_email_request',
                  'is_social_login',
                  'is_active',
                  'is_staff',
                  'is_superuser',
                  'date_password_change',
                  'before_last_login',
                  'last_login',
                  'date_create',)
        export_order = fields
        clean_model_instances = True

class CustomUserAdmin(ExportMixin, UserAdmin):

    resource_class = UserAdminResource

    # 一覧画面
    list_display_ = ('unique_account_id',
                     'unique_user_id',
                     'email',
                     'change_email',
                     'is_change_email_request',
                     'is_social_login',
                     'is_active',
                     'is_staff',
                     'is_superuser',
                     'date_password_change',
                     'before_last_login',
                     'last_login',
                     'date_create',)
    list_filter   = ['is_change_email_request',
                     'is_social_login',
                     'is_active',
                     'is_staff',
                     'is_superuser',
                     'date_password_change',
                     'before_last_login',
                     'last_login',
                     'date_create',]
    list_display       = list_display_
    list_display_links = list_display_
    search_fields      = ('unique_account_id','unique_user_id',)
    ordering           = ('-date_create',)
    
    # 日付のドリルダウンメニュー
    date_hierarchy = 'date_create'
    
    # 表示件数設定
    list_per_page     = 500
    list_max_show_all = 10000

    # 管理者によるアカウント作成画面
    add_form = AdminCustomUserCreationForm
    add_fieldsets = (
        ('アカウント情報', {'fields': (
            'email',
            'password',
            'confirm_password',
            )}),
    )
    # 管理者によるパスワード変更画面
    change_password_form = OverlapAdminPasswordChangeForm

    # 編集画面
    fieldsets = (
        ('ユーザ情報', {'fields': (
            'unique_account_id',
            'unique_user_id',
            'email',
            )}),
        ('認証情報', {'fields': (
            'is_active',
            'password',
            'date_password_change',
            'is_change_email_request',
            'is_social_login',
            )}),
        ('権限情報(管理者権限の設定のため操作注意)', {'fields': (
            'is_staff',
            'is_superuser',
            )}),
        ('その他', {'fields': (
            'before_last_login',
            'last_login',
            'date_create',
            'change_email',
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