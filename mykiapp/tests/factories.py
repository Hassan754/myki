import factory

from mykiapp.models import *
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: "user{0}".format(n))
    email = factory.Sequence(lambda n: "user-{0}@example.com".format(n))
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    class Meta:
        model = User


class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Employee

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")


class TeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Team

    name = factory.Faker("name")


class ItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Item

    name = factory.Sequence(lambda n: n)
    description = factory.Faker("text")


class FolderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Folder

    name = factory.Sequence(lambda n: n)
    description = factory.Faker("text")


class EmployeeItemAccessFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmployeeItemAccess

    item = factory.SubFactory(ItemFactory)
    employee = factory.SubFactory(EmployeeFactory)
    access_level = 2


class EmployeeFolderAccessFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmployeeFolderAccess

    folder = factory.SubFactory(FolderFactory)
    employee = factory.SubFactory(EmployeeFactory)
    access_level = 2


class TeamItemAccessFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TeamItemAccess

    item = factory.SubFactory(ItemFactory)
    team = factory.SubFactory(TeamFactory)
    access_level = 2


class TeamFolderAccessFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TeamFolderAccess

    folder = factory.SubFactory(FolderFactory)
    team = factory.SubFactory(TeamFactory)
    access_level = 2
