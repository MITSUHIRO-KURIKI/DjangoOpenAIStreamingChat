import os
import environ
from django.conf import settings

env = environ.Env()
env.read_env(os.path.join(settings.BASE_DIR, '.env'))

# MEASURE BRUTE FORCE ATTACK
AXES_FAILURE_LIMIT      = int(env.get_value('AXES_FAILURE_LIMIT',int)*2) # ログイン試行回数(なぜか1回で2カウントされるため2倍にする)
AXES_COOLOFF_TIME       = env.get_value('AXES_COOLOFF_TIME',int)         # アカウントロック時間(/HOURS)
AXES_ONLY_USER_FAILURES = env.get_value('AXES_ONLY_USER_FAILURES',bool)  # ロック対象をユーザ(DEFORT IP ADDRESS)
AXES_LOCKOUT_TEMPLATE   = 'accounts/AccountLock/lock.html'               # アカウントロック画面
AXES_RESET_ON_SUCCESS   = env.get_value('AXES_RESET_ON_SUCCESS',bool)    # ログイン成功で回数をリセット