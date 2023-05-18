from rest_framework import serializers

from .models import Hospital, Doctor, School, Major, SalesHistory
from auths.serializers import CustomSerializer, UserSerializer
from auths.models import User


class DoctorSerializer(CustomSerializer):
    '''
    Doctor (General) Serializer
    '''
    class Meta:
        model = Doctor
        fields = ['name', 'graduate_year', 'graduate_school', 'major']
        extra_kwargs = {
            'name': {'required': True},
        }

class SchoolSerializer(serializers.ModelSerializer):
    '''
    School (General) Serializer
    '''
    class Meta:
        model = School
        fields = ['name']
        extra_kwargs = {
            'name': {'required': True},
        }

class MajorSerializer(serializers.ModelSerializer):
    '''
    Major (General) Serializer
    '''
    class Meta:
        model = Major
        fields = ['name']
        extra_kwargs = {
            'name': {'required': True},
        }

class HospitalSerializer(CustomSerializer):
    '''
    Hospital (General) Serializer
    '''
    # Formats establish_at attribute as such : "year-month-day"
    established_at = serializers.DateTimeField(format="%Y-%m-%d")

    manager_info = UserSerializer(source='manager', fields=('name', 'dept'))
    director_info = DoctorSerializer(source='director', fields=('name', 'major', 'graduate_school'))

    class Meta:
        model = Hospital
        fields = '__all__'

class SalesHistorySerializer(serializers.ModelSerializer):
    '''
    Serializer For Listing(Get) SalesHistory
    '''
    
    hosp_info = HospitalSerializer(source='hospital', fields=('hospital_name', 'manager_info'), read_only=True)
    modified_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    class Meta:
        model = SalesHistory
        fields = ['id', 'hospital', 'content', 
                  'get_status_display', 'hosp_info',
                  'modified_at']
        
class SalesHistoryCreateSerializer(serializers.ModelSerializer):
    '''
    Serializer for Creating(Post) Sales History
    '''

    class Meta:
        model = SalesHistory
        fields = [
            'hospital', 'content', 'status'
        ]
        extra_kwargs = {
            'hospital': {'required': True},
            'content': {'required': True},
            'status': {'required': True}
        }

class SalesHistoryRegisterSerializer(serializers.ModelSerializer):
    '''
    Serializer for Sales History Register View 

    *This Serializer is for Read Only

    It shows Certain fields : date, status, content, hosp_info
    '''

    hosp_info = HospitalSerializer(source='hospital', fields=('hospital_name', 
                                                              'manager_info', 
                                                              'director_info'))
    
    modified_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = SalesHistory
        fields = [
            'modified_at', 'status', 'content', 'hosp_info', 'hospital', 'get_status_display'
        ]

