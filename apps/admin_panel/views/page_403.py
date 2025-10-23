from django.shortcuts import render


def custom_403_view(request, exception=None):
    _ = exception
    return render(request, 'admin_panel/403.html', status=403)
