import uuid

from django.db import models

from mykiapp.enums.models import AccessLevel
from mykiapp.logic.models_logic import get_permissions, get_all_user_permissions


class BaseModel(models.Model):
    # Override the default integer id with uuid field for security
    id = models.UUIDField(
        verbose_name="id",
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        editable=False,
        db_index=True,
    )

    class Meta:
        abstract = True


class Item(BaseModel):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Folder(BaseModel):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    items = models.ManyToManyField(Item)

    def __str__(self):
        return self.name


class Employee(BaseModel):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)

    def get_user_permissions(self):
        return get_permissions(self)

    def get_all_permissions(self):
        return get_all_user_permissions(self)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class Team(BaseModel):
    name = models.CharField(max_length=40)
    employees = models.ManyToManyField(Employee, related_name="teams")

    def get_all_permissions(self):
        return get_permissions(self)

    def __str__(self):
        return self.name


ACCESS_LEVELS = (
    # Lower Value -> higher access
    (1, AccessLevel.ADMIN.value),
    (2, AccessLevel.STANDARD.value)
)


class TeamItemAccess(BaseModel):
    team = models.ForeignKey(Team, models.CASCADE, related_name="items")
    item = models.ForeignKey(Item, models.CASCADE)
    access_level = models.IntegerField(choices=ACCESS_LEVELS, default=2)

    class Meta:
        unique_together = ('team', 'item')


class TeamFolderAccess(BaseModel):
    team = models.ForeignKey(Team, models.CASCADE, related_name="folders")
    folder = models.ForeignKey(Folder, models.CASCADE)
    access_level = models.IntegerField(choices=ACCESS_LEVELS, default=2)

    class Meta:
        unique_together = ('team', 'folder')


class EmployeeItemAccess(BaseModel):
    employee = models.ForeignKey(Employee, models.CASCADE, related_name="items")
    item = models.ForeignKey(Item, models.CASCADE)
    access_level = models.IntegerField(choices=ACCESS_LEVELS, default=2)

    class Meta:
        unique_together = ('employee', 'item')


class EmployeeFolderAccess(BaseModel):
    employee = models.ForeignKey(Employee, models.CASCADE, related_name="folders")
    folder = models.ForeignKey(Folder, models.CASCADE)
    access_level = models.IntegerField(choices=ACCESS_LEVELS, default=2)

    class Meta:
        unique_together = ('employee', 'folder')
