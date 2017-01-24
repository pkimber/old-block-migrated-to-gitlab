# -*- encoding: utf-8 -*-
from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'temp.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

if DEBUG:
    # weird errors with running py test 
    # a) it runs with the settings profile example_block/dev_malcolm
    #    not example_block/dev_test.py
    # b) DEBUG is True here but in example_block/urls.py it is False
    # this variable fixes that
    ALLOW_DEBUG_TOOLBAR=True
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    INSTALLED_APPS += (
        # 'django.contrib.formtools',
        'debug_toolbar',
        'django_extensions',
    )

    #force the debug toolbar to be displayed
    def show_toolbar(request):
        return True

    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK" : show_toolbar,
    }


    import socket

    ALLOWED_HOSTS = [
        '127.0.0.1',
        '127.0.1.1',
        'localhost',
        socket.gethostbyname(socket.gethostname())
    ]
