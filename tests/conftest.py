import pytest
from django.contrib.admin.sites import AdminSite
from rest_framework.test import APIClient
from tests import factories


@pytest.fixture()
def api_client():
    return APIClient()


@pytest.fixture
def admin_site():
    return AdminSite()


@pytest.fixture
def user():
    return factories.UserFactory()


@pytest.fixture
def author():
    return factories.AuthorFactory()
