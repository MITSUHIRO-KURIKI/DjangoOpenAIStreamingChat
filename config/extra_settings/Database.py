import os
from config.read_env import read_env
from django.conf import settings

# LOAD SECRET STEEINGS
env = read_env(settings.BASE_DIR)

# Database
if os.getenv('GAE_APPLICATION', None) or os.getenv('GAE_INSTANCE', None):
    if settings.IS_USE_GC_SQL:
        # USE_CloudSQL:
        # アプリケーションからDBへの接続情報
        DATABASES = {
            'default': {
                'ENGINE':   'django.db.backends.mysql',
                'NAME':     env.get_value('DB_SQL_DB_NAME',str),
                'USER':     env.get_value('DB_SQL_USER_NAME',str),
                'PASSWORD': env.get_value('DB_SQL_USER_PASSWORD_GCP',str),
                # 'HOST':     env.get_value('DB_SQL_PRIVATE_IP',str),
                'HOST':     '/cloudsql/' + env.get_value('DB_SQL_CONNECTION_NAME',str),
            }
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME':   settings.BASE_DIR / 'db.sqlite3',
            }
        }
else:
    if settings.IS_USE_GC_SQL:
        # USE_CloudSQL:
        # ローカルからマイグレーションする際の接続情報
        DATABASES = {
            'default': {
                'ENGINE':   'django.db.backends.mysql',
                'NAME':     env.get_value('DB_SQL_DB_NAME',str),
                'USER':     env.get_value('DB_SQL_USER_NAME',str),
                'PASSWORD': env.get_value('DB_SQL_USER_PASSWORD_GCP',str),
                # 'HOST':     env.get_value('DB_SQL_PUBLIC_IP',str),
                'HOST':     'localhost',
                # 'PORT':     env.get_value('DB_SQL_LOCAL_PORT',str),
            }
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME':   settings.BASE_DIR / 'db.sqlite3',
            }
        }