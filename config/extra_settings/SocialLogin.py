import os
import environ
from django.conf import settings
from unidecode import unidecode

env = environ.Env()
env.read_env(os.path.join(settings.BASE_DIR, '.env'))

# Reference
# https://sinyblog.com/django/social-auth-app-django/
# https://python-social-auth.readthedocs.io/en/latest/use_cases.html#improve-unicode-cleanup-from-usernames
SOCIAL_AUTH_REDIRECT_IS_HTTPS       = False if settings.DEBUG or not os.getenv('GAE_APPLICATION', None) else True # デバック時には HTTPS化 無効
SOCIAL_AUTH_CLEAN_USERNAME_FUNCTION = 'unidecode.unidecode'
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY       = env.get_value('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY',str)                          # クライアントID
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET    = env.get_value('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET',str)                       # クライアント シークレット