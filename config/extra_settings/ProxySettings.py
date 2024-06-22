from django.conf import settings
from config.read_env import read_env

# LOAD SECRET STEEINGS
env = read_env(settings.BASE_DIR)

HTTP_PROXY  = f"http://{env.get_value('PROXY_PRIVATE_IP',str)}:{env.get_value('PROXY_PORT',str)}"
HTTPS_PROXY = f"https://{env.get_value('PROXY_PRIVATE_IP',str)}:{env.get_value('PROXY_PORT',str)}"