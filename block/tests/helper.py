# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.db import IntegrityError

from block.models import BlockError


def check_content_methods(model_instance):
    """Call the standard methods used by the block content.

    An exception will be thrown if the method is not defined
    """
    model_instance.url_publish()
    model_instance.url_remove()
    model_instance.url_update()
    # check the 'content' set
    try:
        model_instance.block.content.all()
    except AttributeError as e:
        raise BlockError(
            "The 'block' field in the content model does not have "
            "a 'related_name' (should be set to 'content')"
        )
    # check the string method
    str(model_instance)
    # check the unique together constraint
    try:
        model_instance.pk = 0
        model_instance.save()
        raise BlockError(
            "Missing 'unique_together' on {} ("
            "unique_together = ('block', 'moderate_state'))"
            "".format(model_instance.__class__)
        )
    except IntegrityError:
        pass
