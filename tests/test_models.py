import pytest
from unicef_snapshot.models import Activity
from tests.factories import ActivityFactory, AuthorFactory, UserFactory

pytestmark = pytest.mark.django_db


def test_str():
    user = UserFactory()
    author = AuthorFactory()
    activity = ActivityFactory(
        target=author,
        action=Activity.CREATE,
        by_user=user
    )
    assert str(activity) == "{} {} {}".format(user, Activity.CREATE, author)


def test_by_user_display_empty():
    user = UserFactory()
    activity = ActivityFactory(by_user=user)
    user.username = ""
    assert str(user) == ""
    assert activity.by_user_display() == user.email


def test_by_user_display():
    user = UserFactory()
    activity = ActivityFactory(by_user=user)
    assert str(user) == user.username
    assert activity.by_user_display() == user.username


def test_delete_target():
    author = AuthorFactory()
    activity = ActivityFactory(target=author)
    assert activity.target == author
    author.delete()
    assert Activity.objects.filter(pk=activity.pk).exists() is True
    activity_updated = Activity.objects.get(pk=activity.pk)
    assert activity_updated.target_content_type == activity.target_content_type
    assert activity_updated.target_object_id == str(activity.target_object_id)
    assert activity_updated.target is None


def test_get_action_display_create():
    activity = ActivityFactory(action=Activity.CREATE)
    assert activity.get_action_display() == "Created"


def test_get_action_display_update_no_change_value():
    author = AuthorFactory()
    activity = ActivityFactory(target=author, action=Activity.UPDATE)
    assert activity.get_action_display() == "Changed unknown"


def test_get_action_display_update_many_field():
    author = AuthorFactory()
    activity = ActivityFactory(
        target=author,
        action=Activity.UPDATE,
        change={"books": ""}
    )
    assert activity.get_action_display() == "Changed books"


def test_get_action_display_update_invalid_field():
    author = AuthorFactory()
    activity = ActivityFactory(
        target=author,
        action=Activity.UPDATE,
        change={"wrong": ""}
    )
    assert activity.get_action_display() == "Changed "


def test_get_action_display_update():
    author = AuthorFactory()
    activity = ActivityFactory(
        target=author,
        action=Activity.UPDATE,
        change={"name": ""}
    )
    assert activity.get_action_display() == "Changed name"
