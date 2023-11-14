from django.apps import AppConfig


class AccessSecurityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    
    name         = 'apps.access_security'
    verbose_name = '99_アクセスブロック'