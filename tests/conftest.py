import pytest
from rest_framework.test import APIClient
from tests import factories


@pytest.fixture()
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return factories.UserFactory()


@pytest.fixture
def author():
    return factories.AuthorFactory()
