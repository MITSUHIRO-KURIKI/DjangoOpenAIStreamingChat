import os
import environ
from django.conf import settings

env = environ.Env()
env.read_env(os.path.join(settings.BASE_DIR, '.env'))

FRONTEND_URL = env.get_value('FRONTEND_URL',str)