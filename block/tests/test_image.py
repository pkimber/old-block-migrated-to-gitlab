# -*- encoding: utf-8 -*-
import pytest

from block.tests.factories import ImageFactory


@pytest.mark.django_db
def test_image_factory():
    ImageFactory()


@pytest.mark.django_db
def test_image_str():
    str(ImageFactory())
