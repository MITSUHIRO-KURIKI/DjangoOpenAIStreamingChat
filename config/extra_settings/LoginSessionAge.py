import os
import environ
from django.conf import settings

env = environ.Env()
env.read_env(os.path.join(settings.BASE_DIR, '.env'))

# DEFOLT LOGIN SESSION
# USER SET LOGIN SESSION RemenberTime write accounts.views.py
# Loginセッションの有効時間(秒)
SESSION_COOKIE_AGE = env.get_value('SESSION_COOKIE_AGE',int)
# ブラウザを閉じたらLoginセッション終了
SESSION_EXPIRE_AT_BROWSER_CLOSE = env.get_value('SESSION_EXPIRE_AT_BROWSER_CLOSE',bool)