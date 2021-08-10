import pytest
from unittest.mock import Mock

from unicef_snapshot.admin import ActivityAdmin
from unicef_snapshot.models import Activity

from demo.sample.admin import AuthorAdmin
from demo.sample.models import Author

pytestmark = pytest.mark.django_db


def test_admin_str(admin_site):
    aa = AuthorAdmin(Author, admin_site)
    assert str(aa) == 'sample.AuthorAdmin'


def test_admin_has_add_permission(admin_site):
    aa = AuthorAdmin(Author, admin_site)
    activity_admin = aa.inlines[0](Author, admin_site)
    assert activity_admin.has_add_permission(request=None) is False
    main_activity_admin = ActivityAdmin(Activity, admin_site)
    assert main_activity_admin.has_add_permission(request=None) is False


def test_admin_save_update(admin_site, author, user):
    mock_request = Mock()
    mock_request.user = user
    aa = AuthorAdmin(Author, admin_site)
    form = aa.get_form(mock_request)()
    author.name = "Changed"
    change = {"name": "Changed"}

    activity_qs = Activity.objects.filter(
        target_object_id=author.pk,
        action=Activity.UPDATE
    )
    assert activity_qs.exists() is False
    aa.save_model(mock_request, author, form, change)
    assert activity_qs.exists() is True


def test_admin_save_obj_create(admin_site, author, user):
    mock_request = Mock()
    mock_request.user = user
    aa = AuthorAdmin(Author, admin_site)
    form = aa.get_form(mock_request)()
    author.pk = None
    change = {}

    activity_qs = Activity.objects.filter(
        action=Activity.CREATE
    )
    assert activity_qs.exists() is False
    aa.save_model(mock_request, author, form, change)
    assert activity_qs.exists() is True
