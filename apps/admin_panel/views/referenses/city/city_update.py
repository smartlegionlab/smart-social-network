from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from apps.admin_panel.decorators.superuser import superuser_required
from apps.references.forms.city_form import CityForm
from apps.references.models.city import City


@superuser_required
def city_update_view(request, pk):

    city = get_object_or_404(City, pk=pk)

    if request.method == 'POST':
        form = CityForm(request.POST, instance=city)
        if form.is_valid():
            form.save()
            messages.success(request, 'City updated!')
            return redirect('admin_panel:city_list')
    else:
        form = CityForm(instance=city)

    return render(request, 'admin_panel/references/city_form.html', {'form': form, 'city': city})
