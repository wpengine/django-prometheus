from django.db.models import (
    Model, CharField, PositiveIntegerField, ManyToManyField)
from django_prometheus.models import ExportModelOperationsMixin


class Dog(ExportModelOperationsMixin('dog'), Model):
    name = CharField(max_length=100, unique=True)
    breed = CharField(max_length=100, blank=True, null=True)
    age = PositiveIntegerField(blank=True, null=True)


class Lawn(ExportModelOperationsMixin('lawn'), Model):
    location = CharField(max_length=100)


class Ingredient(ExportModelOperationsMixin('ingredient'), Model):
    name = CharField(max_length=100, unique=True)


class Recipe(ExportModelOperationsMixin('recipe'), Model):
    name = CharField(max_length=100, unique=True)
    country = CharField(max_length=2)
    ingredients = ManyToManyField(Ingredient)
