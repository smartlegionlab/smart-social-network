from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from apps.admin_panel.decorators.superuser import superuser_required
from apps.references.forms.city_form import CityForm


@superuser_required
def city_create_view(request):
    success_url = reverse_lazy('admin_panel:city_list')

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'City created!')
            return redirect(success_url)
    else:
        form = CityForm()

    return render(request, 'admin_panel/references/city_form.html', {'form': form})
