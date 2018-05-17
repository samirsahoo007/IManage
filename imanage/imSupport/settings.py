# Django settings for imSupport project.
　
DEBUG = True
TEMPLATE_DEBUG = True
　
import os
　
from os.path import abspath, dirname, join, normpath
　
from imSupport.libs import helpers
　
########## PATH CONFIGURATION
# Absolute filesystem path to this Django project directory.
# dirname(dirname()) is similar to '../..'
PROJECT_ROOT = dirname(dirname(dirname(abspath(__file__))))
　
# if DJANGO_LOG_DIR not defined, sets imanage/logs.
LOG_DIR = os.environ.get('DJANGO_LOG_DIR', join(PROJECT_ROOT,'logs'))
　
# Absolute filesystem path to the secret file which holds this project's
# SECRET_KEY. Will be auto-generated the first time this file is interpreted.
SECRET_FILE = normpath(join(PROJECT_ROOT, 'deploy', 'secretwsgi.txt'))
　
# Try to load the SECRET_KEY from our SECRET_FILE. If that fails, then generate
# a random SECRET_KEY and save it into our SECRET_FILE for future loading. If
# everything fails, then just raise an exception.
try:
    SECRET_KEY = open(SECRET_FILE).read().strip()
except IOError:
    try:
        with open(SECRET_FILE, 'w') as f:
            f.write(helpers.gen_secret_key(50))
            os.chmod(SECRET_FILE, 0400)   # Read only.
            SECRET_KEY = open(SECRET_FILE).read().strip()
    except IOError:
        raise Exception('Cannot open file `%s` for writing.' % SECRET_FILE)
########## END KEY CONFIGURATION
　
RUNAS = 'root'
imanageOSROOT = join(PROJECT_ROOT, 'imanage')
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS
　
DATABASES = {
   #'mysql': {       # Local MySQL db
   'default': {       # Local MySQL db
      'ENGINE': 'django.db.backends.mysql',
      'NAME': 'XE',
      'USER': 'root',
      'PASSWORD': 'root123',
      'HOST': 'localhost',
      'PORT': '3306',
   },
   'oracle_prod': {       # Oracle Database 11g Express
   #'default': {       # Oracle Database 11g Express
      'ENGINE': 'django.db.backends.oracle',
      'NAME': 'XE',
      'USER': 'consracp',
      'PASSWORD': 'ERiDfjhPvR8Xqwp',
      'HOST': 'usvhipe1csmecm01.us.abcd',
      'PORT': '20001',
   },
   'oracle11g': {       # Oracle Database 11g setup by DBAs for dev msupport. GSR-3486004
      'ENGINE': 'django.db.backends.oracle',
      'NAME': 'XXXXXXXXXX',
      'USER': 'msupport',
      'PASSWORD': 'XXXXXXXXXX',
      'HOST': 'oraconsdv-scan.us.abcd',
      'PORT': '20001',
   },
   'itm': {       # Oracle Database 11g Express
      'ENGINE': 'django.db.backends.oracle',
      'NAME': 'DITM02',
      'USER': 'ITM_RO',
      'PASSWORD': 'g00dn1ght',
      'HOST': 'gbl04931.systems.uk.abcd',
      'PORT': '1542',
   },
   'OPTIONS': {
           'threaded': True,
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
# Example: "/home/media/media.lawrence.com/static/"
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
　
# Make this unique, and don't share it with anybody.
#SECRET_KEY = 'r)ogk$-i!+x)jk9pawbeh_qyyeuj@ap^a%i9+r28qb3rl_$nwc'
　
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
    os.path.join(PROJECT_ROOT, 'apps', 'msupport', 'templates'),
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
    "imSupport.apps.msupport.helpers.views.user_context"
)
INSTALLED_APPS = (
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'imSupport.apps.msupport',
    'imSupport.apps.msupport.appman',
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
           'format': '%(levelname)s|%(asctime)s|%(module)s[%(pathname)s:%(lineno)s]|%(process)d|%(thread)d|%(message)s',
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
           'level':'INFO',
           'class':'logging.handlers.RotatingFileHandler',
           'filename': os.path.join(LOG_DIR, 'django_wsgi.log'),
           'maxBytes': 1024*1024*1024, # 1G
           'backupCount': 5,
           'formatter': 'verbose',
        },
    },
    'loggers': {
        'others': {
            'handlers': ['console', 'logfile'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['logfile'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}
'''
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'imanage_debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
'''
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
GUARDIAN_TEMPLATE_403 = 'msupport/403.html'
'''
#DEV
# The following are for DEV ADAM authentication.
#SSL
#AD_LDAP_URL='ldaps://gluetest.systems.mn.abcd:3269/'
#nonssl
###################### Dev ADAM settings ####################
LDAPSEARCH_SERVER_NAME = 'gluetest.systems.mn.abcd:3268'
LDAPSEARCH_BASE_DN = 'OU=abcdPeople,DC=InfoDir,DC=Dev,DC=abcd'
AD_BIND_DN = 'CN=InfoDir-ohb-nadmadmin,OU=Service Accounts,DC=InfoDir,DC=Dev,DC=abcd'
AD_BIND_PASS = 'SXv8c31C'
　
#ldap backend settings
AUTH_LDAP_SERVER_URI = 'ldap://gluetest.systems.mn.abcd:3268/'
AUTH_LDAP_USER_DN_TEMPLATE = "CN=%(user)s,OU=abcdPeople,DC=InfoDir,DC=Dev,DC=abcd"
##################End Dev ADAM settings #####################
#PROD
###################### Prod ADAM settings ####################
# The following are for Prod ADAM authentication.
# AD_LDAP_URL = 'ldaps://USINFODIR-VH.US.abcd:3269/'
AD_SEARCH_DN = 'OU=abcdPeople,DC=InfoDir,DC=Prod,DC=abcd'
AD_BIND_DN = 'CN=iwas61us,OU=HTSN WAS,OU=SysAdmin,DC=InfoDir,DC=Prod,DC=abcd'
AD_BIND_PASS = 'w@s@dm1n'
AUTH_LDAP_SERVER_URI = 'ldaps://USINFODIR-VH.US.abcd:3269/'
AUTH_LDAP_USER_DN_TEMPLATE = "CN=%(user)s,OU=abcdPeople,DC=InfoDir,DC=Prod,DC=abcd"
LDAPSEARCH_BASE_DN = 'OU=abcdPeople,DC=InfoDir,DC=Prod,DC=abcd'
##################End Dev ADAM settings #####################
'''
############################My(Samir's) Test LDAP Server ####################
import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType
　
# Baseline configuration.
AUTH_LDAP_SERVER_URI = "ldap://mnl107171.mn.abcd:389"
AD_BIND_DN = 'cn=Manager,dc=mn,dc=abcd'
AD_BIND_PASS = 'P@ssword01'
LDAPSEARCH_BASE_DN = 'OU=People,DC=mn,DC=abcd'
AUTH_LDAP_BIND_DN = "cn=Manager,dc=mn,dc=abcd"
AUTH_LDAP_BIND_PASSWORD = "P@ssword01"
AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=People,dc=mn,dc=abcd",
    ldap.SCOPE_SUBTREE, "(cn=%(user)s)")
　
################## End of Dev ADAM settings #####################
　
AD_DEBUG = True
AD_DEBUG_FILE = os.path.join(LOG_DIR, 'ldap_debug.log')
AD_CERT_PATH = ''
　
#SESSION CACHE
　
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
　
#SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_ENGINE = 'redis_sessions.session'
#SESSION_REDIS_UNIX_DOMAIN_SOCKET_PATH = '/spare/imanage/redis/redis.sock'
SESSION_REDIS_UNIX_DOMAIN_SOCKET_PATH = '/tmp/redis.sock'
　
################################################################
#DNA/EBI Team Members ID's need adding here for admin access
################################################################
　
ADMIN_ACCOUNTS = ['username1', 'username2', 'username3', ]
　
USRRBSCRPT = 'rollback_ldapV2.pl '
　
USRRB_OUTFILE_LOC = '/appvol/DJANGO/certtool/logs/usrrb/tickets'
　
###########################
###########################
　
# Variables for SSL cert renewal tool
　
CRSCRPTHOME = '/spare/iManage/imanage/scripts'
　
CRTMGMTHOME = '/appvol/DJANGO/certtool'
　
CRSCRPT = 'runSSLTool.ksh'
　
# Variables for SSL cert renewal tool
　
# Security Configuration
#SESSION_COOKIE_SECURE = True
#CSRF_COOKIE_SECURE = True
　
SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
　
ALLOWED_HOSTS = ['hostname1', 'hostname2',  'hostname3', 'mnl106757.mn.abcd']
　
# Cloud registration origination IP
　
ALLOWED_IP = ['1.4.5.7', '13.4.5.8', '161.1.1.8']
　
　
###########################
　
# CELERY SETTINGS
　
BROKER_URL = 'redis://localhost:6379/0'
#BROKER_URL = 'redis://mnl105712.mn.abcd:6379/0'
　
CELERY_ACCEPT_CONTENT = ['json']
　
CELERY_TASK_SERIALIZER = 'json'
　
CELERY_RESULT_SERIALIZER = 'json'
　
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
#CELERY_RESULT_BACKEND = 'redis://mnl105712.mn.abcd:6379/0'
　
BULK_DATA = '/spare/iManage/imanage/bulk_load/data.txt'
HOST_FILE = '/spare/iManage/imanage/scripts/hosts.txt'
MOTD_FILE = '/spare/iManage/imanage/motd.txt'
　
