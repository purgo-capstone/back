from django.urls import path

from .views import *


urlpatterns = [
    path('hospital/', hospital, name='hospital'),
]