import os
import environ
from django.conf import settings

env = environ.Env()
env.read_env(os.path.join(settings.BASE_DIR, '.env'))

RECAPTCHA_PUBLIC_KEY  = env.get_value('RECAPTCHA_PUBLIC_KEY',str)
RECAPTCHA_PRIVATE_KEY = env.get_value('RECAPTCHA_PRIVATE_KEY',str)