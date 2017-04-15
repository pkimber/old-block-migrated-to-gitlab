# -*- encoding: utf-8 -*-
from block.models import Image
from celery import shared_task
from easy_thumbnails.files import generate_all_aliases


@shared_task
def thumbnail_image(image_pk):
    try:
        img = Image.objects.get(id=image_pk)
    except Image.DoesNotExist:
        img = None
    if img:
        generate_all_aliases(img.image, include_global=True)
