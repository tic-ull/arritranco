# Django settings for arritranco project.

import os

PROJECT_ROOT = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
#PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

# Celery settings

BROKER_URL = 'amqp://localhost//'

# INVENTORY/CHECKER settings

CHECKER = 'localhost'
INVENTORY = 'http://localhost'
BACKUP_QUEUENAME = 'inventario'
BACKUP_URLBASE = INVENTORY +'/rest/backup/backupfilechecker/?checker=' + CHECKER
BACKUP_URLCOMPRESS = INVENTORY + '/rest/backup/addCompressedBackupFile?checker=' + CHECKER + '&'
BACKUP_FILE_INFO_URL = INVENTORY + '/rest/backup/backupFileInfo'
BACKUP_UPDATE_STATUS_URL = INVENTORY + '/rest/scheduler/tasks/%s/status'
BACKUP_URLDELETE = INVENTORY + '/rest/backup/filesToDelete?checker=' + CHECKER + '&format=json'

#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)
# time to wait to delete the backup deleted files in de data base in days
BACKUP_FILE_TIME_TO_DELETE = 300
DEFAULT_SVC_IFACE_NAME = 'service'
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        #'django.db.backends.sqlite3',           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',  # Or path to database file if using sqlite3.
        'USER': '',  # Not used with sqlite3.
        'PASSWORD': '',  # Not used with sqlite3.
        'HOST': '',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',  # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Atlantic/Canary'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Static media lives
STATIC_URL = '/static/'

# Static filesystem path
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'deployed-static')

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'arritranco-static'),
)


# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = PROJECT_ROOT + '/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '9u)uyfcmr*p9m6d=km@r@(0bzvoi*nt^_9*yy)-h)+-o&$6z=5'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.load_template_source',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'arritranco.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_ROOT + '/templates',
)

NAGIOS_SERVER_IP = "127.0.0.1"

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.messages',
    'django_extensions',
    'south',
    'rest_framework',
    'monitoring.nagios',
    'monitoring.cacti',
    'monitoring',
    'location',
    'hardware',
    'scheduler',
    'inventory',
    'hardware_model',
    'network',
    'backups',
    'monitoring.sondas',
    'security',
    'fabric',
    'celery',
    'arritranco',
)

ADMIN_REORDER = (
    ('scheduler', ""),
    ('backups', ""),
    ('nagios', ""),
    ('inventory', ""),
    ('location', ""),
    ('hardware', ""),
    ('hardware_model', ""),
    ('network', ""),
    ('sondas', ""),
    ('security', ""),
    ('auth', ""),
)

AREA_CHOICES = [[1, 'La Laguna'],
                [2, 'Santa Cruz'],
]

INTERNAL_IPS = ('127.0.0.1',)

FILE_BACKUP_CHECKERS = (
    ('bckpsrv01.example.com', 'backup server1'),
    ('bckpsrv02.example.com', 'backup server2'),
    ('bckpsrv03.example.com', 'backup server3'),
    ('bckpsrv04.example.com', 'backup server4'),
)

# If None or False no default parent will set.
DEFAULT_NAGIOS_HOST_PARENT = None
DEFAULT_NAGIOS_CG = 'Sistemas'
PROPAGATE_STATUS_TO_NAGIOS = False
SEND_NSCA_BIN = '/usr/sbin/send_nsca'
NSCA_DAEMON_HOSTNAME = 'nagios.fully.qualified.domain.name'
SEND_NSCA_CFG = '/etc/send_nsca.cfg'

# Logging configuration
LOG_FILENAME = os.path.join(PROJECT_ROOT, 'logs/arritranco.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'fichero_rotado': {
            'level': 'DEBUG',
            'class': 'logging.handlers.WatchedFileHandler',
            'formatter': 'verbose',
            'filename': LOG_FILENAME,
        },

    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        '': {  # catch_all logger
               'handlers': ['fichero_rotado', ],
               'level': 'DEBUG',
               'propagate': True,
        },
    }
}

UPS_ROOM_NAMES = ('cpd',)

MAX_COMPRESS_GB = 400

PX_FOR_UNITS = 15

# Network settings
SWITCH_LEVEL_SNMP_COMMUNITY_1 = ''
BACKUP_METHOD_SFTP_USER = ''
BACKUP_METHOD_SFTP_PASSWORD = ''

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.XMLRenderer',
        'rest_framework.renderers.YAMLRenderer',
    )
}

try:
    from arritranco.settings_local import *
except ImportError:
    pass
