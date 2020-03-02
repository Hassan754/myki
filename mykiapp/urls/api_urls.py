from django.conf.urls import url
from django.urls import include
from rest_framework import routers
from mykiapp.views.api_views import *

app_name = 'mykiapp'

router = routers.DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'items', ItemViewSet)
router.register(r'folders', FolderViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls'))
]
