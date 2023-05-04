'''
Basic ModelViewSet provides these functions:

list(): Returns a list of all objects in the queryset.

create(): Creates a new object instance from the request data.

retrieve(): Returns a single object instance by primary key.

update(): Updates an object instance by primary key with the request data.

partial_update(): Updates an object instance by primary key with the request data, but allows partial updates.

destroy(): Deletes an object instance by primary key.

'''


from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Hospital, Doctor, Major, School
from .serializers import HospitalSerializer, DoctorSerializer, \
                         MajorSerializer, SchoolSerializer

from rest_framework.decorators import api_view
from django.shortcuts import redirect

class HospitalViewSet(viewsets.ModelViewSet):
    '''
    Hospital 관련 Api View

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

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class MajorViewSet(viewsets.ModelViewSet):
    queryset = Major.objects.all()
    serializer_class = MajorSerializer

class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

# @api_view(['POST'])
# def hospital_test_data(request):
#     '''
#     *Test용* 심평원 api를 fetch하여 db에 저장하는 view
#     '''
#     hosp_data = get_hospinfo_openapi()
#     for key in hosp_data.keys():
#         hosp_data[key]['hospital_id'] = key
#         new_hosp = Hospital(**hosp_data[key])
#         new_hosp.save()
    
#     return ('/hospitals')
