import os
import environ
from django.conf import settings

env = environ.Env()
env.read_env(os.path.join(settings.BASE_DIR, '.env'))

ADMIN_NOTICE_EMAIL = env.get_value('ADMIN_NOTICE_EMAIL',str)

if settings.IS_USE_GMAIL:
    EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST          = 'smtp.gmail.com'
    EMAIL_PORT          = env.get_value('EMAIL_PORT',int)
    EMAIL_USE_TLS       = env.get_value('EMAIL_USE_TLS',bool)
    DEFAULT_FROM_EMAIL  = env.get_value('DEFAULT_FROM_EMAIL',str)
    DEFAULT_REPLY_EMAIL = env.get_value('DEFAULT_REPLY_EMAIL',str)
    EMAIL_HOST_USER     = env.get_value('EMAIL_HOST_USER',str)
    EMAIL_HOST_PASSWORD = env.get_value('EMAIL_HOST_PASSWORD',str)
else:
    EMAIL_BACKEND       = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL  = 'debug@mail.debug'
    DEFAULT_REPLY_EMAIL = 'noreply@mail.debug'