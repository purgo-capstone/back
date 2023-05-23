from rest_framework.decorators import api_view
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes 
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import redirect

from auths.permissions import isAdmin, isManager
from .models import Hospital, Doctor, Major, School, SalesHistory
from .serializers import HospitalSerializer, DoctorSerializer, \
                         MajorSerializer, SchoolSerializer, \
                         UserCountSerializer, StatusCountSerializer, \
                         DateCountSerializer, DashboardSerializer,\
                         SalesHistorySerializer, SalesHistoryCreateSerializer, \
                         SalesHistoryRecentSerializer

from .utils.hosp_fetch import get_hospinfo_openapi                
                        

class DoctorViewSet(viewsets.ModelViewSet):
    '''
    Doctor ViewSet 
    
    crud operation on doctor model
    permission: Admin
    
    '''
    permission_classes = [isAdmin]
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class HospitalViewSet(viewsets.ModelViewSet):
    '''
    Hospital ViewSet

    crud, pagination, searchfilter, orderfilter 기능을 제공
    
    Default order: hospital_name

    '''
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['class_code', 'manager__id']
    search_fields = ['hospital_name', 'director__name']
    ordering_fields = ['hospital_name', 'established_at']
    ordering = ['hospital_name']
    
    def get_permissions(self):
        actions = ['update', 'partial_update', 'destroy']

        if self.action in actions:
            permission_classes = [IsAuthenticated & (isManager|isAdmin)]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
        
class MajorViewSet(viewsets.ModelViewSet):
    permission_classes = [isAdmin]
    queryset = Major.objects.all()
    serializer_class = MajorSerializer

class SchoolViewSet(viewsets.ModelViewSet):
    permission_classes = [isAdmin]
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

class SalesHistoryListView(APIView):
    '''
    SalesHistoryView List, Post View

    *query performance differs by using select_related, and prefetch related
    '''

    @extend_schema(
    methods=['get'],
    parameters= [OpenApiParameter('hospital_id', OpenApiTypes.STR, OpenApiParameter.QUERY, required= False)],
    responses={200: SalesHistorySerializer(many=True)},
    # more customizations
    )
    def get(self, request):
        '''
        no parameter:
        
        list: returns The entire list of sales history, ordered by modified date, and hospital id
        
        parameter hospital:
        
        list: returns The filtered list of saleshistory on a hospital id
        params: hospital (hospital_id: str)
        '''
        
        hospital = request.query_params.get('hospital', None)
        
        if hospital is not None:
            history = SalesHistory.objects.filter(hospital=hospital)\
                                          .order_by('-modified_at', 'hospital')\
                                          .select_related('hospital__manager', 'hospital__director')
        else:
            history = SalesHistory.objects.all().order_by('-modified_at', 'hospital')\
                                                .select_related('hospital__manager', 'hospital__director')
           
        serializer = SalesHistorySerializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    @extend_schema(
        methods=['POST'],
        request = SalesHistoryCreateSerializer,
        responses = {201: SalesHistoryCreateSerializer, 400:{'description': 'Invalid Parameters', 'example': {'description': 'Invalid Parameters'}}}
        # more customizations
    )
    def post(self, request, format=None):
        '''
        post: creates new saleshistory

        required: hospital_id, status: (A,B,O,F,P), content
        
        permission: need to be manager of hospital
        '''
        
        serializer = SalesHistoryCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    allowed_methods = ['get', 'post']


class SalesHistoryDetailsView(APIView):
    '''
    SalesHistoryView Based on saleshistory id(pk)

    ** Requires Permission (Hospital Manager) or Admin
    '''
    
    def get_object(self, pk):
        try:
            return SalesHistory.objects.get(pk=pk)
        except SalesHistory.DoesNotExist:
            return Response({'pk not found'}, status=status.HTTP_404_NOT_FOUND)

    def check_owner(self, obj):
        # Checks if user is the manager of the hospital
        return (obj.hospital.manager == self.request.user) or (self.request.user.is_admin)
    
    @extend_schema(
        methods=['GET'],
        responses = {200: SalesHistorySerializer, 404:{'description': 'Invalid saleshistory id(pk)', 'example': {'description': 'Invalid saleshistory id(pk)'}}},
        # more customizations
    )
    def get(self, request, pk=None):
        '''
        get: returns single saleshistory based on pk(id:int)
        '''
        history = self.get_object(pk)                            
        serializer = SalesHistorySerializer(history)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    @extend_schema(
        methods=['PUT'],
        parameters=[
          OpenApiParameter("id (history)", OpenApiParameter.PATH, required=True),
        ],
        request = SalesHistoryCreateSerializer,
        responses = {200: SalesHistorySerializer, 
                     404: {'description': 'Invalid saleshistory id(pk)', 'example': {'description': 'Invalid saleshistory id(pk)'}},
                     403: {'description': 'Insufficient Permission', 'example': {'description': 'Insufficient Permission'}}}
        # more customizations
    )
    def put(self, request, pk):
        '''
        put: updates saleshistory
        permission: need to be manager of hospital & owner of history
        '''
        item = self.get_object(pk)
        
        # Checks for owner permission
        if not self.check_owner(item):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = SalesHistoryCreateSerializer(instance=item, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)


    @extend_schema(
        methods=['PATCH'],
        description='partial update saleshistory only requires id',
        parameters=[
          OpenApiParameter("id (history)", OpenApiParameter.PATH, required=True)
        ],
        request = SalesHistoryCreateSerializer,
        responses = {200: SalesHistorySerializer,
                     404: {'description': 'Invalid saleshistory id(pk)', 'example': {'description': 'Invalid saleshistory id(pk)'}},
                     403: {'description': 'Insufficient Permission', 'example': {'description': 'Insufficient Permission'}}}
        # more customizations
    )
    def patch(self, request, pk):
        '''
        patch: 	partially updates saleshistory
        permission: need to be manager of hospital & owner of history 
        
        '''
        item = self.get_object(pk)

        if not self.check_owner(item):
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = SalesHistoryCreateSerializer(instance=item, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(data=serializer.error_messages, status=status.HTTP_404_NOT_FOUND)
    
    @extend_schema(
        methods=['DELETE'],
        parameters = [OpenApiParameter("id (history)", OpenApiParameter.PATH, required=True)],
        responses={204: 'No content',
                   404: {'description': 'Invalid saleshistory id(pk)', 'example': {'description': 'Invalid saleshistory id(pk)'}},
                   403: {'description': 'Insufficient Permission', 'example': {'description': 'Insufficient Permission'}}}
    )
    def delete(self, request, pk):
        '''
        Delete History
        
        permission: need to be manager of hospital & owner of history
        '''
        item = self.get_object(pk)

        if not self.check_owner(item):
            return Response(status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(item)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
    
    allowed_methods = ['get','put','patch','delete']

class SalesHistoryRecentView(APIView):
    '''
    SalesHistoryView List Sales History of current logged in user
    '''
    allowed_methods = ['get']
    
    @extend_schema(
        methods=['GET'],
        responses = {200: SalesHistoryRecentSerializer(many=True)},
        # more customizations
    )
    def get(self, request):
        '''
        get: returns list of saleshistories created by the current user logged in
        '''
    
        history = SalesHistory.objects.filter(hospital__manager=request.user) \
                                        .order_by('-modified_at') \
                                        .select_related('hospital__manager')

        serializer = SalesHistoryRecentSerializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class SalesHistoryHospitalView(APIView):
    '''
    SalesHistoryView based on the hospital(pk)
    '''
    allowed_methods = ['get']
    
    @extend_schema(
    methods=['get'],
    parameters=[
        OpenApiParameter("pk (hospital)", OpenApiParameter.PATH, required=True), 
    ],
    responses={200: SalesHistorySerializer(many=True)},
    )
    def get(self, request, hospital=None):
        '''
        list: Returns The list of sales history, based on a hospital pk (요양기호)
        '''
        history = SalesHistory.objects.filter(hospital=hospital)\
                                      .order_by('-modified_at', 'hospital')\
                                      .select_related('hospital__manager', 'hospital__director')                
                                      
        serializer = SalesHistorySerializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DashboardView(APIView):
    '''
    Dashboard View various insightful data
    
    '''
    @extend_schema(
    methods=['get'],
    responses={200: DashboardSerializer(many=True)},
    )
    def get(self, request):
        '''
        list: returns various insightful stats in serialized forms  
        '''
        from django.db.models import Count, F
        from django.db.models.functions import TruncDate
    
        # saleshistory count by status:
        status_cnt = SalesHistory.objects.values('status').annotate(count = Count('status'))
        ## 'status' : 'A', 'count': 2 // charfield, integerfield

        status_cnt = StatusCountSerializer(status_cnt, many=True)

        # saleshistory count by date:
        date_cnt = SalesHistory.objects.annotate(date = TruncDate('modified_at')).values('date').annotate(count=Count('date'))

        ## 'date':datetime.date(2023,5,16), 'count':2 // Datefield, integerfield
        date_cnt = DateCountSerializer(date_cnt, many=True)
        
        # saleshistory count by user: 
        user_cnt = SalesHistory.objects.values('hospital__manager').annotate(count=Count('hospital__manager'))
        
        user_cnt = UserCountSerializer(user_cnt, many=True)
        ## 'hospital__manager' : 2, 'count': 2 // integerfield, integerfield

        total_cnt = {
            'user_cnt' : user_cnt.data,
            'date_cnt' : date_cnt.data,
            'status_cnt' : status_cnt.data
        }
        dashboard = DashboardSerializer(total_cnt)

        return Response(dashboard.data, status=status.HTTP_200_OK)


           
    
####
#### This Function is for Testing Purposes ONLY
####

@api_view(['POST'])
def hospital_test_data(request):
    '''
    *Test용* 심평원 api를 fetch하여 db에 저장하는 view
    '''
    hosp_data = get_hospinfo_openapi()
    for key in hosp_data.keys():
        hosp_data[key]['hospital_id'] = key
        new_hosp = Hospital(**hosp_data[key])
        new_hosp.save()
    
    return ('/hospitals')
