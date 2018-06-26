import factory
import factory.fuzzy
from demo.sample.models import Author, Book, Tag
from django.contrib.auth import get_user_model
from factory import random

from unicef_snapshot import models


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker("user_name")
    email = factory.Faker("email")

    class Meta:
        model = get_user_model()


class TagFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")

    class Meta:
        model = Tag


class AuthorFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")

    class Meta:
        model = Author


class BookFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    author = factory.SubFactory(AuthorFactory)

    class Meta:
        model = Book


class FuzzyActivityAction(factory.fuzzy.BaseFuzzyAttribute):
    def fuzz(self):
        return random.randgen.choice(
            [a[0] for a in models.Activity.ACTION_CHOICES]
        )


class ActivityFactory(factory.django.DjangoModelFactory):
    target = factory.SubFactory(AuthorFactory)
    action = FuzzyActivityAction()
    by_user = factory.SubFactory(UserFactory)
    data = {"random": "data"}
    change = ""

    class Meta:
        model = models.Activity
