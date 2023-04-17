from django.urls import reverse
from rest_framework import status

import pytest

from unicef_snapshot.models import Activity

pytestmark = pytest.mark.django_db


def test_snapshot_model_serializer(api_client, author, user):
    activity_qs = Activity.objects.filter(target_object_id=author.pk)
    assert activity_qs.exists() is False
    api_client.force_login(user)
    response = api_client.patch(
        reverse("sample:author-detail", args=[author.pk]),
        data={"name": "Changed"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert activity_qs.exists() is True
