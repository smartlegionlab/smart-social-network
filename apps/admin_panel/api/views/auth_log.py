from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Q

from apps.admin_panel.api.serializers.auth_log import UserAuthLogSerializer
from apps.auth_logs.models import UserAuthLog


class UserAuthLogViewSet(viewsets.ViewSet):
    def list(self, request, user_id=None):
        try:
            draw = int(request.GET.get('draw', 1))
            start = int(request.GET.get('start', 0))
            length = int(request.GET.get('length', 10))
            search_value = request.GET.get('search', '')

            order_column = request.GET.get('order_column')
            order_dir = request.GET.get('order_dir', 'asc')

            queryset = UserAuthLog.objects.filter(user_id=user_id)

            if search_value:
                queryset = queryset.filter(
                    Q(ip__icontains=search_value) |
                    Q(user_agent__icontains=search_value)
                )

            if order_column and order_column.isdigit():
                order_column = int(order_column)
                column_mapping = {
                    0: 'ip',
                    1: 'user_agent',
                    2: 'timestamp',
                }

                if order_column in column_mapping:
                    order_field = column_mapping[order_column]
                    if order_dir == 'desc':
                        order_field = f'-{order_field}'
                    queryset = queryset.order_by(order_field)
            else:
                queryset = queryset.order_by('-timestamp')

            total_records = UserAuthLog.objects.filter(user_id=user_id).count()
            filtered_records = queryset.count()

            queryset = queryset[start:start + length]
            serializer = UserAuthLogSerializer(queryset, many=True)

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
