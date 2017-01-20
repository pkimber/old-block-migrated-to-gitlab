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
MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INSTALLED_APPS += (
    # 'django.contrib.formtools',
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

