import pytest

from mykiapp import serializers
from . import factories

pytestmark = pytest.mark.django_db


class TestEmployeeSerializer:
    def test_employee_serializer(self, request):
        tested_user = factories.EmployeeFactory()
        serializer_data = {
            "first_name": tested_user.first_name,
            "last_name": tested_user.last_name
        }
        assert serializers.EmployeeSerializer(data=serializer_data).is_valid()


class TestTeamSerializer:
    def test_team_serializer(self, request):
        tested_team = factories.TeamFactory()
        serializer_data = {
            "name": tested_team.name,
        }
        assert serializers.TeamSerializer(data=serializer_data).is_valid()

# Rest Serializers to be tested
