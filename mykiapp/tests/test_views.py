import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from mykiapp.models import *
from mykiapp.tests.factories import *

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    def inner(user=None, *args, **kwargs):
        ac = APIClient(*args, **kwargs)
        if user is not None:
            ac.force_authenticate(user)
        return ac

    return inner


@pytest.fixture
def user():
    return UserFactory()


class TestEmployeeView:
    def test_list_employees(self, user, api_client):
        url_name = "mykiapp:employee-list"
        employees_count = Employee.objects.count()
        EmployeeFactory.create_batch(5)
        response = api_client(user).get(reverse(url_name))
        assert response.status_code == status.HTTP_200_OK
        print(response.data)
        assert len(response.data) == employees_count + 5

    def test_employee_details(self, user, api_client):
        url_name = "mykiapp:employee-detail"
        employee = EmployeeFactory()
        response = api_client(user).get(reverse(url_name, args=[str(employee.id)]), )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == str(employee.id)

    def test_employee_delete(self, user, api_client):
        url_name = "mykiapp:employee-detail"
        employee = EmployeeFactory()
        assert Employee.objects.filter(id=employee.id).exists()
        permission = EmployeeItemAccessFactory(employee=employee)
        assert EmployeeItemAccess.objects.filter(id=permission.id).exists()
        response = api_client(user).delete(reverse(url_name, args=[str(employee.id)]), )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Employee.objects.filter(id=employee.id).exists()
        assert not EmployeeItemAccess.objects.filter(id=permission.id).exists()

    def test_employee_update(self, user, api_client):
        url_name = "mykiapp:employee-detail"
        employee = EmployeeFactory()
        data = {"first_name": "Hassan"}
        response = api_client(user).patch(reverse(url_name, args=[str(employee.id)], ), data=data, )
        assert response.status_code == status.HTTP_200_OK
        employee = Employee.objects.get(id=employee.id)
        assert employee.first_name == "Hassan"

    def test_permissions(self, user, api_client):
        url_name = 'mykiapp:employee-permissions'
        employee = EmployeeFactory()
        for i in range(5):
            EmployeeFolderAccessFactory(employee=employee)
            EmployeeItemAccessFactory(employee=employee)
        assert EmployeeFolderAccess.objects.filter(employee=employee).count() == 5
        assert EmployeeItemAccess.objects.filter(employee=employee).count() == 5
        response = api_client(user).get(reverse(url_name, args=[str(employee.id)]))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0

    def test_edit_create_item_permissions(self, user, api_client):
        url_name = 'mykiapp:employee-edit-create-item-permissions'
        employee = EmployeeFactory()
        item = ItemFactory()
        assert not EmployeeItemAccess.objects.filter(employee=employee, item=item).exists()
        data = {
            "item": item.id,
            "access_level": 2
        }
        response = api_client(user).patch(reverse(url_name, args=[str(employee.id)], ), data=data, format="json" )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        response = api_client(user).post(reverse(url_name, args=[str(employee.id)], ), data=data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert EmployeeItemAccess.objects.filter(employee=employee, item=item).exists()
        assert EmployeeItemAccess.objects.filter(employee=employee, item=item).first().access_level == 2
# ...