from django.contrib import messages
from django.shortcuts import render, redirect

from apps.admin_panel.decorators.superuser import superuser_required
from apps.core.forms import SiteConfigForm
from apps.core.models.site_config import SiteConfig


@superuser_required
def site_config_update_view(request):
    site_config = SiteConfig.objects.first()

    if request.method == 'POST':
        form = SiteConfigForm(request.POST, instance=site_config)
        if form.is_valid():
            form.save()
            messages.success(request, f'Site Config updated!')
            return redirect('admin_panel:site_config')
    else:
        form = SiteConfigForm(instance=site_config)

    return render(request, 'admin_panel/site_config/site_config_form.html', {'form': form})
