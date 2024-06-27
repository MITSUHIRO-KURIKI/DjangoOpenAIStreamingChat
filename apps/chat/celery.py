from django.conf import settings
import os
from celery import Celery


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# https://stackoverflow.com/questions/45744992/celery-raises-valueerror-not-enough-values-to-unpack
if settings.DEBUG:
    os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')


app = Celery('apps_chat')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()