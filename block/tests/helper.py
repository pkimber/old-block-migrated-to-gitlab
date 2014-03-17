# -*- encoding: utf-8 -*-
from __future__ import unicode_literals


def check_content_methods(model_instance):
    """
    Call the standard methods used by the block content.  An exception will
    be thrown if the method is not defined
    """
    model_instance.url_publish()
    model_instance.url_remove()
    model_instance.url_update()
