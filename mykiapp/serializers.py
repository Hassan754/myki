from rest_framework import serializers
from mykiapp.models import *


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="mykiapp:employee-detail")

    class Meta:
        model = Employee
        fields = ['id', 'url', 'first_name', 'last_name', ]


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    employees = EmployeeSerializer(many=True, read_only=False, required=False)
    url = serializers.HyperlinkedIdentityField(view_name="mykiapp:team-detail")

    class Meta:
        model = Team
        fields = ['id', 'url', 'name', 'employees']


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="mykiapp:item-detail")

    class Meta:
        model = Item
        fields = ['id', 'url', 'name', 'description']


class FolderSerializer(serializers.HyperlinkedModelSerializer):
    items = ItemSerializer(many=True, read_only=False)
    url = serializers.HyperlinkedIdentityField(view_name="mykiapp:folder-detail")

    class Meta:
        model = Folder
        fields = ['id', 'url', 'name', 'description', 'items']


class ItemEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeItemAccess
        fields = ['item', 'employee', 'access_level']
        


class ItemTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamItemAccess
        fields = ['item', 'team', 'access_level']


class FolderEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeFolderAccess
        fields = ['folder', 'employee', 'access_level']


class FolderTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamFolderAccess
        fields = ['folder', 'team', 'access_level']


class ItemAccessSerializer(serializers.Serializer):
    item = serializers.SerializerMethodField()
    access_level = serializers.SerializerMethodField()
    through = serializers.CharField()

    class Meta:
        fields = ['item', 'access_level', 'through']

    def get_item(self, obj):
        return ItemSerializer(obj['item'], context=self.context).data

    def get_access_level(self, obj):
        return obj['access_level']

    def get_through(self, obj):
        return obj['through']
