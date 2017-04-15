# -*- encoding: utf-8 -*-
import pytest

from block.models import ModerateState
from block.tests.factories import PageSectionFactory
from block.tests.helper import check_content
from login.tests.factories import UserFactory

from example_block.models import Title
from example_block.tests.factories import TitleBlockFactory, TitleFactory


@pytest.mark.django_db
def test_content_methods():
    c = TitleFactory()
    check_content(c)


@pytest.mark.django_db
def test_get_max_order():
    block = TitleBlockFactory()
    TitleFactory(block=block, order=4)
    assert 4 == Title.objects.get_max_order(block)


@pytest.mark.django_db
def test_get_max_order_empty():
    assert 0 == Title.objects.get_max_order(TitleBlockFactory())


@pytest.mark.django_db
def test_get_max_order_ignore_removed():
    block = TitleBlockFactory()
    TitleFactory(block=block, order=2)
    TitleFactory(
        block=block,
        order=5,
        moderate_state=ModerateState.objects._removed(),
    )
    assert 2 == Title.objects.get_max_order(block)


@pytest.mark.django_db
def test_order_move():
    page_section = PageSectionFactory()
    b1 = TitleBlockFactory(page_section=page_section)
    t1 = TitleFactory(block=b1, order=3)
    b2 = TitleBlockFactory(page_section=page_section)
    t2 = TitleFactory(block=b2, order=5)
    b3 = TitleBlockFactory(page_section=page_section)
    t3 = TitleFactory(block=b3, order=6)
    # test
    Title.objects.order_move(t1, 5)
    # check
    t1.refresh_from_db()
    assert 5 == t1.order
    t2.refresh_from_db()
    assert 4 == t2.order
    t3.refresh_from_db()
    assert 6 == t3.order


@pytest.mark.django_db
def test_order_vacate():
    page_section = PageSectionFactory()
    b1 = TitleBlockFactory(page_section=page_section)
    t1 = TitleFactory(block=b1, order=3)
    b2 = TitleBlockFactory(page_section=page_section)
    t2 = TitleFactory(block=b2, order=5)
    b3 = TitleBlockFactory(page_section=page_section)
    t3 = TitleFactory(block=b3, order=6)
    # test
    Title.objects.order_vacate(t1)
    # check
    t1.refresh_from_db()
    assert 3 == t1.order
    t2.refresh_from_db()
    assert 4 == t2.order
    t3.refresh_from_db()
    assert 5 == t3.order


@pytest.mark.django_db
def test_pending_order():
    """Pending items should be in 'order' order."""
    page_section = PageSectionFactory()
    # block 1
    block_1 = TitleBlockFactory(page_section=page_section)
    TitleFactory(block=block_1, title='ABC', order=5)
    # block 2 (publish)
    block_2 = TitleBlockFactory(page_section=page_section)
    TitleFactory(block=block_2, title='LMN', order=3)
    block_2.publish(UserFactory())
    # block 3 (publish)
    block_3 = TitleBlockFactory(page_section=page_section)
    TitleFactory(block=block_3, title='XYZ', order=1)
    # check order
    assert ['XYZ', 'LMN', 'ABC'] == [
        t.title for t in Title.objects.pending(page_section)
    ]


@pytest.mark.django_db
def test_published_order():
    """Published items should be in 'order' order."""
    page_section = PageSectionFactory()
    # publish block 1
    block_1 = TitleBlockFactory(page_section=page_section)
    TitleFactory(block=block_1, title='ABC', order=9)
    block_1.publish(UserFactory())
    # publish block 2
    block_2 = TitleBlockFactory(page_section=page_section)
    TitleFactory(block=block_2, title='XYZ', order=8)
    block_2.publish(UserFactory())
    # check order
    assert ['XYZ', 'ABC'] == [
        t.title for t in Title.objects.published(page_section)
    ]
