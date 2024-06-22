from django.conf import settings
from config.read_env import read_env

# LOAD SECRET STEEINGS
env = read_env(settings.BASE_DIR)

# メール認証用Tokenの有効時間(秒)
EMAIL_CERTIFICATION_TOKEN_AGE = env.get_value('EMAIL_CERTIFICATION_TOKEN_AGE',int)
# USE 'auth_views.PasswordResetView'
PASSWORD_RESET_TIMEOUT = env.get_value('PASSWORD_RESET_TOKEN_AGE',int)