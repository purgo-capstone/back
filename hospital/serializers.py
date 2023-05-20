from rest_framework import serializers
from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from drf_spectacular.types import OpenApiTypes 

from .models import Hospital, Doctor, School, Major, SalesHistory
from auths.serializers import CustomSerializer, UserSerializer
from auths.models import User




class SchoolSerializer(serializers.ModelSerializer):
    '''
    School (General) Serializer
    '''
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = School
        fields = ['id', 'name']
        extra_kwargs = {
            'name': {'required': True},
        }

class MajorSerializer(serializers.ModelSerializer):
    '''
    Major (General) Serializer
    '''
    class Meta:
        model = Major
        fields = ['id', 'name']
        extra_kwargs = {
            'name': {'required': True},
        }

class DoctorSerializer(CustomSerializer):
    '''
    Doctor (General) Serializer
    '''
    
    graduate_school_name = SchoolSerializer(source='graduate_school', read_only=True)
    major_name = MajorSerializer(source='major', read_only=True)
    
    class Meta:
        model = Doctor
        fields = ['name', 'graduate_year', 'graduate_school', 'major', 'graduate_school_name', 'major_name']
        extra_kwargs = {
            'name': {'required': True},
        }
        
class HospitalSerializer(CustomSerializer):
    '''
    Hospital (General) Serializer
    '''
    # Formats establish_at attribute as such : "year-month-day"
    established_at = serializers.DateTimeField(format="%Y-%m-%d")

    manager_info = UserSerializer(source='manager', fields=('id', 'name', 'dept_name'), read_only=True)
    director_info = DoctorSerializer(source='director', fields=('id', 'name', 'major_name', 'graduate_school_name'), read_only=True)

    class Meta:
        model = Hospital
        fields = '__all__'



@extend_schema_serializer(
    exclude_fields=('hosp_info'), # schema ignore these fields
    examples = [
         OpenApiExample(
            '단일 sales history',
            summary='Sales History Summary',
            description='Sales History single instance by saleshistory pk(int:id)',
            value= {
                    "id": 0,
                    "hospital": "요양기호(pk)",
                    "content": "Some Text Content",
                    "get_status_display": "OPP",
                    "hosp_info": {
                        "manager_info": {
                        "name": "string",
                        "dept": 0,
                        },
                        "director_info": {
                        "name": "string",
                        "graduate_year": "2019-08-24",
                        "graduate_school": 0,
                        "major": 0
                        },
                        "hospital_name": "string",
                        
                        "manager": 0,
                        "director": 0,
                    },
                    "modified_at": "2019-08-24T14:15:22Z",
            },
        )
    ]
)
class SalesHistorySerializer(serializers.ModelSerializer):
    '''
    Serializer For Listing(Get) SalesHistory
    '''
    
    hosp_info = HospitalSerializer(source='hospital', fields=('hospital_name', 'manager_info'), read_only=True)
    modified_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
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


@extend_schema_serializer(
    exclude_fields=('hosp_info'), # schema ignore these fields
    examples = [
         OpenApiExample(
            '등록화면 HISTORY',
            summary='Sales History List (user)',
            description='Sales History List by logged in user',
            value= {
                    '1': {"modified_at": "2019-08-24 14:14",
                    "get_status_display": "OPP",
                    "hospital": "요양기호(pk)",
                    "content": "Some Text Content",
                    "hosp_info": {
                        "director_info": {
                        "name": "string",
                        "graduate_year": "2019-08-24",
                        "graduate_school": 0,
                        "major": 0
                        },
                        "hospital_name": "string",
                        "manager": 0,
                        "director": 0,
                    },
                    },'2': {
                    "modified_at": "2019-08-24 14:15",
                    "get_status_display": "ACT",
                    "hospital": "요양기호(pk)",
                    "content": "Some Text Content",
                    "hosp_info": {
                        "director_info": {
                        "name": "string",
                        "graduate_year": "2019-08-24",
                        "graduate_school": 0,
                        "major": 0
                        },
                        "hospital_name": "string",
                        "manager": 0,
                        "director": 0,
                    }

            },
            }
        )
    ]
)
class SalesHistoryRecentSerializer(serializers.ModelSerializer):
    '''
    Serializer for Sales History Recent View 

    *This Serializer is for Read Only

    It shows Certain fields : date, status, content, hosp_info
    '''

    hosp_info = HospitalSerializer(source='hospital', fields=('hospital_name', 
                                                              'director_info'), read_only=True)
    
    modified_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = SalesHistory
        fields = [
            'modified_at', 'status', 'content', 'hosp_info', 'hospital', 'get_status_display'
        ]

