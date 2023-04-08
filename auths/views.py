from rest_framework import viewsets
from .models import User, Department
from .serializers import UserSerializer, DepartmentSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

'''
Basic ModelViewSet provides these functions:

list(): Returns a list of all objects in the queryset.

create(): Creates a new object instance from the request data.

retrieve(): Returns a single object instance by primary key.

update(): Updates an object instance by primary key with the request data.

partial_update(): Updates an object instance by primary key with the request data, but allows partial updates.

destroy(): Deletes an object instance by primary key.

'''
