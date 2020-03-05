import pytest
from mykiapp.models import *
from mykiapp.tests.factories import *

pytestmark = pytest.mark.django_db


class TestEmployeeModel:
    def test_employee_permissions(self):
        item = ItemFactory()
        employee = EmployeeFactory()
        user_permission = EmployeeItemAccess(item=item, employee=employee).save()
        assert len(employee.get_all_permissions()) == 1
        team = TeamFactory()
        team.employees.add(employee)
        other_permission = TeamItemAccess(item=item, team=team, access_level=1).save()
        assert len(employee.get_all_permissions()) == 1
        assert employee.get_all_permissions()[0]['access_level'] == 1
        assert employee.get_all_permissions()[0]['through'] == f'Team {team.name}'
