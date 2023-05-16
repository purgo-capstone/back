from rest_framework.decorators import api_view
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import redirect

from auths.permissions import isAdmin, isOwner
from .models import Hospital, Doctor, Major, School, SalesHistory
from .serializers import HospitalSerializer, DoctorSerializer, \
                         MajorSerializer, SchoolSerializer, \
                         SalesHistorySerializer, SalesHistoryCreateSerializer

from .utils.hosp_fetch import get_hospinfo_openapi                
                         

class DoctorViewSet(viewsets.ModelViewSet):
    '''
    Doctor ViewSet 
    '''
    permission_classes = [isAdmin]
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class HospitalViewSet(viewsets.ModelViewSet):
    '''
    Hospital ViewSet

    crud, pagination, searchfilter, orderfilter 기능을 제공
    
    Default order: hospital_name

    '''
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['class_code']
    search_fields = ['hospital_name', 'director__name']
    ordering_fields = ['hospital_name', 'established_at']
    ordering = ['hospital_name']

class MajorViewSet(viewsets.ModelViewSet):
    permission_classes = [isAdmin]
    queryset = Major.objects.all()
    serializer_class = MajorSerializer

class SchoolViewSet(viewsets.ModelViewSet):
    permission_classes = [isAdmin]
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

class SalesHistoryView(APIView):
    '''
    SalesHistory API View

    get: returns the specific history with pk, entire list without pk

    ** Requires Permission (Hospital Manager) or Admin

    post: creates a new history

    update: update history

    partial update: paritally updates history

    delete: deletes history

    add sql logging ref: https://www.dabapps.com/insights/logging-sql-queries-django-13/

    *query performance differs by using select_related, and prefetch related
    '''
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return SalesHistory.objects.get(pk=pk)
        except SalesHistory.DoesNotExist:
            return Response({'pk not found'}, status=status.HTTP_404_NOT_FOUND)

    def check_owner(self, obj):

        # Checks if user is the manager of the hospital
        return (obj.hospital.manager == self.request.user) or (self.request.user.is_admin)

    def get(self, request, pk=None):
        '''
        Returns The histories managed by the current user if pk,
        Returns all history if not
        '''

        if pk is not None:
            history = SalesHistory.objects.filter(pk=pk).select_related('hospital__manager')    
        else:
            history = SalesHistory.objects.all().select_related('hospital__manager')

        serializer = SalesHistorySerializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    
    def post(self, request, format=None):
        '''
        Create(Post) a new Sales History 

        required: Hospital(key), status: B2B(stages A,B,O,F,P), content
        '''
        serializer = SalesHistoryCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def put(self, request, pk):
        '''
        Update History
        ** Requires: Hospital, status, content fields
        '''
        item = self.get_object(pk)
        
        # Checks for owner permission
        if not self.check_owner(item):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = SalesHistoryCreateSerializer(instance=item, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        '''
        Partially Updates History
        ** Doesn't Require Any Field
        '''
        item = self.get_object(pk)

        if not self.check_owner(item):
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = SalesHistoryCreateSerializer(instance=item, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(data=serializer.error_messages, status=status.HTTP_404_NOT_FOUND)

    
    def delete(self, request, pk):
        '''
        Delete History
        '''
        item = self.get_object(pk)

        if not self.check_owner(item):
            return Response(status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(item)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    allowed_methods = ['get', 'post', 'put', 'patch', 'delete']

    
####
#### This Function is for Testing Purposes ONLY
####

@api_view(['POST'])
def hospital_test_data(request):
    '''
    *Test용* 심평원 api를 fetch하여 db에 저장하는 view
    '''
    hosp_data = get_hospinfo_openapi()
    for key in hosp_data.keys():
        hosp_data[key]['hospital_id'] = key
        new_hosp = Hospital(**hosp_data[key])
        new_hosp.save()
    
    return ('/hospitals')
