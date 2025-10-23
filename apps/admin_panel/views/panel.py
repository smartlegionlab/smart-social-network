from django.shortcuts import render

from apps.admin_panel.decorators.superuser import superuser_required


@superuser_required
def admin_panel_view(request):
    return render(request, 'admin_panel/admin_panel.html', {})
