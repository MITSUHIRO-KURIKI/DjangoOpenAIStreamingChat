from django.apps import AppConfig


class UserPropertiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    
    name         = 'apps.user_properties'
    verbose_name = '02_ユーザ情報'