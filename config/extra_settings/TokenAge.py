import os
import environ
from django.conf import settings

env = environ.Env()
env.read_env(os.path.join(settings.BASE_DIR, '.env'))

# メール認証用Tokenの有効時間(秒)
EMAIL_CERTIFICATION_TOKEN_AGE = env.get_value('EMAIL_CERTIFICATION_TOKEN_AGE',int)
# USE 'auth_views.PasswordResetView'
PASSWORD_RESET_TIMEOUT = env.get_value('PASSWORD_RESET_TOKEN_AGE',int)