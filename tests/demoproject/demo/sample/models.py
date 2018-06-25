from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        app_label = "sample"


class Author(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        app_label = "sample"


class Book(models.Model):
    name = models.CharField(max_length=150)
    author = models.ForeignKey(
        Author,
        related_name="books",
        on_delete=models.CASCADE,
    )
    tags = models.ManyToManyField(Tag)

    class Meta:
        app_label = "sample"
