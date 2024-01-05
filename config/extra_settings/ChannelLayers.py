import os
import environ
from django.conf import settings

env = environ.Env()
env.read_env(os.path.join(settings.BASE_DIR, '.env'))

if settings.IS_USE_RADIS or not settings.DEBUG:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                'hosts': [(env.get_value('RADIS_HOST',str), env.get_value('RADIS_PORT',int))],
            },
        },
    }
else:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer"
        }
    }
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }
