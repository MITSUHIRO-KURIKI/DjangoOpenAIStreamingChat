from django.conf import settings
from config.read_env import read_env

# LOAD SECRET STEEINGS
env = read_env(settings.BASE_DIR)

FRONTEND_URL = env.get_value('FRONTEND_URL',str)