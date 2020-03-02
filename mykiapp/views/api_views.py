from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from mykiapp.serializers import *
from mykiapp.models import Employee, Team, Item, Folder


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permissions_serializer = ItemAccessSerializer

    @action(detail=True, methods=['GET'])
    def permissions(self, request, pk=None):
        employee = self.get_object()
        permissions = employee.get_all_permissions()
        serializer = self.permissions_serializer(permissions, many=True, context={"request": request}).data
        return Response(serializer)

    @action(detail=True, methods=['POST', 'PUT'], serializer_class=ItemEmployeeSerializer)
    def edit_create_item_permissions(self, request, pk=None):
        permission = EmployeeItemAccess.objects.filter(employee_id=pk, item=request.data['item']).first()
        serializer = self.serializer_class(permission, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], serializer_class=ItemEmployeeSerializer)
    def delete__item_permission(self, request, pk=None):
        permission = EmployeeItemAccess.objects.filter(employee_id=pk, item=request.data['item']).delete()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST', 'PUT'], serializer_class=FolderEmployeeSerializer)
    def edit_create_folder_permissions(self, request, pk=None):
        permission = EmployeeFolderAccess.objects.filter(employee_id=pk, folder=request.data['folder']).first()
        serializer = self.serializer_class(permission, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], serializer_class=FolderEmployeeSerializer)
    def delete__folder_permission(self, request, pk=None):
        permission = EmployeeFolderAccess.objects.filter(employee_id=pk, item=request.data['folder']).delete()
        return Response(status=status.HTTP_200_OK)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    @action(detail=True, methods=['PUT'], url_path='add/(?P<user_id>[^/.]+)')
    def add_employee(self, request, pk=None, user_id=None):
        team = self.get_object()
        try:
            employee = Employee.objects.get(id=user_id)
        except:
            raise APIException("Employee Doesn't exist", 'employee_not_found')
        team.employees.add(employee)
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['POST', 'PUT'], serializer_class=ItemTeamSerializer)
    def edit_create_item_permissions(self, request, pk=None):
        permission = TeamItemAccess.objects.filter(team_id=pk, item=request.data['item']).first()
        serializer = self.serializer_class(permission, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], serializer_class=ItemTeamSerializer)
    def delete__item_permission(self, request, pk=None):
        permission = TeamItemAccess.objects.filter(team_id=pk, item=request.data['item']).delete()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST', 'PUT'], serializer_class=FolderTeamSerializer)
    def edit_create_folder_permissions(self, request, pk=None):
        permission = TeamFolderAccess.objects.filter(employee_id=pk, folder=request.data['folder']).first()
        serializer = self.serializer_class(permission, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], serializer_class=FolderTeamSerializer)
    def delete__folder_permission(self, request, pk=None):
        permission = TeamFolderAccess.objects.filter(employee_id=pk, item=request.data['folder']).delete()
        return Response(status=status.HTTP_200_OK)


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class FolderViewSet(viewsets.ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

    @action(detail=True, methods=['PUT'], url_path='add/(?P<item_id>[^/.]+)')
    def add_item(self, request, pk=None, item_id=None):
        folder = self.get_object()
        try:
            item = Item.objects.get(id=item_id)
        except:
            raise APIException("Item Doesn't exist", 'item_not_found')
        folder.items.add(item)
        return Response(status=status.HTTP_201_CREATED)
