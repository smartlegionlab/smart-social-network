from django.shortcuts import render

from apps.admin_panel.decorators.superuser import superuser_required
from apps.core.utils.paginator import CachedCountPaginator
from apps.references.models.city import City


@superuser_required
def city_list_view(request):
    city_list = City.objects.all()
    paginate_by = 50
    count = city_list.count()
    paginator = CachedCountPaginator(city_list, paginate_by, count)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'is_exists': count > 0,
        'count': count,
    }

    return render(request, 'admin_panel/references/city_list.html', context)
