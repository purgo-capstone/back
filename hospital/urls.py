'''
Basic router url provides these endpoints:

GET /hospitals/: Retrieve a list of all hospitals
POST /hospitals/: Create a new user
GET /hospitals/{pk}/: Retrieve a single user by primary key
PUT /hospitals/{pk}/: Update a single user by primary key
PATCH /hospitals/{pk}/: Partially update a single user by primary key
DELETE /hospitals/{pk}/: Delete a single user by primary key

'''


from django.urls import path, include
from rest_framework import routers
from .views import HospitalViewSet, DoctorViewSet, \
                   MajorViewSet, SchoolViewSet, \
                   SalesHistoryView
                   
router = routers.DefaultRouter()

router.register(r'hospitals', HospitalViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'majors', MajorViewSet)
router.register(r'schools', SchoolViewSet)

urlpatterns =[
    path('', include(router.urls)),
    path('histories/', SalesHistoryView.as_view(), name='sales-history'),
    path('histories/<int:pk>/', SalesHistoryView.as_view(), name='sales-history-more'),
]

