import os

from reistijdenauto.settings_common import * # noqa F403
from reistijdenauto.settings_common import INSTALLED_APPS, DEBUG # noqa F401
from reistijdenauto.settings_databases import LocationKey,\
    get_docker_host,\
    get_database_key,\
    OVERRIDE_HOST_ENV_VAR,\
    OVERRIDE_PORT_ENV_VAR

INSTALLED_APPS += [
    'dataset',
    'rest_framework_swagger',
]

ROOT_URLCONF = 'reistijdenauto.urls'


WSGI_APPLICATION = 'reistijdenauto.wsgi.application'


DATABASE_OPTIONS = {
    LocationKey.docker: {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DATABASE_NAME', 'reistijdenauto'),
        'USER': os.getenv('DATABASE_USER', 'reistijdenauto'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'insecure'),
        'HOST': 'database',
        'PORT': '5432'
    },
    LocationKey.local: {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DATABASE_NAME', 'reistijdenauto'),
        'USER': os.getenv('DATABASE_USER', 'reistijdenauto'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'insecure'),
        'HOST': get_docker_host(),
        'PORT': '5412'
    },
    LocationKey.override: {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DATABASE_NAME', 'reistijdenauto'),
        'USER': os.getenv('DATABASE_USER', 'reistijdenauto'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'insecure'),
        'HOST': os.getenv(OVERRIDE_HOST_ENV_VAR),
        'PORT': os.getenv(OVERRIDE_PORT_ENV_VAR, '5432')
    },
}

DATABASES = {
    'default': DATABASE_OPTIONS[get_database_key()]
}

# Directory for raw test data:
TESTDATA_DIR = os.path.join(BASE_DIR, 'test_data') # noqa F405
