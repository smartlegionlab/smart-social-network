from rest_framework import serializers

from apps.users.models import User


class UserPublicSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d.%m.%Y', read_only=True)
    last_activity = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S', read_only=True)
    date_of_birth = serializers.DateField(format='%d.%m.%Y', read_only=True)
    avatar = serializers.ImageField(read_only=True)
    city_name = serializers.CharField(source='city.name', read_only=True, default='')

    class Meta:
        model = User
        fields = [
            'id',
            'full_name',
            'gender',
            'date_of_birth',
            'age',
            'created_at',
            'is_active',
            'avatar',
            'is_online',
            'last_activity',
            'city_name',
            'username',
        ]

    def get_is_online(self, obj):
        return True if obj.is_online else False
