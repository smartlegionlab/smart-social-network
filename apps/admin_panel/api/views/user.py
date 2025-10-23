from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Q

from apps.admin_panel.api.serializers.user import UserSerializer
from apps.users.models import User


class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            draw = int(request.GET.get('draw', 1))
            start = int(request.GET.get('start', 0))
            length = int(request.GET.get('length', 10))
            search_value = request.GET.get('search[value]', '')

            order_column = request.GET.get('order[0][column]', '')
            order_dir = request.GET.get('order[0][dir]', 'asc')

            queryset = User.objects.all()

            if search_value:
                queryset = queryset.filter(
                    Q(first_name__icontains=search_value) |
                    Q(last_name__icontains=search_value) |
                    Q(email__icontains=search_value) |
                    Q(about_me__icontains=search_value) |
                    Q(telegram_chat_id__icontains=search_value)
                )

            if order_column.isdigit():
                order_column = int(order_column)
                column_mapping = [
                    None,
                    'first_name',
                    'last_activity',
                    'gender',
                    None,
                    'email',
                    'date_of_birth',
                    'date_of_birth',
                    'telegram_chat_id',
                    'is_2fa_enabled',
                    'is_active',
                    'is_superuser',
                    'created_at',
                    'updated_at',
                    'last_activity',
                    None
                ]

                if 0 <= order_column < len(column_mapping) and column_mapping[order_column]:
                    order_field = column_mapping[order_column]
                    if order_dir == 'desc':
                        order_field = f'-{order_field}'
                    queryset = queryset.order_by(order_field)

            total_records = User.objects.count()
            filtered_records = queryset.count()

            queryset = queryset[start:start + length]
            serializer = UserSerializer(queryset, many=True)

            return Response({
                'draw': draw,
                'recordsTotal': total_records,
                'recordsFiltered': filtered_records,
                'data': serializer.data
            })

        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"API Error: {str(e)}", exc_info=True)
            return Response({
                'error': 'Server error',
                'draw': 1,
                'recordsTotal': 0,
                'recordsFiltered': 0,
                'data': []
            }, status=500)
