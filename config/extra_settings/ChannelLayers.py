import os
from django.conf import settings
from config.read_env import read_env

# LOAD SECRET STEEINGS
env = read_env(settings.BASE_DIR)

# https://zenn.dev/t0mmy/articles/internal_server_error_by_websocket
if os.getenv('GAE_APPLICATION', None) or os.getenv('GAE_INSTANCE', None):
    os.environ['ASGI_THREADS'] = '5'

# https://github.com/django/channels_redis
if settings.DEBUG:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
        },
    }
else:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                'hosts':        [(env.get_value('RADIS_HOST',str), env.get_value('RADIS_PORT',int))],
                'expiry':       env.get_value('RADIS_EXPIRY',int),
                'group_expiry': env.get_value('RADIS_GROUP_EXPIRY',int),
                'capacity':     env.get_value('RADIS_CAPACITY',int),
            },
        },
    }

# # channel のみ利用であれば以下でローカル時にはインメモリで実行可能
# # celery と channel を組み合わせる場合には同じキャッシュメモリを参照
# # しないとうまくいかないため Radis 等必須
# if settings.IS_USE_RADIS or not settings.DEBUG:
#     CHANNEL_LAYERS = {
#         'default': {
#             'BACKEND': 'channels_redis.core.RedisChannelLayer',
#             'CONFIG': {
#                 'hosts':        [(env.get_value('RADIS_HOST',str), env.get_value('RADIS_PORT',int))],
#                 'expiry':       env.get_value('RADIS_EXPIRY',int),
#                 'group_expiry': env.get_value('RADIS_GROUP_EXPIRY',int),
#                 'capacity':     env.get_value('RADIS_CAPACITY',int),
#             },
#         },
#     }
# else:
#     CHANNEL_LAYERS = {
#         'default': {
#             'BACKEND': 'channels.layers.InMemoryChannelLayer',
#             'CONFIG': {
#                 'capacity': 1000,
#                 'expiry':   10,
#             },
#         }
#     }
#     CACHES = {
#         'default': {
#             'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#         }
#     }