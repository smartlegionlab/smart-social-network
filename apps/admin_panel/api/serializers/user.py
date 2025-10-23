from rest_framework import serializers

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    is_online = serializers.SerializerMethodField()
    auth_history_count = serializers.SerializerMethodField()
    date_of_birth = serializers.DateField(format="%d.%m.%Y", required=False)
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")
    updated_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")
    last_activity = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S")
    age = serializers.SerializerMethodField()
    city_name = serializers.CharField(source='city.name', read_only=True, default='')

    class Meta:
        model = User
        fields = '__all__'

    def get_avatar_url(self, obj):
        return obj.get_avatar_url()

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_is_online(self, obj):
        return obj.is_online

    def get_auth_history_count(self, obj):
        return obj.auth_logs.count()

    def get_age(self, obj):
        return obj.age
