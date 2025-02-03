from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsExpertUser
from .serializers import (UserProfileSerializer, AdminExpertsListSerializer, AdminHomePageSerializer,
                          ExpertHomePageSerializer, ExpertProfileSerializer)
from .models import User
from case.models import Case
from rest_framework.response import Response
import sys

class ExpertProfileView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, pk):
        try:
            expert = User.objects.filter(is_staff=False, is_active=True, is_superuser=False).get(pk=pk)
            serializer = ExpertProfileSerializer(expert)
            data = {
                'expert': serializer.data,
                'company_email': expert.serializer.data,
                'birthday': expert.serializer.data
            }
            return Response(data)
        except Exception as e:
            print(f'Error in Expert Profile : {e}', file=sys.stderr)
            return Response(f'Error in Expert Profile : {e}')
class ExpertHomePageView(APIView):
    permission_classes = [IsAuthenticated, IsExpertUser]

    def get(self, request):
        try:
            cases = Case.objects.filter(
                case_status='ONGOING',
                expert=request.user,
                case_logs__substep__doer='EXPERT',
                case_logs__substep_status='INPROGRESS'
            ).distinct()

            serializer = ExpertHomePageSerializer(cases, many=True)
            finished_cases = Case.objects.filter(expert=request.user, case_status='FINISHED').count()
            ongoing_cases = Case.objects.filter(expert=request.user, case_status='ONGOING').count()
            expert_cases = Case.objects.filter(expert=request.user).count()

            data = {
                'cases': serializer.data,
                'finished_cases': finished_cases,
                'ongoing_cases': ongoing_cases,
                'left_cases': expert_cases - finished_cases,
                'success_rate': (finished_cases / expert_cases * 100) if expert_cases > 0 else 0
            }

            return Response(data)
        except Exception as e:
            print(f'Error in Expert Home Page : {e}', file=sys.stderr)
            return Response(f'Error in Expert Home Page : {e}')
class AdminHomePageView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        try:
            admin_cases = Case.objects.filter(
                case_status='ONGOING',
                case_logs__substep__doer='ADMIN',
                case_logs__substep_status='INPROGRESS',
                admin=request.user
            ).distinct()

            cases = AdminHomePageSerializer(admin_cases, many=True)
            finished_cases = Case.objects.filter(case_status='FINISHED').count()
            ongoing_cases = Case.objects.filter(case_status='ONGOING').count()
            total_cases = Case.objects.all().count()

            data = {
                'cases': cases.data,
                'finished_cases': finished_cases,
                'ongoing_cases': ongoing_cases,
                'left_cases': total_cases - finished_cases,
                'success_rate': (finished_cases / total_cases * 100) if total_cases > 0 else 0
            }
            return Response(data)
        except Exception as e:
            print(f'Error in Admin Home Page : {e}', file=sys.stderr)
            return Response(f'Error in Admin Home Page : {e}')
class AdminExpertListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        try:
            experts = User.objects.filter(is_active=True, is_staff=False, is_superuser=False)
            serialized = AdminExpertsListSerializer(experts, many=True)
            data = {
                'experts': serialized.data,
            }
            return Response(data)
        except Exception as e:
            print(f'Error in Admin Expert List : {e}', file=sys.stderr)
            return Response(f'Error in Admin Expert List : {e}')
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            serializer = UserProfileSerializer(request.user)
            data = {
                'user': serializer.data
            }
            return Response(data)
        except Exception as e:
            print(f'Error in User Profile : {e}', file=sys.stderr)
            return Response(f'Error in User Profile : {e}')
