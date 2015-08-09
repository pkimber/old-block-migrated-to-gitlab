# -*- encoding: utf-8 -*-
import pytest

from block.tests.factories import DocumentFactory


@pytest.mark.django_db
def test_document_factory():
    DocumentFactory()


@pytest.mark.django_db
def test_document_str():
    str(DocumentFactory())
