import os
from django.conf import settings
from config.read_env import read_env

# LOAD SECRET STEEINGS
env = read_env(settings.BASE_DIR)

# https://zenn.dev/t0mmy/articles/internal_server_error_by_websocket
if os.getenv('GAE_APPLICATION', None) or os.getenv('GAE_INSTANCE', None):
    os.environ['ASGI_THREADS'] = '5'

if settings.IS_USE_RADIS or not settings.DEBUG:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                'hosts':    [(env.get_value('RADIS_HOST',str), env.get_value('RADIS_PORT',int))],
                'capacity': 1000,
                'expiry':   10,
            },
        },
    }
else:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels.layers.InMemoryChannelLayer',
            'CONFIG': {
                'capacity': 1000,
                'expiry':   10,
            },
        }
    }
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }