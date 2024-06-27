import os
from django.conf import settings
from config.read_env import read_env

# LOAD SECRET STEEINGS
env = read_env(settings.BASE_DIR)

if settings.DEBUG:
    CELERY_BROKER_URL         = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND     = 'redis://localhost:6379'
else:
    CELERY_BROKER_URL         = f"redis://{env.get_value('RADIS_HOST',str)}:{env.get_value('RADIS_PORT',int)}"
    CELERY_RESULT_BACKEND     = f"redis://{env.get_value('RADIS_HOST',str)}:{env.get_value('RADIS_PORT',int)}"

CELERY_ACCEPT_CONTENT     = env.get_value('CELERY_ACCEPT_CONTENT',str).split(',')
CELERY_TASK_SERIALIZER    = env.get_value('CELERY_TASK_SERIALIZER',str)
CELERY_RESULT_SERIALIZER  = env.get_value('CELERY_RESULT_SERIALIZER',str)
CELERY_TASK_TRACK_STARTED = env.get_value('CELERY_TASK_TRACK_STARTED',bool)
CELERY_TIMEZONE           = env.get_value('CELERY_TIMEZONE',str)