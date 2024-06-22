# https://cloud.google.com/python/django/appengine?hl=ja#understanding-secrets
import os
import environ

def read_env(BASE_DIR):
    env      = environ.Env()
    env_file = os.path.join(BASE_DIR, '.env')
    if os.path.isfile(env_file):
        # Use a local secret file, if provided
        env.read_env(env_file)
    elif os.environ.get('GOOGLE_CLOUD_PROJECT', None):
        # Pull secrets from Secret Manager
        import io
        from google.cloud.secretmanager import SecretManagerServiceClient
        project_id    = os.environ.get('GOOGLE_CLOUD_PROJECT')
        client        = SecretManagerServiceClient()
        settings_name = os.environ.get('SETTINGS_NAME', 'django_settings')
        name          = f'projects/{project_id}/secrets/{settings_name}/versions/latest'
        payload       = client.access_secret_version(name=name).payload.data.decode('UTF-8')
        env.read_env(io.StringIO(payload))
    else:
        raise Exception('No local .env or GOOGLE_CLOUD_PROJECT detected. No secrets found.')
    return env