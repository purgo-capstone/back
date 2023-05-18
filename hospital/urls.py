from django.urls import path, include
from rest_framework import routers
from .views import HospitalViewSet, DoctorViewSet, \
                   MajorViewSet, SchoolViewSet, \
                   SalesHistoryView, SalesHistoryRegisterView
                   
router = routers.DefaultRouter()

router.register(r'hospitals', HospitalViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'majors', MajorViewSet)
router.register(r'schools', SchoolViewSet)

urlpatterns =[
    path('', include(router.urls)),
    path('saleshistory/', SalesHistoryView.as_view(), name='sales-history'),
    path('saleshistory/<str:pk>/', SalesHistoryView.as_view(), name='sales-history-detail'),
    path('salesregisterhistory/', SalesHistoryRegisterView.as_view(), name='sales-history-register')
]

