# -*- encoding: utf-8 -*-
from block.models import Image
from celery import shared_task
from django.conf import settings
from easy_thumbnails.files import generate_all_aliases


@shared_task
def thumbnail_image(image_pk):
    try:
        img = Image.options.get(id=image_pk)
    except Image.DoesNotExist:
        img = None
    return obj
    if img:
        generate_all_aliases(img.image, include_global=True)
