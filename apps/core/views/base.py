from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.paginator import Paginator
from django.db.models import Q


class BaseListView(APIView):
    model = None
    serializer_class = None
    search_fields = []
    order_fields = []

    def get_queryset(self, request):
        queryset = self.model.objects.all()
        search_value = request.GET.get('search[value]', '')

        if search_value:
            query = Q()
            for field in self.search_fields:
                query |= Q(**{f"{field}__icontains": search_value})
            queryset = queryset.filter(query)

        return queryset

    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))

        queryset = self.get_queryset(request)

        if isinstance(queryset, Response):
            return queryset

        total_records = queryset.count()

        order_column = request.GET.get('order[0][column]', '0')
        order_dir = request.GET.get('order[0][dir]', 'asc')

        if order_column.isdigit() and int(order_column) < len(self.order_fields):
            order_field = self.order_fields[int(order_column)]
            if order_dir == 'desc':
                order_field = '-' + order_field
            queryset = queryset.order_by(order_field)

        paginator = Paginator(queryset, length)
        page = paginator.get_page(start // length + 1)

        serializer = self.serializer_class(page, many=True)

        return Response({
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': queryset.count(),
            'data': serializer.data
        })
