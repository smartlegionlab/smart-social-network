from rest_framework.permissions import IsAuthenticated
from apps.core.views.base import BaseListView
from apps.users.serializers.users.public_users import UserPublicSerializer
from apps.users.models import User


class UserPublicListView(BaseListView):
    model = User
    serializer_class = UserPublicSerializer
    permission_classes = [IsAuthenticated]
    search_fields = [
        'first_name',
        'last_name',
    ]
    order_fields = [
        'updated_at',
        'created_at',
    ]
