from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .conf import settings
from .models import AccessAttempt, AccessLog, AccessFailureLog


class AccessAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "attempt_time",
        "ip_address",
        "user_agent",
        "username",
        "path_info",
        "failures_since_start",
    )

    list_filter = ["attempt_time",]

    search_fields = []

    date_hierarchy = "attempt_time"

    fieldsets = (
        (None, {"fields": ("path_info", "failures_since_start")}),
        (_("Form Data"), {"fields": ("get_data", "post_data")}),
        (_("Meta Data"), {"fields": ("user_agent", "ip_address", "http_accept")}),
    )

    readonly_fields = [
        "user_agent",
        "ip_address",
        "username",
        "http_accept",
        "path_info",
        "attempt_time",
        "get_data",
        "post_data",
        "failures_since_start",
    ]

    # 権限設定
    # 追加不可
    def has_add_permission(self, request) -> bool:
        return False
    # 表示可能
    def has_module_permission(self, request, obj=None) -> bool:
        return request.user.is_superuser or request.user.is_staff
    def has_view_permission(self, request, obj=None) -> bool:
        return request.user.is_superuser or request.user.is_staff
    # 変更不可
    def has_change_permission(self, request, obj=None) -> bool:
        return False
    # 削除は is_superuser のみ
    def has_delete_permission(self, request, obj=None) -> bool:
        return request.user.is_superuser


class AccessLogAdmin(admin.ModelAdmin):
    list_display = (
        "attempt_time",
        "logout_time",
        "ip_address",
        "username",
        "user_agent",
        "path_info",
    )

    list_filter = ["attempt_time", "logout_time",]

    search_fields = []

    date_hierarchy = "attempt_time"

    fieldsets = (
        (None, {"fields": ("path_info",)}),
        (_("Meta Data"), {"fields": ("user_agent", "ip_address", "http_accept")}),
    )

    readonly_fields = [
        "user_agent",
        "ip_address",
        "username",
        "http_accept",
        "path_info",
        "attempt_time",
        "logout_time",
    ]

    # 権限設定
    # 追加不可
    def has_add_permission(self, request) -> bool:
        return False
    # 表示可能
    def has_module_permission(self, request, obj=None) -> bool:
        return request.user.is_superuser or request.user.is_staff
    def has_view_permission(self, request, obj=None) -> bool:
        return request.user.is_superuser or request.user.is_staff
    # 変更不可
    def has_change_permission(self, request, obj=None) -> bool:
        return False
    # 削除は is_superuser のみ
    def has_delete_permission(self, request, obj=None) -> bool:
        return request.user.is_superuser


class AccessFailureLogAdmin(admin.ModelAdmin):
    list_display = (
        "attempt_time",
        "ip_address",
        "username",
        "user_agent",
        "path_info",
        "locked_out",
    )

    list_filter = ["attempt_time", "locked_out",]

    search_fields = []

    date_hierarchy = "attempt_time"

    fieldsets = (
        (None, {"fields": ("path_info",)}),
        (_("Meta Data"), {"fields": ("user_agent", "ip_address", "http_accept")}),
    )

    readonly_fields = [
        "user_agent",
        "ip_address",
        "username",
        "http_accept",
        "path_info",
        "attempt_time",
        "locked_out",
    ]

    # 権限設定
    # 追加不可
    def has_add_permission(self, request) -> bool:
        return False
    # 表示可能
    def has_module_permission(self, request, obj=None) -> bool:
        return request.user.is_superuser or request.user.is_staff
    def has_view_permission(self, request, obj=None) -> bool:
        return request.user.is_superuser or request.user.is_staff
    # 変更不可
    def has_change_permission(self, request, obj=None) -> bool:
        return False
    # 削除は is_superuser のみ
    def has_delete_permission(self, request, obj=None) -> bool:
        return request.user.is_superuser


if settings.AXES_ENABLE_ADMIN:
    admin.site.register(AccessAttempt, AccessAttemptAdmin)
    admin.site.register(AccessLog, AccessLogAdmin)
    admin.site.register(AccessFailureLog, AccessFailureLogAdmin)
