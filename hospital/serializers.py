from rest_framework import serializers
from .models import Hospital, Doctor, School, Major

class HospitalSerializer(serializers.ModelSerializer):

    # Formats establish_at attribute as such : "year-month-day"
    established_at = serializers.DateTimeField(format='%Y-%m-%d')
    class Meta:
        model = Hospital
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctor
        fields = ['name']

class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = ['name']

class MajorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Major
        fields = ['name']




