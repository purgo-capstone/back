from django.test import TestCase
from .models import Hospital
from .utils.hosp_fetch import get_hospinfo_openapi
import json
# Create your tests here.


class HospitalTestCase(TestCase):
    def setUp(self):
        hosp_data = get_hospinfo_openapi()
        with open('h_data.json', 'w') as file:
            json.dump(hosp_data, file)
        for key in hosp_data:
           Hospital.objects.create(**hosp_data[key]) 

    def test_db(self):
        db_data = Hospital.objects.all()
        for items in db_data:
            for k, v in items:
                print(f'{k}:{v}')