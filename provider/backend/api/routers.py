from rest_framework import routers
from .viewsets import UserList
routers = routers.DefaultRouter()
routers.register('user', UserList)