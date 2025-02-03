from rest_framework.serializers import (CharField, SerializerMethodField,
                                        ModelSerializer, StringRelatedField, PrimaryKeyRelatedField)
from .models import Case, CasePerson, CaseSubStep, HeadRelative, CasePartner, CaseService, CompanySubject, CaseLog


class AdminHeadRelativeSerializer(ModelSerializer):
    case = PrimaryKeyRelatedField(queryset=Case.objects.all())

    class Meta:
        model = HeadRelative
        fields = '__all__'


class AdminCasePartnerSerializer(ModelSerializer):
    case = PrimaryKeyRelatedField(queryset=Case.objects.all())

    class Meta:
        model = CasePartner
        fields = '__all__'


class AdminCaseServiceSerializer(ModelSerializer):
    case = PrimaryKeyRelatedField(queryset=Case.objects.all())

    class Meta:
        model = CaseService
        fields = '__all__'


class AdminCompanySubjectSerializer(ModelSerializer):
    case = PrimaryKeyRelatedField(queryset=Case.objects.all())

    class Meta:
        model = CompanySubject
        fields = '__all__'


class AdminCasePersonSerializer(ModelSerializer):
    class Meta:
        model = CasePerson
        fields = '__all__'


class LatestCaseLogSerializer(ModelSerializer):
    substep = StringRelatedField()

    class Meta:
        model = CaseLog
        fields = ['substep']


class AdminCaseLogProfileSerializer(ModelSerializer):
    substep = StringRelatedField()
    substep_status = CharField(source='get_substep_status_display')

    class Meta:
        model = CaseLog
        exclude = ['case', 'created_at', 'updated_at', 'description']


class AdminCaseListSerializer(ModelSerializer):
    latest_step = SerializerMethodField()

    class Meta:
        model = Case
        fields = ['id', 'head_first_name', 'head_last_name', 'image', 'latest_step']

    @staticmethod
    def get_latest_step(obj):
        latest_step = obj.case_logs.order_by('-id').first()
        return LatestCaseLogSerializer(latest_step).data if latest_step else None


class AdminCaseRetrieveSerializer(ModelSerializer):
    case_logs = SerializerMethodField()
    case_status = CharField(source='get_case_status_display')
    work_address = CharField(source='caseperson.work_address', read_only=True)
    home_address = CharField(source='caseperson.home_address', read_only=True)
    national_id = CharField(source='caseperson.national_id', read_only=True)
    birth_year = CharField(source='caseperson.birth_year', read_only=True)

    class Meta:
        model = Case
        exclude = ['created_at', 'updated_at']
        fields = '__all__'

    @staticmethod
    def get_case_logs(obj):
        logs = obj.case_logs.order_by('id').all()
        return AdminCaseLogProfileSerializer(logs, many=True).data


class AdminCaseCreateSerializer(ModelSerializer):
    class Meta:
        model = Case
        exclude = ['created_at', 'updated_at', 'admin']
        extra_kwargs = {
            'head_first_name': {'required': True},
            'head_last_name': {'required': True}
        }

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['admin'] = user
        return super().create(validated_data)


class AdminCaseUpdateSerializer(ModelSerializer):
    class Meta:
        model = Case
        exclude = ['created_at', 'updated_at', 'admin']


class ExpertCaseListSerializer(ModelSerializer):
    latest_step = SerializerMethodField()

    class Meta:
        model = Case
        fields = ['id', 'head_first_name', 'head_last_name', 'image', 'latest_step']

    @staticmethod
    def get_latest_step(obj):
        latest_step = obj.case_logs.order_by('-id').first()
        return LatestCaseLogSerializer(latest_step).data if latest_step else None


class ExpertCaseLogProfileSerializer(ModelSerializer):
    substep = StringRelatedField()

    class Meta:
        model = CaseLog
        exclude = ['case', 'created_at', 'updated_at']


class ExpertCaseRetrieveSerializer(ModelSerializer):
    case_logs = SerializerMethodField()

    class Meta:
        model = Case
        exclude = ['created_at', 'updated_at']

    @staticmethod
    def get_case_logs(obj):
        logs = obj.case_logs.order_by('id').all()
        return ExpertCaseLogProfileSerializer(logs, many=True).data


class ExpertProfileCaseListSerializer(ModelSerializer):
    latest_step = SerializerMethodField()

    class Meta:
        model = Case
        fields = ['id', 'head_first_name', 'head_last_name', 'image', 'latest_step']

    @staticmethod
    def get_latest_step(obj):
        latest_step = obj.case_logs.order_by('-id').first()
        return LatestCaseLogSerializer(latest_step).data if latest_step else None


class CaseSubStepSerializer(ModelSerializer):
    type = CharField(source='get_type_display')

    class Meta:
        model = CaseSubStep
        fields = ['substep_name', 'description', 'type']


class CaseLogRetrieveSerializer(ModelSerializer):
    substep = CaseSubStepSerializer()
    substep_status = CharField(source='get_substep_status_display')

    class Meta:
        model = CaseLog
        exclude = ['created_at', 'updated_at']


class CaseLogUpdateSerializer(ModelSerializer):
    class Meta:
        model = CaseLog
        exclude = ['created_at', 'updated_at', 'substep_status', 'case', 'substep']


class CaseHeadRelativeSerializer(ModelSerializer):
    class Meta:
        model = HeadRelative
        exclude = ['created_at', 'updated_at', 'case']


class CasePartnerSerializer(ModelSerializer):
    class Meta:
        model = CasePartner
        exclude = ['created_at', 'updated_at', 'case']


class CaseServiceSerializer(ModelSerializer):
    class Meta:
        model = CaseService
        exclude = ['created_at', 'updated_at', 'case']


class CompanySubjectSerializer(ModelSerializer):
    class Meta:
        model = CompanySubject
        exclude = ['created_at', 'updated_at', 'case']


class CasePersonSerializer(ModelSerializer):
    class Meta:
        model = CasePerson
        exclude = ['created_at', 'updated_at', 'case']
