import os.path
import time
from django.conf import settings
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from accounts.permissions import IsExpertUser
from .models import (Case, CasePerson, CaseService, CaseLog, CasePartner, CompanySubject, HeadRelative)
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .serializers import (AdminCasePersonSerializer, CasePersonSerializer, CompanySubjectSerializer,
                          CaseServiceSerializer, CasePartnerSerializer, CaseHeadRelativeSerializer,
                          CaseLogUpdateSerializer, CaseLogRetrieveSerializer, ExpertCaseRetrieveSerializer,
                          ExpertCaseListSerializer, AdminCaseUpdateSerializer, AdminCaseCreateSerializer,
                          AdminCaseRetrieveSerializer, AdminCaseListSerializer, AdminHeadRelativeSerializer,
                          AdminCasePartnerSerializer, AdminCaseServiceSerializer, AdminCompanySubjectSerializer)
import shutil
import sys
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import case_log_submit
class AdminCaseListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        return Case.objects.filter(admin=self.request.user).all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AdminCaseCreateSerializer
        return AdminCaseListSerializer
class AdminCaseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        return Case.objects.filter(admin=self.request.user).all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AdminCaseUpdateSerializer
        return AdminCaseRetrieveSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # بکاپ گرفتن از فایل‌های مرتبط با کیس
            if instance.passport:
                old_file_path = os.path.join(settings.MEDIA_ROOT, instance.passport.path)
                if os.path.isfile(old_file_path):
                    new_file_path = os.path.join(settings.MEDIA_ROOT, 'backup',
                                                 f'client/{str(instance.id)}/passport/{time.time()}'
                                                 f'_{os.path.basename(old_file_path)}')
                    os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
                    shutil.move(old_file_path, new_file_path)

            if instance.image:
                old_file_path = os.path.join(settings.MEDIA_ROOT, instance.image.path)
                if os.path.isfile(old_file_path):
                    new_file_path = os.path.join(settings.MEDIA_ROOT, 'backup',
                                                 f'client/{str(instance.id)}/image/{time.time()}'
                                                 f'_{os.path.basename(old_file_path)}')
                    os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
                    shutil.move(old_file_path, new_file_path)

            if instance.case_logs:
                for log in instance.case_logs.all():
                    if log.file:
                        old_file_path = os.path.join(settings.MEDIA_ROOT, log.file.path)
                        if os.path.isfile(old_file_path):
                            new_file_path = os.path.join(settings.MEDIA_ROOT, 'backup',
                                                         f'client/{str(instance.id)}/logs/{log.id}/{time.time()}'
                                                         f'_{os.path.basename(old_file_path)}')
                            os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
                            shutil.move(old_file_path, new_file_path)

            # حذف فولدر و فایل‌های مرتبط با کیس
            folder_path = os.path.join(settings.MEDIA_ROOT, f'client/{str(instance.id)}')
            if os.path.isdir(folder_path):
                shutil.rmtree(folder_path)

            # فراخوانی متد اصلی destroy
            response = super().destroy(request, *args, **kwargs)
            return response
        except Exception as e:
            print(f'Error in Case Delete : {e}', file=sys.stderr)
            return Response(f'Error in Case Delete : {e}')

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # بکاپ گرفتن از فایل‌های آپلود شده
            if request.data.get('passport') is not None and instance.passport:
                old_file_path = os.path.join(settings.MEDIA_ROOT, instance.passport.path)
                if os.path.isfile(old_file_path):
                    new_file_path = os.path.join(settings.MEDIA_ROOT, 'backup',
                                                 f'client/{str(instance.id)}/passport/{time.time()}'
                                                 f'_{os.path.basename(old_file_path)}')
                    os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
                    shutil.move(old_file_path, new_file_path)

            if request.data.get('image') is not None and instance.image:
                if instance.image:
                    old_file_path = os.path.join(settings.MEDIA_ROOT, instance.image.path)
                    if os.path.isfile(old_file_path):
                        new_file_path = os.path.join(settings.MEDIA_ROOT, 'backup',
                                                     f'client/{str(instance.id)}/image/{time.time()}'
                                                     f'_{os.path.basename(old_file_path)}')
                        os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
                        shutil.move(old_file_path, new_file_path)

            # فراخوانی متد اصلی برای بروزرسانی
            response = super().update(request, *args, **kwargs)
            return response
        except Exception as e:
            print(f'Error in Case Update : {e}', file=sys.stderr)
            return Response(f'Error in Case Update : {e}')


class AdminCompanySubjectListCreateView(ListCreateAPIView):
    queryset = CompanySubject.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [JSONParser]
    serializer_class = AdminCompanySubjectSerializer
class AdminCompanySubjectRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = CompanySubject.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [JSONParser]
    serializer_class = AdminCompanySubjectSerializer
class AdminCasePartnerListCreateView(ListCreateAPIView):
    queryset = CasePartner.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [JSONParser]
    serializer_class = AdminCasePartnerSerializer
class AdminCasePartnerRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = CasePartner.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [JSONParser]
    serializer_class = AdminCasePartnerSerializer
class AdminCaseServiceListCreateView(ListCreateAPIView):
    queryset = CaseService.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [JSONParser]
    serializer_class = AdminCaseServiceSerializer
class AdminCaseServiceRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = CaseService.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [JSONParser]
    serializer_class = AdminCaseServiceSerializer
class AdminHeadRelativeListCreateView(ListCreateAPIView):
    queryset = HeadRelative.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [JSONParser]
    serializer_class = AdminHeadRelativeSerializer
class AdminHeadRelativeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = HeadRelative.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [JSONParser]
    serializer_class = AdminHeadRelativeSerializer
class AdminCasePersonListCreateView(ListCreateAPIView):
    queryset = CasePerson.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [JSONParser]
    serializer_class = AdminCasePersonSerializer
class AdminCasePersonRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = CasePerson.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [JSONParser]
    serializer_class = AdminCasePersonSerializer
class AdminCaseCancelView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, pk):
        try:
            case = Case.objects.get(pk=pk)
            inprogress_log = CaseLog.objects.filter(
                case=case,
                substep_status='INPROGRESS'
            ).first()
            inprogress_log.substep_status = 'CANCELED'
            inprogress_log.save()
            case.case_status = 'CANCELED'
            case.save()
            return Response('done')
        except Exception as e:
            print(f'Error in Case Cancel : {e}', file=sys.stderr)
            return Response(f'Error in Case Cancel : {e}')

class ExpertCaseList(APIView):
    permission_classes = [IsAuthenticated, IsExpertUser]

    def get(self, request):
        try:
            cases = Case.objects.filter(
                expert=self.request.user,
                case_logs__substep__doer='EXPERT',
            ).distinct()
            serlialized = ExpertCaseListSerializer(cases, many=True)
            data = {
                'cases': serlialized.data
            }
            return Response(data)
        except Exception as e:
            print(f'Error in ExpertCaseList : {e}', file=sys.stderr)
            return Response(f'Error in ExpertCaseList : {e}')
class ExpertCaseDetail(APIView):
    permission_classes = [IsAuthenticated, IsExpertUser]

    def get(self, request, pk):
        try:
            case = Case.objects.filter(
                expert=self.request.user,
                id=pk
            ).first()
            if case is None:
                return Response({
                    'message': 'Case not found'
                }, status=404)
            serlialized = ExpertCaseRetrieveSerializer(case)
            data = {
                'case': serlialized.data
            }
            return Response(data)
        except Exception as e:
            print(f'Error in ExpertCaseDetail : {e}', file=sys.stderr)
            return Response(f'Error in ExpertCaseDetail : {e}')

class CaseLogRetrieveUpdateView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]
    queryset = CaseLog.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CaseLogUpdateSerializer
        return CaseLogRetrieveSerializer

    def update(self, request, *args, **kwargs):
        try:
            not_updated_instance = self.get_object()
            updated = super().update(request, *args, **kwargs)
            case_log_submit(not_updated_instance, request, *args, **kwargs)
            return updated
        except Exception as e:
            print(f'Error in CaseLog Update : {e}', file=sys.stderr)
            return Response(f'Error in CaseLog Update : {e}')
class HomePageCaseLogRetrieveView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            current_log = CaseLog.objects.get(pk=pk)
            inprogress_previous_log = (CaseLog.objects.filter(case=current_log.case)
                                       .exclude(substep_status='INPROGRESS').order_by('-id').first())
            data = {
                'current_log': CaseLogRetrieveSerializer(current_log).data,
                'inprogress_previous_log': CaseLogRetrieveSerializer(inprogress_previous_log).data
                if inprogress_previous_log else None
            }
            return Response(data)
        except Exception as e:
            print(f'Error in HomePageCaseLogRetrieve : {e}', file=sys.stderr)
            return Response(f'Error in HomePageCaseLogRetrieve : {e}')

class CaseRelativesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, requset, pk):
        try:
            headrelatives = HeadRelative.objects.filter(case_id=pk).all()
            serialized = CaseHeadRelativeSerializer(headrelatives, many=True, allow_null=False)
            data = {
                'headrelatives': serialized.data
            }
            return Response(data)
        except Exception as e:
            print(f'error in Caseheadrelatives View :{e}', file=sys.stderr)
            return Response(f'error in Caseheadrelatives View:{e}')
class CasePartnersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, requset, pk):
        try:
            casepartners = CasePartner.objects.filter(case_id=pk).all()
            serialized = CasePartnerSerializer(casepartners, many=True, allow_null=False)
            data = {
                'casepartners': serialized.data
            }
            return Response(data)
        except Exception as e:
            print(f'error in CasePartners View :{e}', file=sys.stderr)
            return Response(f'error in CasePartners View:{e}')
class CaseServiceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, requset, pk):
        try:
            caseservices = CaseService.objects.filter(case_id=pk).all()
            serialized = CaseServiceSerializer(caseservices, many=True, allow_null=False)
            data = {
                'caseservices': serialized.data
            }
            return Response(data)
        except Exception as e:
            print(f'error in CaseService View :{e}', file=sys.stderr)
            return Response(f'error in CaseService View:{e}')
class CompanySubjectView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, requset, pk):
        try:
            companysubjects = CompanySubject.objects.filter(case_id=pk).all()
            serialized = CompanySubjectSerializer(companysubjects, many=True, allow_null=False)
            data = {
                'companysubjects': serialized.data
            }
            return Response(data)
        except Exception as e:
            print(f'error in CompanySubject View :{e}', file=sys.stderr)
            return Response(f'error in CompanySubject View:{e}')
class CasePersonView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, requset, pk):
        try:
            casepersons = CasePerson.objects.filter(case_id=pk).all()
            serialized = CasePersonSerializer(casepersons, many=True, allow_null=False)
            data = {
                'casepersons': serialized.data
            }
            return Response(data)
        except Exception as e:
            print(f'error in CasePerson View :{e}', file=sys.stderr)
            return Response(f'error in CasePerson View:{e}')
