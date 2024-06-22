from django.conf import settings
from config.read_env import read_env

# LOAD SECRET STEEINGS
env = read_env(settings.BASE_DIR)

# DEFOLT LOGIN SESSION
# USER SET LOGIN SESSION RemenberTime write accounts.views.py
# Loginセッションの有効時間(秒)
SESSION_COOKIE_AGE = env.get_value('SESSION_COOKIE_AGE',int)
# Loginを維持する場合のセッションの有効時間(秒)
SESSION_COOKIE_SET_EXPIRY_AGE = env.get_value('SESSION_COOKIE_SET_EXPIRY_AGE',int)
# ブラウザを閉じたらLoginセッション終了
SESSION_EXPIRE_AT_BROWSER_CLOSE = env.get_value('SESSION_EXPIRE_AT_BROWSER_CLOSE',bool)