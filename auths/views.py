from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout
from .models import User, Department
from .serializers import UserSerializer, DepartmentSerializer,\
                         LoginSerializer, RegisterSerializer
from .permissions import isOwner, isAdmin


class DepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = [isAdmin]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class UserViewSet(viewsets.ModelViewSet):
    '''
    User viewset

    - get: list all users
    - post: not allowed / use register view below to create user

    User needs permission : (is owner, is admin) to do the followings 

    - update: updates credentials of the instance
    - delete: makes user inactive state(not delete from db)

    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'email']
    ordering_fields = ['name', 'email']
    ordering = ['name']

    def get_permissions(self):
        actions = ['update', 'partial_update', 'destroy']

        if self.action in actions:
            permission_classes = [IsAuthenticated & (isOwner|isAdmin)]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):

        raise MethodNotAllowed('POST')

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
    - post: Register's new user based on the form credentials
    
    '''
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    

class LoginView(APIView):
    '''
    Login View

    - post: Login user based on the credentials
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

    - get: Logs user out if logged in
    '''
    def get(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)

    

