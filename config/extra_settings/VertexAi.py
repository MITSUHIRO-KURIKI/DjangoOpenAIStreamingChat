from django.conf import settings
from config.read_env import read_env

# LOAD SECRET STEEINGS
env = read_env(settings.BASE_DIR)

GCP_PROJECT_ID                              = env.get_value('GCP_PROJECT_ID',str)
VERTEX_AI_REGION                            = env.get_value('VERTEX_AI_REGION',str)
VERTEX_AI_MATCHING_ENGINE_API_ENDPOINT      = env.get_value('VERTEX_AI_MATCHING_ENGINE_API_ENDPOINT',str)
VERTEX_AI_MATCHING_ENGINE_INDEX_ENDPOINT    = env.get_value('VERTEX_AI_MATCHING_ENGINE_INDEX_ENDPOINT',str)
VERTEX_AI_MATCHING_ENGINE_DEPLOYED_INDEX_ID = env.get_value('VERTEX_AI_MATCHING_ENGINE_DEPLOYED_INDEX_ID',str)