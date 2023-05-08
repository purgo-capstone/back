'''
Basic ModelViewSet provides these functions:

list(): Returns a list of all objects in the queryset.

create(): Creates a new object instance from the request data.

retrieve(): Returns a single object instance by primary key.

update(): Updates an object instance by primary key with the request data.

partial_update(): Updates an object instance by primary key with the request data, but allows partial updates.

destroy(): Deletes an object instance by primary key.

'''

from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout
from .models import User, Department
from .serializers import UserSerializer, DepartmentSerializer,\
                         LoginSerializer, RegisterSerializer
from .permissions import isOwner

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'email']
    ordering_fields = ['name', 'email']
    ordering = ['name']

    def get_permissions(self):
        actions = ['update', 'partial_update', 'destroy']
        if self.action in actions:
            permission_classes = [IsAuthenticated & isOwner]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def destroy(self, request, *args, **kwargs):
        '''
        Override Destroy Method to Inactivate user on delete request
        '''
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({'detail':'Deleted User'}, status=status.HTTP_204_NO_CONTENT)


class RegisterView(CreateAPIView):
    '''
    Register View
    '''
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    

class LoginView(APIView):
    '''
    Login View

    '''
    authentication_classes = [SessionAuthentication] # Session Based Authentication
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request':request})
        
        if serializer.is_valid(raise_exception=True):

            user = serializer.validated_data['user']

            login(request, user)
            return Response(status=status.HTTP_202_ACCEPTED)
        
        else:
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    '''
    Logout View
    '''
    def get(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)

    

