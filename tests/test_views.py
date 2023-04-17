import datetime
import json

from django.urls import reverse
from django.utils import timezone
from rest_framework import status

import pytest

from tests.factories import ActivityFactory, UserFactory
from unicef_snapshot.models import Activity

pytestmark = pytest.mark.django_db
tz = timezone.get_default_timezone()


def assert_data(activity, response):
    assert response["id"] == activity.pk
    assert response["by_user"] == activity.by_user.pk
    assert response["action"] == activity.action
    assert response["data"] == activity.data
    assert response["change"] == activity.change


def test_empty(api_client):
    response = api_client.get(reverse("snapshot:activity-list"))
    assert response.status_code == status.HTTP_200_OK
    response_json = json.loads(response.rendered_content)
    assert response_json == []


def test_list(api_client):
    activity = ActivityFactory()
    response = api_client.get(reverse("snapshot:activity-list"))
    assert response.status_code == status.HTTP_200_OK
    response_json = json.loads(response.rendered_content)
    assert len(response_json) == 1
    assert_data(activity, response_json[0])


def test_filter_user(api_client):
    ActivityFactory(action=Activity.CREATE)
    activity = ActivityFactory(action=Activity.UPDATE)
    response = api_client.get(
        reverse("snapshot:activity-list"), data={"user": activity.by_user.email}
    )
    assert response.status_code == status.HTTP_200_OK
    response_json = json.loads(response.rendered_content)
    assert len(response_json) == 1
    assert_data(activity, response_json[0])


def test_filter_target(api_client):
    user = UserFactory()
    ActivityFactory(action=Activity.CREATE)
    activity = ActivityFactory(action=Activity.UPDATE, target=user)
    response = api_client.get(
        reverse("snapshot:activity-list"), data={"target": user.__class__.__name__}
    )
    assert response.status_code == status.HTTP_200_OK
    response_json = json.loads(response.rendered_content)
    assert len(response_json) == 1
    assert_data(activity, response_json[0])


def test_filter_action(api_client):
    ActivityFactory(action=Activity.CREATE)
    activity = ActivityFactory(action=Activity.UPDATE)
    response = api_client.get(
        reverse("snapshot:activity-list"), data={"action": Activity.UPDATE}
    )
    assert response.status_code == status.HTTP_200_OK
    response_json = json.loads(response.rendered_content)
    assert len(response_json) == 1
    assert_data(activity, response_json[0])


def test_filter_date_from(api_client):
    ActivityFactory(action=Activity.CREATE)
    activity = ActivityFactory(action=Activity.UPDATE)
    activity.created = datetime.datetime(2100, 2, 1, tzinfo=tz)
    activity.save()
    response = api_client.get(
        reverse("snapshot:activity-list"), data={"date_from": "2100-01-01"}
    )
    assert response.status_code == status.HTTP_200_OK
    response_json = json.loads(response.rendered_content)
    assert len(response_json) == 1
    assert_data(activity, response_json[0])


def test_filter_date_from_invalid(api_client):
    ActivityFactory(action=Activity.CREATE)
    activity = ActivityFactory(action=Activity.UPDATE)
    activity.created = datetime.datetime(2100, 2, 1, tzinfo=tz)
    activity.save()
    response = api_client.get(
        reverse("snapshot:activity-list"), data={"date_from": "00-01-01"}
    )
    assert response.status_code == status.HTTP_200_OK
    response_json = json.loads(response.rendered_content)
    assert response_json == []


def test_filter_date_to(api_client):
    ActivityFactory(action=Activity.CREATE)
    activity = ActivityFactory(action=Activity.UPDATE)
    activity.created = datetime.datetime(2001, 1, 1, tzinfo=tz)
    activity.save()
    response = api_client.get(
        reverse("snapshot:activity-list"), data={"date_to": "2001-02-01"}
    )
    assert response.status_code == status.HTTP_200_OK
    response_json = json.loads(response.rendered_content)
    assert len(response_json) == 1
    assert_data(activity, response_json[0])


def test_filter_date_to_invalid(api_client):
    ActivityFactory(action=Activity.CREATE)
    activity = ActivityFactory(action=Activity.UPDATE)
    activity.created = datetime.datetime(2001, 1, 1, tzinfo=tz)
    activity.save()
    response = api_client.get(
        reverse("snapshot:activity-list"), data={"date_to": "01-02-01"}
    )
    assert response.status_code == status.HTTP_200_OK
    response_json = json.loads(response.rendered_content)
    assert response_json == []
