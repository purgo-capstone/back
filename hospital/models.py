from django.db import models 


class InfoModel(models.Model): 
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

    def __str__(self): 
        return (
            f'{self.hospital_id}, {self.hospital_name}, {self.class_code}, {self.class_code_name}, ' 
            f'{self.phone}, {self.url}, {self.established_at}, {self.sggu_name}, {self.emdong_name}, ' 
            f'{self.post_no}, {self.address}, {self.sido_name}, {self.sggu_no}, {self.sido_no}, ' 
            f'{self.general_doctor_count}, {self.intern_count}, {self.fellow_doctor_count}'
            )