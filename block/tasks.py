# -*- encoding: utf-8 -*-
from celery import shared_task


@shared_task
def thumbnail_image(image_pk):
    print(image_pk)
