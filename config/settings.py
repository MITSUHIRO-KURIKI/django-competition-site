import os
from pathlib import Path
import environ
from unidecode import unidecode


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
USE_SOCIAL_LOGIN = False
USE_EMAIL_CERTIFICATION = False
USE_EMAIL_NOTIFICATION = False
USE_EMAIL_INQUIRY_NOTIFICATION_ADMIN = False
USE_RECAPTCHA = False
USE_GCS = False
USE_CloudSQL = False
if USE_GCS:
    from google.oauth2 import service_account
USE_DJANGO_TOOLBAR = False

# Build paths inside the project like this: BASE_DIR / 'subdir'.
if DEBUG:
    BASE_DIR = Path(__file__).resolve().parent.parent
else:
    if USE_GCS:
        BASE_DIR = Path(__file__).resolve().parent.parent
        # BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    else:
        BASE_DIR = Path(__file__).resolve().parent.parent


# LOAD SECRET STEEINGS
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.get_value('SECRET_KEY',str)


# SEND EMAIL
if USE_EMAIL_CERTIFICATION or USE_EMAIL_NOTIFICATION:
    if DEBUG:
        EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
        FROM_EMAIL_ADDRESS = env.get_value('FROM_EMAIL_ADDRESS',str)
    else:
        EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
        EMAIL_HOST = env.get_value('EMAIL_HOST',str)
        EMAIL_PORT = env.get_value('EMAIL_PORT',int)
        EMAIL_HOST_USER = env.get_value('EMAIL_HOST_USER',str)
        EMAIL_HOST_PASSWORD = env.get_value('EMAIL_HOST_PASSWORD',str)
        EMAIL_USE_TLS = env.get_value('EMAIL_USE_TLS',bool)
        DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
        FROM_EMAIL_ADDRESS = EMAIL_HOST_USER

if USE_EMAIL_INQUIRY_NOTIFICATION_ADMIN:
    ADMIN_EMAIL_ADDRESS = env.get_value('ADMIN_EMAIL_ADDRESS',str)


# ALLOWED HOSTS
if os.getenv('GAE_APPLICATION', None):
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = [
    # CREATE APPS
    'accounts.apps.AccountsConfig', # First Migrate is only 'makemigrations accounts'
    'user_profile.apps.UserProfileConfig',
    'user_settings.apps.UserSettingsConfig',
    'competitions.apps.CompetitionsConfig',
    'submission.apps.SubmissionConfig',
    'discussions_and_notebooks.apps.Discussions_and_notebooksConfig',
    'comments.apps.CommentsConfig',
    'bookmark.apps.BookmarkConfig',
    'vote.apps.VoteConfig',
    'user_inquiry.apps.UserInquiryConfig',
    'management.apps.ManagementConfig',
    # DEFAULT or INSTALL APPS
    'django.contrib.admin',
    'django.contrib.auth',
    'social_django', # ADD social-auth-app-django
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'axes', # ADD django-axes
    'sorl.thumbnail',  # ADD ImageFile Resize
    'django_cleanup', # ADD django-cleanup(DELETE OLD IMAGE/ NOT DELETE MODEL DECORATE '@cleanup.ignore')
    'extra_views',# ADD django-extra-views
    'django_summernote',# ADD django-summernote
    'templatetags.apps.TemplatetagsConfig', # Custom Template Filter
    'django.contrib.humanize',
    'django_extensions', # Model ER Graph django-extensions
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware', # ADD social-auth-app-django
    'axes.middleware.AxesMiddleware', # ADD django-axes **MUST BOTTOM**
]
if USE_DJANGO_TOOLBAR:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

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
                'django.template.context_processors.media', # ADD USE TEMPLATE {{ MEDIA_URL }}
                'social_django.context_processors.backends',  # ADD social-auth-app-django
                'social_django.context_processors.login_redirect', # ADD social-auth-app-django
            ],
            'libraries': {
                'split_slash_text': 'templatetags.common.SplitText', # Custom Template Filter
                'split_blank_text': 'templatetags.common.SplitText', # Custom Template Tag
                'date2remain_days_or_progress_days': 'templatetags.common.Date2ProgressRemain', # Custom Template Filter
                'stringformat_s': 'templatetags.common.StringFormat', # Custom Template Tag
                'access_dict': 'templatetags.common.AccessDict', # Custom Template Simple Tag
                'access_list': 'templatetags.common.AccessList', # Custom Template Simple Tag
                'calculation_Add': 'templatetags.common.Calculation', # Custom Template Simple Tag
                'calculation_Multiplication': 'templatetags.common.Calculation', # Custom Template Simple Tag
                'calculation_Division': 'templatetags.common.Calculation', # Custom Template Simple Tag
                'num2locate': 'templatetags.user_profile.Num2Locate', # Custom Template Filter
                'num2gender': 'templatetags.user_profile.Num2Gender', # Custom Template Filter
                'date2progressrate': 'templatetags.competitions.Date2Active', # Custom Template Filter
                'date2progress_days': 'templatetags.competitions.Date2Active', # Custom Template Filter
                'date2remain_days': 'templatetags.competitions.Date2Active', # Custom Template Filter
                'object2votes_sum': 'templatetags.vote.Object2VotesSum', # Custom Template Tag
                'object2uer_votes_situation': 'templatetags.vote.Object2UserVotesSituation', # Custom Template Tag
            },
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


NUMBER_GROUPING = 3


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
if os.getenv('GAE_APPLICATION', None):
    import pymysql
    pymysql.install_as_MySQLdb()
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': env.get_value('DB_SQL_NAME',str),
            'USER': env.get_value('DB_SQL_USER',str),
            'PASSWORD': env.get_value('DB_SQL_PASSWORD_GCP',str),
            'HOST': env.get_value('DB_SQL_HOST',str),
        }
    }
else:
    if USE_CloudSQL:
        import pymysql
        pymysql.install_as_MySQLdb()
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': env.get_value('DB_SQL_NAME',str),
                'USER': env.get_value('DB_SQL_USER',str),
                'PASSWORD': env.get_value('DB_SQL_PASSWORD_GCP',str),
                'HOST': 'localhost',
                'PORT': '3306',
            }
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
        # DATABASES = {
        #     'default': {
        #         'ENGINE': 'django.db.backends.mysql',
        #         'NAME': env.get_value('DB_SQL_NAME',str),
        #         'USER': 'root',
        #         'PASSWORD': env.get_value('DB_SQL_PASSWORD_LOCAL',str),
        #         'HOST': '127.0.0.1',
        #         'PORT': '3307',
        #     }
        # }


# AUTH USER MODELS
AUTH_USER_MODEL = 'accounts.CustomUser'


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 4,}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Password Hash algorithm
# PASSWORD_HASHERS = [
#     'django.contrib.auth.hashers.Argon2PasswordHasher',
#     'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
#     'django.contrib.auth.hashers.BCryptPasswordHasher',
#     'django.contrib.auth.hashers.PBKDF2PasswordHasher',
#     'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
# ]


# USE 'auth_views.PasswordResetView'
PASSWORD_RESET_TIMEOUT = 60*60*24


# ADD social-auth-app-django
AUTHENTICATION_BACKENDS = (
    'axes.backends.AxesBackend', # ADD django-axes **MUST TOP**
    # 'social_core.backends.open_id.OpenIdAuth',  # OpenId
    # 'social_core.backends.google.GoogleOpenId',  # Google OpenId
    'social_core.backends.google.GoogleOAuth2',  # Google OAuth2
    # 'social_core.backends.github.GithubOAuth2',  # Github
    # 'social_core.backends.twitter.TwitterOAuth',  # Twitter
    # 'social_core.backends.facebook.FacebookOAuth2',  # Facebook
    'django.contrib.auth.backends.ModelBackend',  # backends
)
if not DEBUG:
    SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

# https://python-social-auth.readthedocs.io/en/latest/use_cases.html#improve-unicode-cleanup-from-usernames
if USE_SOCIAL_LOGIN:
    SOCIAL_AUTH_CLEAN_USERNAME_FUNCTION = 'unidecode.unidecode'
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env.get_value('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY',str)  # クライアントID
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env.get_value('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET',str) # クライアント シークレット


# ADD reCAPTCHA
if USE_RECAPTCHA:
    RECAPTCHA_PUBLIC_KEY = env.get_value('RECAPTCHA_PUBLIC_KEY',str)
    RECAPTCHA_PRIVATE_KEY = env.get_value('RECAPTCHA_PRIVATE_KEY',str)


# MEASURE BRUTE FORCE ATTACK
AXES_FAILURE_LIMIT = env.get_value('AXES_FAILURE_LIMIT',int) # ログイン試行回数
AXES_COOLOFF_TIME = env.get_value('AXES_COOLOFF_TIME',int) # アカウントロック時間(/HOURS)
AXES_ONLY_USER_FAILURES = env.get_value('AXES_ONLY_USER_FAILURES',bool) # ロック対象をユーザ(DEFORT IP ADDRESS)
AXES_LOCKOUT_TEMPLATE = 'accounts/LogIn_LogOut/account_lock.html'
AXES_RESET_ON_SUCCESS = env.get_value('AXES_RESET_ON_SUCCESS',bool) # ログイン成功で回数をリセット


# SUCSESS LOGIN AND LOGPUT REDIRECT PATH
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'


# CREATE USER TOKEN EXPIRY
CREATE_USER_TOKEN_EXPIRED_SECOUND_TIME = env.get_value('CREATE_USER_TOKEN_EXPIRED_SECOUND_TIME',int)


# DEFOLT LOGIN SESSION
# USER SET LOGIN SESSION RemenberTime write accounts.views.py
SESSION_COOKIE_AGE = env.get_value('SESSION_COOKIE_AGE',int)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False # ブラウザを閉じたらセッション終了


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = 'ja' #言語設定
TIME_ZONE = 'Asia/Tokyo' #タイムゾーン設定
USE_I18N = True
USE_L10N = True
USE_TZ = True


PROJECT_NAME = os.path.basename(BASE_DIR)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
GS_BUCKET_NAME = env.get_value('GS_BUCKET_NAME',str)
GS_PROJECT_ID = env.get_value('GS_PROJECT_ID',str)
if USE_GCS:
    GS_CREDENTIALS_JSON = env.get_value('GS_CREDENTIALS_JSON',str)
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
        os.path.join(BASE_DIR, GS_CREDENTIALS_JSON),
        )

STATIC_URL = '/static/'
if USE_GCS:
    GS_QUERYSTRING_AUTH = True
    GS_DEFAULT_ACL = None
    STATIC_ROOT = env.get_value('GS_STATIC_URL',str)
    STATICFILES_DIRS = [ os.path.join(BASE_DIR, "static") ] #これがないとstaticに現在入っているファイルが上がらない
    STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
elif os.getenv('GAE_APPLICATION', None):
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
    # STATICFILES_DIRS = [ STATIC_ROOT ]
else:
    # STATIC_ROOT = os.path.join(BASE_DIR, "static")
    STATICFILES_DIRS = [ os.path.join(BASE_DIR, "static") ]

# Media files
MEDIA_URL = '/media/'
if USE_GCS:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
elif os.getenv('GAE_APPLICATION', None):
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
else:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



# https://sorl-thumbnail.readthedocs.io/en/latest/reference/settings.html
THUMBNAIL_PRESERVE_FORMAT = True # True: Preservation of format


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

GRAPH_MODELS = {
  'app_labels': ["user_profile",],
}


# Development Environment
if os.getenv('GAE_APPLICATION', None):
    FRONTEND_URL = '**YOUR FONTEND URL**'
else:
    FRONTEND_URL = 'http://127.0.0.1:8000/'


# [LOAD] UPLOAD FILE SIZE LIMIT SETTINGS
try:
    from .extra_settings.upload_file_size_limit_settings import *
except ImportError:
    pass

# [LOAD] UPLOAD IMAGE SIZE SETTINGS
try:
    from .extra_settings.upload_image_size_settings import *
except ImportError:
    pass

# [LOAD] SUMMERNOTE SETTINGS
try:
    from .extra_settings.summernote_settings import *
except ImportError:
    pass
if USE_DJANGO_TOOLBAR:
    try:
        from .extra_settings.django_toolbar_settings import *
    except ImportError:
        pass
