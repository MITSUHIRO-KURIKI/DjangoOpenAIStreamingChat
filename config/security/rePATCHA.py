from django.conf import settings
from config.read_env import read_env

# LOAD SECRET STEEINGS
env = read_env(settings.BASE_DIR)

RECAPTCHA_PUBLIC_KEY  = env.get_value('RECAPTCHA_PUBLIC_KEY',str)
RECAPTCHA_PRIVATE_KEY = env.get_value('RECAPTCHA_PRIVATE_KEY',str)