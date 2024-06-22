from django.contrib import admin
from import_export.admin import ExportMixin
from import_export.resources import ModelResource
from .models import Inquiry

class InquiryResource(ModelResource):
    class Meta:
        model  = Inquiry
        fields = ('id',
                  'unique_account_id',
                  'email',
                  'inquiry_text',
                  'ip_address',
                  'date_create',
                  'situation',
                  'date_complete',
                  'is_notice_admin',
                  )
        export_order = fields
        clean_model_instances = True

class InquiryAdmin(ExportMixin, admin.ModelAdmin):
    
    resource_class = InquiryResource
    
    # 表示する文字数の制限▽
    def character_limit_inquiry_text(self, obj):
        limit=20
        character = obj.inquiry_text
        if character:
            if len(character)>limit:
                character=character[:limit]+'...'
        return character
    # 表示する文字数の制限△

    # 一覧画面
    list_display_ = ('unique_account_id',
                     'email',
                     'character_limit_inquiry_text',
                     'date_create',
                     'situation',
                     'date_complete',
                     'is_notice_admin',)
    list_filter        = ['is_notice_admin','situation',]
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
            'ip_address',
            )}),
        ('対応状況', {'fields': (
            'situation',
            'date_complete',
            )}),
        ('その他', {'fields': (
            'is_notice_admin',
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