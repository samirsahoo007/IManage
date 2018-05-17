# Django settings imSupport project.
　
DEBUG = True
TEMPLATE_DEBUG = DEBUG
　
# sets PROJECT_ROOT as parent directory, since database is located at: ../data
import os
PROJECT_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
　
# if DJANGO_LOG_DIR not defined, sets e2/logs.
LOG_DIR = os.environ.get('DJANGO_LOG_DIR', os.path.join(PROJECT_ROOT,'logs'))
　
RUNAS = 'ihsadm'
E2OSROOT = PROJECT_ROOT
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
　
MANAGERS = ADMINS
　
DATABASES = {
   'default': {       # Oracle Database 11g Express
      'ENGINE': 'django.db.backends.oracle',
      'NAME': 'MyDBTEST',
      'USER': 'username1',
      'PASSWORD': 'password_2018',
      'HOST': 'myNewHost.com',
      'PORT': '20001',
   },
   'oracle11g': {       
      'ENGINE': 'django.db.backends.oracle',
      'NAME': 'USERNAMEONE',
      'USER': 'username1',
      'PASSWORD': 'passw0rd',
      'HOST': 'myNewHost.us.abcd',
      'PORT': '20001',
   },
}
　
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'
　
# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'
　
SITE_ID = 1
# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
　
# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True
　
# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True
　
# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''
　
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''
　
# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.samir.com/static/"
STATIC_ROOT = ''
　
# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'
　
# Additional locations of static files
　
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, "static"),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)
　
# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
　
LOGIN_URL = '/auth/'
SECRET_KEY = 'dfdsfds45432545@der(Mm,mn)@m,,nkjk#$213213dsfsdfd'
　
# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)
　
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
　
ROOT_URLCONF = 'imSupport.urls'
　
# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'imSupport.wsgi.application'
　
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'apps', 'esupport', 'templates'),
)
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    "imSupport.apps.esupport.helpers.views.user_context"
)
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'imSupport.apps.esupport',
    'imSupport.apps.esupport.appman',
    'guardian',
)
　
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
　
    'formatters': {
        'verbose': {
           'format': '%(levelname)s|%(asctime)s|%(module)s|%(process)d|%(thread)d|%(message)s',
           'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
　
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'logfile': {
           'level':'ERROR',
           'class':'logging.handlers.RotatingFileHandler',
           'filename': os.path.join(LOG_DIR, 'django.log'),
           'maxBytes': 1024*1024*1024, # 1G
           'backupCount': 5,
           'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['logfile'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}
　
#################################################################
#
# LDAP Authentication settings.
#
#################################################################
AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)
　
#Guardian Settings
ANONYMOUS_USER_ID = -1
GUARDIAN_RENDER_403 = True
GUARDIAN_TEMPLATE_403 = 'esupport/403.html'
　
　
#DEV
# The following are for DEV ADAM authentication.
#SSL
#AD_LDAP_URL='ldaps://gluetest.systems.mn.abcd:3269/'
#nonssl
LDAPSEARCH_SERVER_NAME = 'gluetest.systems.mn.abcd:3268'
LDAPSEARCH_BASE_DN = 'OU=abcdPeople,DC=InfoDir,DC=Dev,DC=abcd'
　
　
AD_BIND_DN = 'CN=InfoDir-ohb-nadmadmin,OU=Service Accounts,DC=InfoDir,DC=Dev,DC=abcd'
AD_BIND_PASS = 'dsfsd333gfhgfh'
　
#ldap backend settings
AUTH_LDAP_SERVER_URI = 'ldap://gluetest.systems.mn.abcd:3268/'
AUTH_LDAP_USER_DN_TEMPLATE = "CN=%(user)s,OU=abcdPeople,DC=InfoDir,DC=Dev,DC=abcd"
　
#AD_LDAP_URL = 'ldap://gluetest.systems.mn.abcd:3268/'
#AD_SEARCH_DN = 'OU=abcdPeople,DC=InfoDir,DC=Dev,DC=abcd'
#AD_BIND_PREFIX = 'CN='
#AD_BIND_SUFFIX = ',OU=abcdPeople,DC=InfoDir,DC=Dev,DC=abcd'
#AD_BIND_DN = 'CN=InfoDir-ohb-nadmadmin,OU=Service Accounts,DC=InfoDir,DC=Dev,DC=abcd'
#AD_BIND_PASS = 'dsfdsfdg'
　
#AD_BIND_DN = 'CN=user1,OU=abcdPeople,DC=InfoDir,DC=Dev,DC=abcd'
#AD_BIND_DN = 'CN=user2,OU=abcdPeople,DC=InfoDir,DC=Dev,DC=abcd'
　
#PROD
# The following are for Prod ADAM authentication.
#AD_LDAP_URL = 'ldaps://USINFODIR-VH.US.abcd:3269/'
#AD_SEARCH_DN = 'OU=abcdPeople,DC=InfoDir,DC=Prod,DC=abcd'
#AD_BIND_DN = 'CN=iwas61us,OU=HTSN WAS,OU=SysAdmin,DC=InfoDir,DC=Prod,DC=abcd'
#AD_BIND_PASS = 'p@ssw0rd'
　
　
AD_DEBUG = True
AD_DEBUG_FILE = os.path.join(LOG_DIR, 'ldap_debug.log')
AD_CERT_PATH = ''
　
　
#SESSION CACHE
　
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
　
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
　
################################################################
#DNA/EBI Team Members ID's need adding here for admin access
################################################################
　
ADMIN_ACCOUNTS = ['user1', 'user2', 'user3']
　
# Security Configuration
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
　
SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
　
