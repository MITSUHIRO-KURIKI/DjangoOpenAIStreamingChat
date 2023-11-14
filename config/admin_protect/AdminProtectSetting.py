import os
import environ
from django.conf import settings

env = environ.Env()
env.read_env(os.path.join(settings.BASE_DIR, '.env'))

ADMIN_PATH       = env.get_value('ADMIN_PATH',str)                  # 管理画面URL
ALLOWED_IP_ADMIN = env.get_value('ALLOWED_IP_ADMIN',str).split(',') # 管理画面 アクセス許可IPアドレス(, 区切りで複数指定可能. スペース開けないこと)