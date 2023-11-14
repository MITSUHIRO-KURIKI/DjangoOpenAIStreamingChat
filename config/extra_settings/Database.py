import os
import environ
from django.conf import settings

env = environ.Env()
env.read_env(os.path.join(settings.BASE_DIR, '.env'))

# Database
if os.getenv('GAE_APPLICATION', None):
    if settings.IS_USE_GC_SQL:
        # USE_CloudSQL:
        # アプリケーションからDBへの接続情報
        DATABASES = {
            'default': {
                'ENGINE':   'django.db.backends.mysql',
                'NAME':     env.get_value('DB_SQL_DB_NAME',str),
                'USER':     env.get_value('DB_SQL_USER_NAME',str),
                'PASSWORD': env.get_value('DB_SQL_USER_PASSWORD_GCP',str),
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
                'HOST':     'localhost',
                'PORT':     env.get_value('DB_SQL_LOCAL_PORT',str),
            }
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME':   settings.BASE_DIR / 'db.sqlite3',
            }
        }