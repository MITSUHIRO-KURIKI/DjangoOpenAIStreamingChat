# References
# https://pypi.org/project/django-searchable-encrypted-fields/
import os
import environ
from django.conf import settings

env = environ.Env()
env.read_env(os.path.join(settings.BASE_DIR, '.env'))

FIELD_ENCRYPTION_KEYS = [
    env.get_value('FIELD_ENCRYPTION_KEYS_01',str),
]

ENCRYPTION_HASH_KEY = env.get_value('ENCRYPTION_HASH_KEY',str)
