from django.conf import settings
from config.read_env import read_env

# LOAD SECRET STEEINGS
env = read_env(settings.BASE_DIR)

IS_ADMIN_NOTICE  = env.get_value('IS_ADMIN_NOTICE',bool)
ADMIN_EMAIL_LIST = env.get_value('ADMIN_EMAIL_LIST',str).split(',') # 管理者宛連絡のメールアドレス(, 区切りで複数指定可能. スペース開けないこと)

if settings.IS_USE_EMAIL_SERVICE:
    # # SendGrid
    # EMAIL_HOST          = 'smtp.sendgrid.net'
    # EMAIL_PORT          = env.get_value('SENDGRID_EMAIL_PORT',int)
    # EMAIL_USE_TLS       = env.get_value('SENDGRID_EMAIL_USE_TLS',bool)
    # EMAIL_HOST_USER     = env.get_value('SENDGRID_EMAIL_HOST_USER',str)
    # EMAIL_HOST_PASSWORD = env.get_value('SENDGRID_EMAIL_HOST_PASSWORD',str)
    # DEFAULT_FROM_EMAIL  = env.get_value('SENDGRID_DEFAULT_FROM_EMAIL',str)
    # DEFAULT_REPLY_EMAIL = env.get_value('SENDGRID_DEFAULT_REPLY_EMAIL',str)
        
    # Gmail
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