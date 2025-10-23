from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from apps.admin_panel.decorators.superuser import superuser_required
from apps.users.models import User
from apps.admin_panel.services.users.import_export.users_export import UserExportService


@superuser_required
def users_export_view(request, export_format):

    if request.method != 'GET':
        return HttpResponse(status=405)

    try:
        if export_format == 'csv':
            return UserExportService.export_to_csv(User.objects.all())
        elif export_format == 'json':
            return UserExportService.export_to_json(User.objects.all())
        else:
            messages.error(request, "Unsupported export format")
    except Exception as e:
        print(f"Export error: {str(e)}")
        messages.error(request, f"Export error: {str(e)}")

    return redirect(reverse('admin_panel:admin_panel'))
