from django.shortcuts import redirect, render


class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            if not request.user.is_authenticated:
                return redirect('users:login')
            if not request.user.is_superuser:
                return self.handle_permission_denied(request)

        response = self.get_response(request)
        return response

    def handle_permission_denied(self, request):
        return render(request, 'admin_panel/403.html', status=403)
