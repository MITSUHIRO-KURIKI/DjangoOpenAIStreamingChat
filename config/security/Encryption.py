# References
# https://pypi.org/project/django-searchable-encrypted-fields/
from django.conf import settings
from config.read_env import read_env

# LOAD SECRET STEEINGS
env = read_env(settings.BASE_DIR)

FIELD_ENCRYPTION_KEYS = [
    env.get_value('FIELD_ENCRYPTION_KEYS_01',str),
]

ENCRYPTION_HASH_KEY = env.get_value('ENCRYPTION_HASH_KEY',str)