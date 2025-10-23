from django.contrib import messages
from django.shortcuts import redirect

from apps.admin_panel.decorators.superuser import superuser_required
from apps.references.models.city import City


@superuser_required
def cities_clear_view(request):
    City.objects.all().delete()
    messages.success(request, 'City deleted!')
    return redirect('admin_panel:city_list')
