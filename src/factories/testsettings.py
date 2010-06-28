# Minimum settings used for testing.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'factory_test.db',
    },
}

INSTALLED_APPS = ['factories', 'django.contrib.flatpages']
