from rest_framework.serializers import ModelSerializer, SerializerMethodField, StringRelatedField
from .models import User
from case.models import Case, CaseLog
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.fields import CharField
from case.serializers import ExpertProfileCaseListSerializer

class OngoingStepSerializer(ModelSerializer):
    substep = StringRelatedField()

    class Meta:
        model = CaseLog
        fields = ['id', 'substep']
class ExpertHomePageSerializer(ModelSerializer):
    ongoing_step = SerializerMethodField()

    class Meta:
        model = Case
        fields = ['head_first_name', 'head_last_name', 'image', 'ongoing_step']

    def get_ongoing_step(self, obj):
        ongoing_step = obj.case_logs.order_by('-id').first()
        return OngoingStepSerializer(ongoing_step).data if ongoing_step else None

class AdminHomePageSerializer(ModelSerializer):
    ongoing_step = SerializerMethodField()

    class Meta:
        model = Case
        fields = ['head_first_name', 'head_last_name', 'image', 'ongoing_step']

    def get_ongoing_step(self, obj):
        ongoing_step = obj.case_logs.order_by('-id').first()
        return OngoingStepSerializer(ongoing_step).data if ongoing_step else None

class AdminExpertsListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'profile_image', 'id', 'phone_number']

class UserDetailChatListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'profile_image']

class ExpertProfileSerializer(ModelSerializer):
    sex = CharField(source='get_sex_display')
    expert_cases = ExpertProfileCaseListSerializer(many=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'birthday', 'company_email',
                  'sex', 'profile_image', 'expert_cases']

class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'profile_image']

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser
        return token