import os
from django.conf import settings
from unidecode import unidecode
from config.read_env import read_env

# LOAD SECRET STEEINGS
env = read_env(settings.BASE_DIR)

# Reference
# https://sinyblog.com/django/social-auth-app-django/
# https://python-social-auth.readthedocs.io/en/latest/use_cases.html#improve-unicode-cleanup-from-usernames
# デバック時には HTTPS化 無効
SOCIAL_AUTH_REDIRECT_IS_HTTPS       = False if settings.DEBUG or not os.getenv('GAE_APPLICATION', None) or not os.getenv('GAE_INSTANCE', None) else True
SOCIAL_AUTH_CLEAN_USERNAME_FUNCTION = 'unidecode.unidecode'
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY       = env.get_value('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY',str)    # クライアントID
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET    = env.get_value('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET',str) # クライアント シークレット