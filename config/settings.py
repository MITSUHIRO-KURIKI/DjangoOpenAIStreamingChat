import os
import environ
from pathlib import Path

# 全体設定▽
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# 管理者へのメール通知設定
# 問い合わせがきた際やアカウントブロック(config.security.AccessSecurityMiddleware)が発生した際など
IS_NOTIFICATION_ADMIN = False

# 認証設定
IS_USE_EMAIL_CERTIFICATION = False  # メール送信でメールアドレスを認証する
IS_USE_SOCIAL_LOGIN        = False  # ソーシャルログインを有効にする
IS_USE_RECAPTCHA           = False  # RECAPTCHA を有効にする

# GMAIL/GCP
IS_USE_GMAIL  = False  # メール送信にGmailを利用する
IS_USE_GCS    = False  # GCS を利用する
IS_USE_GC_SQL = False  # CloudSQL を利用する

# RADIS(WebSoocket)
IS_USE_RADIS = False
# 全体設定△


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# LOAD SECRET STEEINGS
env = environ.Env()
env.read_env(os.path.join(BASE_DIR,'.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.get_value('DJANGO_SECRET_KEY',str)

# [LOAD security] Encryption.py
try:
    from .security.Encryption import *
except ImportError:
    pass

# ALLOWED_HOSTS
if os.getenv('GAE_APPLICATION', None):
    ALLOWED_HOSTS = [env.get_value('ALLOWED_HOSTS_01',str)]
else:
    ALLOWED_HOSTS = [env.get_value('ALLOWED_HOSTS_DEBUG',str)]

# Application definition
INSTALLED_APPS = [
    # CREATE APPS
    'accounts.apps.AccountsConfig',                         # First Migrate is only 'makemigrations accounts'
    'apps.access_security.apps.AccessSecurityConfig',
    'apps.chat.apps.ChatConfig',
    'apps.user_properties.apps.UserPropertiesConfig',
    'apps.inquiry.apps.InquiryConfig',
    # DEFAULT or INSTALL APPS
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'daphne',                                               # ADD daphne
    'django.contrib.staticfiles',
    'rest_framework',                                       # ADD rest_framework
    'channels',                                             # ADD channels
    'encrypted_fields',                                     # ADD django-searchable-encrypted-fields
    'common.lib.axes.apps.AxesConfig',                      # ADD django-axes
    'storages',                                             # ADD django-storages
    'common.lib.social_django.apps.PythonSocialAuthConfig', # ADD social-auth-app-django
    'extra_views',                                          # ADD django-extra-views
    'sorl.thumbnail',                                       # ADD ImageFile Resize
    'django_cleanup',                                       # ADD django-cleanup(DELETE OLD IMAGE/ NOT DELETE MODEL DECORATE '@cleanup.ignore')
    'templatetags.apps.TemplatetagsConfig',                 # Custom Template Filter
]

# [LOAD security.admin_protect] AdminProtectSetting.py
try:
    from .admin_protect.AdminProtectSetting import *
except ImportError:
    pass

# MIDDLEWARE
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'config.security.AccessSecurityMiddleware.AccessSecurityMiddleware',               # ADD Custom AccessSecurityMiddleware
    'common.lib.social_django.middleware.SocialAuthExceptionMiddleware',               # ADD social-auth-app-django
    'config.acsess_logic.AccessBusinessLogicMiddleware.AccessBusinessLogicMiddleware', # ADD Custom AccessBusinessLogicMiddleware
    'config.admin_protect.AdminProtect.AdminProtect',                                  # ADD AdminProtect **MUST BEFORE AXES**
    'common.lib.axes.middleware.AxesMiddleware',                                       # ADD django-axes  **MUST BOTTOM**
]

# ADD social-auth-app-django
AUTHENTICATION_BACKENDS = (
    'common.lib.axes.backends.AxesBackend',                # ADD django-axes **MUST TOP**
    'common.lib.social_core.backends.google.GoogleOAuth2', # Google OAuth2
    'django.contrib.auth.backends.ModelBackend',           # backends **MUST BUTTOM**
)

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',                   # ADD USE TEMPLATE {{ MEDIA_URL }}
                'common.lib.social_django.context_processors.backends',       # ADD social-auth-app-django
                'common.lib.social_django.context_processors.login_redirect', # ADD social-auth-app-django
                "templatetags.context_processors.FRONTEND_URL"                # USE {{FRONTEND_URL}}
            ],
            'libraries': {
                # Custom Template Simple Tag
                'access_dict':                'templatetags.common.AccessDict',
                'access_list':                'templatetags.common.AccessList',
                'calculation_Add':            'templatetags.common.Calculation',
                'calculation_Multiplication': 'templatetags.common.Calculation',
                'calculation_Division':       'templatetags.common.Calculation',
                # Custom Template Filter

            },
        },
    },
]
if DEBUG:
    # templates で {{DEBUG}} を使えるようにする
    TEMPLATES[0]['OPTIONS']['context_processors'] += 'templatetags.context_processors.IS_DEBUG',

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'
# [LOAD extra_settings] ChannelLayers.py
try:
    from .extra_settings.ChannelLayers import *
except ImportError:
    pass

# [LOAD extra_settings] Database.py
try:
    from .extra_settings.Database import *
except ImportError:
    pass

# [LOAD security] PasswordHashers.py
try:
    from .security.PasswordHashers import *
except ImportError:
    pass

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    { "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator", },
    { "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
      'OPTIONS': {'min_length': 8,}, },
    { "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator", },
    { "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator", },
]

# SUCSESS LOGIN AND LOGPUT REDIRECT PATH
LOGIN_URL           = 'accounts:login'
LOGIN_REDIRECT_URL  = 'home'
LOGOUT_REDIRECT_URL = 'accounts:login'

# Internationalization
LANGUAGE_CODE = 'ja'         # 言語設定
TIME_ZONE     = 'Asia/Tokyo' # タイムゾーン設定
USE_I18N      = True
USE_L10N      = True
USE_TZ        = True

# AUTH USER MODELS
AUTH_USER_MODEL = 'accounts.CustomUser'

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# [LOAD security] DjangoAxes.py
try:
    from .security.DjangoAxes import *
except ImportError:
    pass
# [rePATCHA security] rePATCHA.py
if IS_USE_RECAPTCHA:
    try:
        from .security.rePATCHA import *
    except ImportError:
        pass
# [LOAD extra_settings] EmailBackend.py
try:
    from .extra_settings.EmailBackend import *
except ImportError:
    pass
# [LOAD extra_settings] FrontendURL.py
try:
    from .extra_settings.FrontendURL import *
except ImportError:
    pass
# [LOAD extra_settings] Llms.py
try:
    from .extra_settings.Llms import *
except ImportError:
    pass
# [LOAD extra_settings] LoginSessionAge.py
try:
    from .extra_settings.LoginSessionAge import *
except ImportError:
    pass
# [LOAD extra_settings] RestFrameWork.py
try:
    from .extra_settings.RestFrameWork import *
except ImportError:
    pass
# [SocialLogin extra_settings] SocialLogin.py
if IS_USE_SOCIAL_LOGIN:
    try:
        from .extra_settings.SocialLogin import *
    except ImportError:
        pass
# [LOAD extra_settings] StaticMediaFiles.py
try:
    from .extra_settings.StaticMediaFiles import *
except ImportError:
    pass
# [LOAD extra_settings] TokenAge.py
try:
    from .extra_settings.TokenAge import *
except ImportError:
    pass