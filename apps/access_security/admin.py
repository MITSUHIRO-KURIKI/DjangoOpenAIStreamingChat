from django.contrib import admin
from import_export.admin import ExportMixin
from import_export.resources import ModelResource
from .models import AccessSecurity, BlockIpList

class BlockIpListResource(ModelResource):
    class Meta:
        model  = BlockIpList
        fields = ('id',
                  'date_create',
                  'ip',
                  'reason',)
        export_order = fields
        clean_model_instances = True

class BlockIpListAdmin(ExportMixin, admin.ModelAdmin):

    resource_class = BlockIpListResource

    # 一覧画面
    list_display_ = ('date_create',
                     'ip',
                     'reason',)
    list_filter   = ['date_create',]
    list_display       = list_display_
    list_display_links = list_display_
    search_fields      = ()
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
        ('記録', {'fields': (
            'date_create',
            'ip',
            'reason',
            )}),
    )

    # 権限設定
    # CRUD を True で is_superuser に制限(is_stuff の権限剥奪)
    is_only_superuser_Create = True
    is_only_superuser_Read   = False
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


class AccessSecurityResource(ModelResource):
    class Meta:
        model  = AccessSecurity
        fields = ('id',
                  'date_create',
                  'ip',
                  'type',
                  'request_host_url',
                  'request_url',
                  'user_agent',
                  'csrf_token',
                  'time_zone',)
        export_order = fields
        clean_model_instances = True

class AccessSecurityAdmin(ExportMixin, admin.ModelAdmin):

    resource_class = AccessSecurityResource

    # 一覧画面
    list_display_ = ('date_create',
                     'ip',
                     'type',)
    list_filter   = ['type','date_create',]
    list_display       = list_display_
    list_display_links = list_display_
    search_fields      = ()
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
        ('記録', {'fields': (
            'date_create',
            'ip',
            'type',
            'request_host_url',
            'request_url',
            'user_agent',
            'csrf_token',
            'time_zone',
            )}),
    )

    # 権限設定
    # CRUD を True で is_superuser に制限(is_stuff の権限剥奪)
    is_only_superuser_Create = True
    is_only_superuser_Read   = False
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

admin.site.register(BlockIpList,    BlockIpListAdmin)
admin.site.register(AccessSecurity, AccessSecurityAdmin)