from rest_framework import serializers

from auths.serializers import CustomSerializer, UserSerializer
from auths.models import User
from .models import Hospital, Doctor, School, Major, SalesHistory


class HospitalSerializer(CustomSerializer):
    '''
    Hospital (General) Serializer
    '''
    # Formats establish_at attribute as such : "year-month-day"
    established_at = serializers.DateTimeField(format='%Y-%m-%d')

    manager_info = UserSerializer(source='manager', fields=('name', 'dept'))

    class Meta:
        model = Hospital
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    '''
    Doctor (General) Serializer
    '''
    class Meta:
        model = Doctor
        fields = ['name']
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

class SalesHistorySerializer(serializers.ModelSerializer):
    '''
    Serializer For Listing(Get) SalesHistory
    '''
    hosp_info = HospitalSerializer(source='hospital', fields=('hospital_name', 'manager_info'), read_only=True)

    class Meta:
        model = SalesHistory
        fields = ['id', 'hospital',
                  'content', 'get_status_display', 'hosp_info',
                  'created_at', 'modified_at']
        

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
