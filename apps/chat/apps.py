from django.apps import AppConfig


class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    
    name         = 'apps.chat'
    verbose_name = '10_Chat'