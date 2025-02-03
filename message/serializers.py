from rest_framework.serializers import (CharField, ModelSerializer, SerializerMethodField)
from .models import Message, MessageRecord

class MessageSerializer(ModelSerializer):
    status = CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Message
        fields = '__all__'
class MessageRecordSerializer(ModelSerializer):
    is_writer = SerializerMethodField()

    class Meta:
        model = MessageRecord
        exclude = ['is_deleted']
        extra_kwargs = {
            'message': {'write_only': True},
        }

    def get_is_writer(self, obj):
        return obj.is_written_by(self.context['request'].user)
class MessageRecordRetrieveUpdateDestroySerializer(ModelSerializer):
    class Meta:
        model = MessageRecord
        fields = ['content']
