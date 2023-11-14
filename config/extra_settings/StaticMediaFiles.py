import os
import environ
from django.conf import settings

env = environ.Env()
env.read_env(os.path.join(settings.BASE_DIR, '.env'))

# THUMBNAIL
# https://sorl-thumbnail.readthedocs.io/en/latest/reference/settings.html
# https://github.com/jazzband/sorl-thumbnail/tree/master
THUMBNAIL_PRESERVE_FORMAT = True # True: Preservation of format
THUMBNAIL_FORCE_OVERWRITE = True
USER_ICON_RESIZE_WIDTH    = 400
USER_ICON_RESIZE_HEIGHT   = 400

# Static files
STATIC_URL = '/static/'
# Media files
MEDIA_URL = '/media/'

if os.getenv('GAE_APPLICATION', None):
    from google.oauth2 import service_account
    STORAGES = {
        'default':     {'BACKEND': 'storages.backends.gcloud.GoogleCloudStorage'},
        'staticfiles': {'BACKEND': 'storages.backends.gcloud.GoogleCloudStorage'},
    }
    GS_CREDENTIALS_JSON = env.get_value('GS_CREDENTIALS_JSON',str)
    GS_CREDENTIALS      = service_account.Credentials.from_service_account_file(
        os.path.join(settings.BASE_DIR, GS_CREDENTIALS_JSON),
    )
    GS_PROJECT_ID       = env.get_value('GPC_PROJECT_ID',str)
    GS_BUCKET_NAME      = env.get_value('GS_BUCKET_NAME',str)
    GS_IS_GZIPPED       = False
    GS_DEFAULT_ACL      = None
    GS_QUERYSTRING_AUTH = False # 公開URL設定: Trueで認証型URL
    GS_FILE_OVERWRITE   = True
    
    # Static files
    STATIC_ROOT = os.path.join(settings.BASE_DIR, 'static')
    STATICFILES_DIRS = [
        os.path.join(settings.BASE_DIR, 'static')
        ]
    # Media files
    MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'media')
else:
    # Static files
    STATICFILES_DIRS = [ os.path.join(settings.BASE_DIR, 'static') ]
    # Media files
    MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'media')
    
    if settings.IS_USE_GCS:
        from google.oauth2 import service_account
        STORAGES = {
            'default':     {'BACKEND': 'storages.backends.gcloud.GoogleCloudStorage'},
            'staticfiles': {'BACKEND': 'storages.backends.gcloud.GoogleCloudStorage'},
        }
        GS_CREDENTIALS_JSON = env.get_value('GS_CREDENTIALS_JSON',str)
        GS_CREDENTIALS      = service_account.Credentials.from_service_account_file(
            os.path.join(settings.BASE_DIR, GS_CREDENTIALS_JSON),
        )
        GS_PROJECT_ID       = env.get_value('GPC_PROJECT_ID',str)
        GS_BUCKET_NAME      = env.get_value('GS_BUCKET_NAME',str)
        STATIC_ROOT         = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/'