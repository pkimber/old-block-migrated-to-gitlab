# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.db import IntegrityError

from block.models import BlockError


def check_content_methods(model_instance, ignore_remove=None):
    """Call the standard methods used by the block content.

    An exception will be thrown if the method is not defined
    """
    # check the standard URLs
    model_instance.url_publish()
    if ignore_remove:
        if hasattr(model_instance, 'url_remove'):
            raise BlockError(
                "The content model has the 'url_remove' method, but "
                "you have chosen not to test it (see 'ignore_remove' "
                "in 'check_content_methods')"
            )
    else:
        model_instance.url_remove()
    model_instance.url_update()
    # check the 'content' set
    try:
        model_instance.block.content.all()
    except AttributeError:
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
    # check the order field
    try:
        model_instance.order
    except AttributeError:
        raise BlockError(
            "The {} model does not have an 'order' field"
            "".format(model_instance.__class__)
        )
