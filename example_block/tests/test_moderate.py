# -*- encoding: utf-8 -*-
import pytest

from django.db import IntegrityError
from django.test import TestCase

from block.models import (
    BlockError,
    ModerateState,
)
from block.tests.factories import (
    ImageFactory,
    PageSectionFactory,
)
from login.tests.factories import UserFactory

from example_block.models import Title
from example_block.tests.factories import (
    TitleBlockFactory,
    TitleImageFactory,
    TitleFactory,
)


@pytest.mark.django_db
def test_is_pending():
    block = TitleBlockFactory()
    content = TitleFactory(block=block)
    assert content.is_pending is True


@pytest.mark.django_db
def test_is_published():
    """Slightly strange test I think.  Not sure what it is doing."""
    block = TitleBlockFactory()
    content = TitleFactory(block=block)
    # publish the content
    block.publish(UserFactory())
    # get the pending content
    c = block.get_pending()
    # update the pending content
    c.title = 'Hatherleigh Three'
    c.save()
    # check the original content was published
    content = Title.objects.get(title=content.title)
    assert content.is_published is True


@pytest.mark.django_db
def test_is_removed():
    block = TitleBlockFactory()
    content = TitleFactory(block=block)
    block.remove(UserFactory())
    content = Title.objects.get(title=content.title)
    assert content.is_removed is True


@pytest.mark.django_db
def test_two_pending_error():
    block = TitleBlockFactory()
    TitleFactory(block=block)
    with pytest.raises(IntegrityError) as e:
        TitleFactory(
            block=block,
            moderate_state=ModerateState.objects._pending(),
        )
    assert 'UNIQUE constraint failed' in str(e.value)


@pytest.mark.django_db
def test_published():
    page_section = PageSectionFactory()
    # block_1
    block_1 = TitleBlockFactory(page_section=page_section)
    TitleFactory(block=block_1, title='content_1')
    block_1.publish(UserFactory())
    # block_2
    block_2 = TitleBlockFactory(page_section=page_section)
    TitleFactory(block=block_2, title='content_2')
    block_2.publish(UserFactory())
    # check the content is published
    result = [
        c.title for c in Title.objects.published(page_section)
    ]
    assert ['content_1', 'content_2'] == result


@pytest.mark.django_db
def test_pending():
    page_section = PageSectionFactory()
    # block_1
    block_1 = TitleBlockFactory(page_section=page_section)
    TitleFactory(block=block_1, title='content_1')
    # block_2
    block_2 = TitleBlockFactory(page_section=page_section)
    TitleFactory(block=block_2, title='content_2')
    # check the content is pending
    result = [
        c.title for c in Title.objects.pending(page_section)
    ]
    assert ['content_1', 'content_2'] == result


@pytest.mark.django_db
def test_publish():
    page_section = PageSectionFactory()
    block = TitleBlockFactory(page_section=page_section)
    title = TitleFactory(
        block=block,
        title='content_1'
    )
    TitleImageFactory(content=title, image=ImageFactory(), order=1)
    TitleImageFactory(content=title, image=ImageFactory(), order=2)
    # check the content is pending
    assert [
        'content_1'
    ] == [c.title for c in Title.objects.pending(page_section)]
    # check the content is not published
    assert [] == [c.title for c in Title.objects.published(page_section)]
    # publish the content
    block.publish(UserFactory())
    # check the content is published
    published = Title.objects.published(page_section)
    assert ['content_1'] == [c.title for c in published]
    assert 1 == len(published)
    obj = published[0]
    assert 'content_1' == obj.title


@pytest.mark.django_db
def test_remove_already():
    """content has already been removed and cannot be removed again."""
    block = TitleBlockFactory()
    TitleFactory(block=block)
    block.remove(UserFactory())
    with pytest.raises(BlockError) as e:
        block.remove(UserFactory())
    assert 'Cannot find pending or published content to remove' in str(e.value)


@pytest.mark.django_db
def test_remove_pending():
    """remove pending content."""
    page_section = PageSectionFactory()
    # block_1
    block_1 = TitleBlockFactory(page_section=page_section)
    TitleFactory(block=block_1, title='content_1')
    # block_2
    block_2 = TitleBlockFactory(page_section=page_section)
    TitleFactory(block=block_2, title='content_2')
    # check pending
    assert [
        'content_1', 'content_2'
    ] == [c.title for c in Title.objects.pending(page_section)]
    # remove block 1
    block_1.remove(UserFactory())
    # check removed
    assert [
        'content_2'
    ] == [c.title for c in Title.objects.pending(page_section)]


@pytest.mark.django_db
def test_remove_published():
    """remove published content."""
    page_section = PageSectionFactory()
    # block_1
    block_1 = TitleBlockFactory(page_section=page_section)
    TitleFactory(block=block_1, title='content_1')
    block_1.publish(UserFactory())
    # block_2
    block_2 = TitleBlockFactory(page_section=page_section)
    TitleFactory(block=block_2, title='content_2')
    block_2.publish(UserFactory())
    # block_3 (not published)
    block_3 = TitleBlockFactory(page_section=page_section)
    TitleFactory(block=block_3, title='content_3')
    # check published
    assert [
        'content_1', 'content_2'
    ] == [c.title for c in Title.objects.published(page_section)]
    # remove block
    block_2.remove(UserFactory())
    # check removed
    assert [
        'content_1'
    ] == [c.title for c in Title.objects.published(page_section)]


@pytest.mark.django_db
def test_edit_published():
    """edit published content."""
    page_section = PageSectionFactory()
    # block_1
    block_1 = TitleBlockFactory(page_section=page_section)
    TitleFactory(block=block_1, title='content_1')
    block_1.publish(UserFactory())
    # block_2
    block_2 = TitleBlockFactory(page_section=page_section)
    content_2 = TitleFactory(block=block_2, title='content_2')
    block_2.publish(UserFactory())
    # check pending
    assert [
        'content_1', 'content_2'
    ] == [c.title for c in Title.objects.pending(page_section)]
    # check published
    assert [
        'content_1', 'content_2'
    ] == [c.title for c in Title.objects.published(page_section)]
    # edit content
    content_2.title = 'content_2_edit'
    content_2.save()
    # check pending
    assert [
        'content_1', 'content_2_edit'
    ] == [c.title for c in Title.objects.pending(page_section)]
    # check published
    assert [
        'content_1', 'content_2'
    ] == [c.title for c in Title.objects.published(page_section)]
