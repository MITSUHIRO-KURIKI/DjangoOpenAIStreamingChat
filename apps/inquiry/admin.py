from django.contrib import admin
from .models import Inquiry


class InquiryAdmin(admin.ModelAdmin):

    # 一覧画面
    list_display_ = ('unique_account_id',
                     'email',
                     'date_create',
                     'situation',
                     'date_complete',)
    list_filter   = []
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
    add_form      = None
    add_fieldsets = None
    
    # 編集画面
    fieldsets = (
        ('問い合わせ内容', {'fields': (
            'inquiry_text',
            'date_create',
            )}),
        ('照会者情報', {'fields': (
            'unique_account_id',
            'email',
            )}),
        ('対応状況', {'fields': (
            'situation',
            'date_complete',
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

admin.site.register(Inquiry, InquiryAdmin)