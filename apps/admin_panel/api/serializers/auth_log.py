from rest_framework import serializers

from apps.auth_logs.models import UserAuthLog


class UserAuthLogSerializer(serializers.ModelSerializer):
    ip_address = serializers.CharField(source='ip')
    timestamp = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S")

    class Meta:
        model = UserAuthLog
        fields = ['id', 'ip_address', 'user_agent', 'timestamp']
