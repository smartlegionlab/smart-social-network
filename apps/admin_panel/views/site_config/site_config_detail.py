from django.shortcuts import render

from apps.admin_panel.decorators.superuser import superuser_required


@superuser_required
def site_config_detail_view(request):
    return render(request, 'admin_panel/site_config/site_config_detail.html')
