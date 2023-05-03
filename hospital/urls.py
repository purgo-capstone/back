from rest_framework import routers
from .views import HospitalViewSet, DoctorViewSet, MajorViewSet, SchoolViewSet, hospital_test_data
from django.urls import path, include

router = routers.DefaultRouter()

router.register(r'hospitals', HospitalViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'majors', MajorViewSet)
router.register(r'schools', SchoolViewSet)

urlpatterns =[
    path('', include(router.urls)),
    path('test-data', hospital_test_data, name='test-data')
]

'''
Basic router url provides these endpoints:

GET /hospitals/: Retrieve a list of all hospitals
POST /hospitals/: Create a new user
GET /hospitals/{pk}/: Retrieve a single user by primary key
PUT /hospitals/{pk}/: Update a single user by primary key
PATCH /hospitals/{pk}/: Partially update a single user by primary key
DELETE /hospitals/{pk}/: Delete a single user by primary key

'''