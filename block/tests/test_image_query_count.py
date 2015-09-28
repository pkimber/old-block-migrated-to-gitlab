# -*- encoding: utf-8 -*-
from django.test import TestCase

from block.models import Image
from block.tests.factories import ImageFactory


class TestImageQueryCount(TestCase):

    def test_image_query_count(self):
        ImageFactory()
        ImageFactory()
        ImageFactory()
        result = []
        with self.assertNumQueries(1):
            for item in Image.objects.images():
                result.append(str(item.image))
        assert 3 == len(result)
