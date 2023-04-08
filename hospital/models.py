from datetime import datetime

from django.db import models 


# should modify some field names?

class Openapi(models.Model): 
    hospital_id = models.CharField(max_length=255, primary_key=True)
    hospital_name = models.CharField(max_length=255, null=True)
    class_code = models.CharField(max_length=255, null=True)
    class_code_name = models.IntegerField(null=True)
    phone = models.CharField(max_length=255, null=True)
    url = models.CharField(max_length=255, null=True)
    established_at = models.DateTimeField(null=True)
    sggu_name = models.CharField(max_length=255, null=True)
    emdong_name = models.CharField(max_length=255, null=True)
    post_no = models.IntegerField(null=True)
    address = models.CharField(max_length=255, null=True)
    sido_name = models.CharField(max_length=255, null=True)
    sggu_no = models.IntegerField(null=True)
    sido_no = models.IntegerField(null=True)
    general_doctor_count = models.IntegerField(null=True)
    intern_count = models.IntegerField(null=True)
    resident_count = models.IntegerField(null=True)
    fellow_doctor_count = models.IntegerField(null=True)