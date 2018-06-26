import pytest
from django.forms import model_to_dict
from tests.factories import AuthorFactory, BookFactory, UserFactory

from unicef_snapshot import utils

pytestmark = pytest.mark.django_db


def test_jsonify():
    author = AuthorFactory()
    j = utils.jsonify(model_to_dict(author))
    assert j["name"] == author.name


def test_jsonify_unicode():
    author = AuthorFactory(name=u'R\xe4dda')
    j = utils.jsonify(model_to_dict(author))
    assert j["name"] == author.name


def test_many_to_one_fields():
    author = AuthorFactory()
    fields = utils.get_to_many_field_names(author.__class__)
    # check many_to_one field
    assert "books" in fields


def test_many_to_many_fields():
    book = BookFactory()
    fields = utils.get_to_many_field_names(book.__class__)
    # check many_to_many field
    assert "tags" in fields


def test_no_relation():
    author = AuthorFactory()
    obj_dict = utils.create_dict_with_relations(author)
    assert obj_dict["books"] == []


def test_relation():
    author = AuthorFactory()
    book = BookFactory(author=author)
    obj_dict = utils.create_dict_with_relations(author)
    assert obj_dict["books"] == [book.pk]


def test_obj_none():
    obj_dict = utils.create_dict_with_relations(None)
    assert obj_dict == {}


def test_no_prev_dict():
    assert utils.create_change_dict(None, {"key": "value"}) == {}


def test_change():
    before = {"test": "unknown"}
    after = {"test": "known"}
    change = utils.create_change_dict(before, after)
    assert change == {
        "test": {
            "before": "unknown",
            "after": "known"
        }
    }


def test_create():
    user = UserFactory()
    author = AuthorFactory()
    activity = utils.create_snapshot(author, {}, user)
    assert activity.target == author
    assert activity.action == activity.CREATE
    assert activity.by_user == user
    assert activity.data["name"] == author.name
    assert activity.change == {}


def test_update():
    user = UserFactory()
    author = AuthorFactory()
    obj_dict = utils.create_dict_with_relations(author)
    book = BookFactory(author=author)
    activity = utils.create_snapshot(author, obj_dict, user)
    assert activity.target == author
    assert activity.action == activity.UPDATE
    assert activity.by_user == user
    assert activity.data["name"] == author.name
    assert activity.change == {
        "books": {
            "before": [],
            "after": [book.pk]
        }
    }
    assert activity.get_action_display() == "Changed books"
