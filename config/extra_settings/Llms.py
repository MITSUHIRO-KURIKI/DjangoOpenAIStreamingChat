from django.conf import settings
from config.read_env import read_env

# LOAD SECRET STEEINGS
env = read_env(settings.BASE_DIR)

OPENAI_API_KEY                  = env.get_value('OPENAI_API_KEY',str)
AZURE_OPENAI_ENDPOINT           = env.get_value('AZURE_OPENAI_ENDPOINT',str)
AZURE_OPENAI_API_VERSION        = env.get_value('AZURE_OPENAI_API_VERSION',str)
AZURE_OPENAI_DEFAULT_MODEL_NAME = env.get_value('AZURE_OPENAI_DEFAULT_MODEL_NAME',str)