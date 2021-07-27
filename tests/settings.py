import django.db.models.options as options

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ("lookup_fields", "lookup_by_model")

SECRET_KEY = 'secret'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'rest_framework',
    'tests'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test',
    }
}

ROOT_URLCONF = 'tests.urls'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
