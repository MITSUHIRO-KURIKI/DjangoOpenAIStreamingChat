import os
import environ
from django.conf import settings

env = environ.Env()
env.read_env(os.path.join(settings.BASE_DIR, '.env'))

OPENAI_API_KEY = env.get_value('OPENAI_API_KEY',str)