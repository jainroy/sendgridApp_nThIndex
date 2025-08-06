from rest_framework import serializers
from .models import Email


class SendMailSerializer(serializers.Serializer):
    to_mail = serializers.CharField()
    subject = serializers.CharField()
    content = serializers.CharField()

class AddEmailSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    class Meta:
        model = Email
        fields = ('email',)


class SendBulkMailSerializer(serializers.Serializer):
    subject = serializers.CharField()
    content = serializers.CharField()