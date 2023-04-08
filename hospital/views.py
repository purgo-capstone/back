import os
import xml.etree.ElementTree as et

import requests
from datetime import datetime
from decouple import config


from django.http import HttpResponse
from .models import *


# names like functions, variables are not organized.
# some exceptions may be omitted.
# the api returning hospinfo is just for tests. not complete.


def get_hospinfo_openapi(): 
    hospinfo_openapi = {}

    for pageno in range(1, 9):
        try:
            r = requests.get(
                'http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList?' \
                '&numOfRows=10000' \
                '&ServiceKey=%s' \
                '&pageNo=%s'
                %(config('service_key'), str(pageno))
                )
        except Exception as e:
            print(e)
            raise Exception('An openapi request error occured.')

        try: #
            root = et.fromstring(r.text)
            items = root[1][0]
        except Exception as e:
            print(e)
            raise Exception('A XML parsing error occured.')

        for item in items:
            if not (class_code_name:=item.find('clCd')).text in ['01', '11', '41', '51']: 
                continue

            hospital_id = hospital_id.text if (hospital_id:=item.find('ykiho')) != None else None
            hospital_name = hospital_name.text if (hospital_name:=item.find('yadmNm')) != None else None
            class_code = class_code.text if (class_code:=item.find('clCdNm')) != None else None
            class_code_name = int(class_code_name.text) if (class_code_name:=item.find('clCd')) != None else None
            phone = phone.text if (phone:=item.find('telno')) != None else None
            url = url.text if (url:=item.find('hospUrl')) != None else None
            established_at = datetime.strptime(established_at.text, '%Y%m%d').date() if (established_at:=item.find('estbDd')) != None else None 
            sggu_name = sggu_name.text if (sggu_name:=item.find('sgguCdNm')) != None else None
            emdong_name = emdong_name.text if (emdong_name:=item.find('emdongNm')) != None else None
            post_no = int(post_no.text) if (post_no:=item.find('postNo')) != None else None
            address = address.text if (address:=item.find('addr')) != None else None
            sido_name = sido_name.text if (sido_name:=item.find('sidoCdNm')) != None else None
            sggu_no = int(sggu_no.text) if (sggu_no:=item.find('sgguCd')) != None else None
            sido_no = int(sido_no.text) if (sido_no:=item.find('sidoCd')) != None else None
            general_doctor_count = int(general_doctor_count.text) if (general_doctor_count:=item.find('detyGdrCnt')) != None else None
            intern_count = int(intern_count.text) if (intern_count:=item.find('detyIntnCnt')) != None else None
            resident_count = int(resident_count.text) if (resident_count:=item.find('detyResdntCnt')) != None else None
            fellow_doctor_count = int(fellow_doctor_count.text) if (fellow_doctor_count:=item.find('detySdrCnt')) != None else None

            hospinfo_openapi[hospital_id] = {
                'hospital_name': hospital_name,
                'class_code': class_code,
                'class_code_name': class_code_name,
                'phone': phone,
                'url': url,
                'established_at': established_at,
                'sggu_name': sggu_name,
                'emdong_name': emdong_name,
                'post_no': post_no,
                'address': address,
                'sido_name': sido_name,
                'sggu_no': sggu_no,
                'sido_no': sido_no,
                'general_doctor_count': general_doctor_count,
                'intern_count': intern_count,
                'resident_count': resident_count,
                'fellow_doctor_count': fellow_doctor_count
                }

    return hospinfo_openapi


def main(request):
    hospinfo_openapi = get_hospinfo_openapi() 

    for k, v in hospinfo_openapi.items(): 
        try:
            oapi = Openapi.objects.get(hospital_id=k)

            oapi.hospital_name = new_hospital_name if (new_hospital_name:=v['hospital_name']) != oapi.hospital_name else oapi.hospital_name
            oapi.class_code = new_class_code if (new_class_code:=v['class_code']) != oapi.class_code else oapi.class_code
            oapi.class_code_name = new_class_code_name if (new_class_code_name:=v['class_code_name']) != oapi.class_code_name else oapi.class_code_name
            oapi.phone = new_phone if (new_phone:=v['phone']) != oapi.phone else oapi.phone
            oapi.url = new_url if (new_url:=v['url']) != oapi.url else oapi.url
            oapi.established_at = new_established_at if (new_established_at:=v['established_at']) != oapi.established_at else oapi.established_at
            oapi.sggu_name = new_sggu_name if (new_sggu_name:=v['sggu_name']) != oapi.sggu_name else oapi.sggu_name
            oapi.emdong_name = new_emdong_name if (new_emdong_name:=v['emdong_name']) != oapi.emdong_name else oapi.emdong_name
            oapi.post_no = new_post_no if (new_post_no:=v['post_no']) != oapi.post_no else oapi.post_no
            oapi.address = new_address if (new_address:=v['address']) != oapi.address else oapi.address
            oapi.sido_name = new_sido_name if (new_sido_name:=v['sido_name']) != oapi.sido_name else oapi.sido_name
            oapi.sggu_no = new_sggu_no if (new_sggu_no:=v['sggu_no']) != oapi.sggu_no else oapi.sggu_no
            oapi.sido_no = new_sido_no if (new_sido_no:=v['sido_no']) != oapi.sido_no else oapi.sido_no
            oapi.general_doctor_count = new_general_doctor_count if (new_general_doctor_count:=v['general_doctor_count']) != oapi.general_doctor_count else oapi.general_doctor_count
            oapi.intern_count = new_intern_count if (new_intern_count:=v['intern_count']) != oapi.intern_count else oapi.intern_count
            oapi.resident_count = new_resident_count if (new_resident_count:=v['resident_count']) != oapi.resident_count else oapi.resident_count
            oapi.fellow_doctor_count = new_fellow_doctor_count if (new_fellow_doctor_count:=v['fellow_doctor_count']) != oapi.fellow_doctor_count else oapi.fellow_doctor_count

            oapi.save()
        except Openapi.DoesNotExist:
            oapi = Openapi(
                hospital_id=k,
                hospital_name=v['hospital_name'],
                class_code=v['class_code'],
                class_code_name=v['class_code_name'],
                phone=v['phone'],
                url=v['url'],
                established_at=v['established_at'],
                sggu_name=v['sggu_name'],
                emdong_name=v['emdong_name'],
                post_no=v['post_no'],
                address=v['address'],
                sido_name=v['sido_name'],
                sggu_no=v['sggu_no'],
                sido_no=v['sido_no'],
                general_doctor_count=v['general_doctor_count'],
                intern_count=v['intern_count'],
                resident_count=v['resident_count'],
                fellow_doctor_count=v['fellow_doctor_count']
                )
            oapi.save()

    return HttpResponse('complete.')