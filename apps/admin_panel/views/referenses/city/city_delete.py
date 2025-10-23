from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

from apps.admin_panel.decorators.superuser import superuser_required
from apps.references.models.city import City


@superuser_required
def city_delete_view(request, pk):
    city = get_object_or_404(City, pk=pk)
    city.delete()
    messages.success(request, 'City deleted!')
    return redirect('admin_panel:city_list')
