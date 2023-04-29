from rest_framework import serializers
from .models import User, Department
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ['name']


class LoginSerializer(serializers.Serializer):
    '''
    Login Serializer
    
    Takes a given Email, and Password to validate a user

    returns the user on success, or raises a ValidationError
    '''
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:

            user = authenticate(
                request=self.context.get('request'),
                username = email,
                password = password)

            if not user:
                raise serializers.ValidationError('Invalid Credentials', code='authorization')
        else:
            raise serializers.ValidationError('Invalid Credentials', code='authorization')
        
        attrs['user'] = user
        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    '''
    회원가입 Serializer

    Check 항목:
    
    Email이 unique,
    
    password is valid *validate_passowrd 참조

    '''
    email = serializers.EmailField(
        required = True,
        validators = [UniqueValidator(queryset = User.objects.all())]
    )

    name = serializers.CharField(
        required = True
    )

    password = serializers.CharField(
        write_only=True,
        required = True,
        validators = [validate_password]
    )

    class Meta:
        model = User
        fields = ('email', 'password', 'name')

    def create(self, validated_data):
        
        user = User.objects.create_user(
            email=validated_data['email'], 
            password=validated_data['password'], 
            name=validated_data['name']
        )
        user.save()
        return user