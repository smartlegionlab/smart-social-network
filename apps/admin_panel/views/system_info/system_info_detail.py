from django.shortcuts import render

from apps.admin_panel.decorators.superuser import superuser_required


@superuser_required
def system_info_detail_view(request):
    return render(request, 'admin_panel/system_info/system_info.html', {})
