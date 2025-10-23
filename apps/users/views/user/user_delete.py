from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required
def user_delete_view(request):
    try:
        request.user.delete()
    except Exception as e:
        print(e)
        messages.error(request, 'Something went wrong while deleting user')
    else:
        messages.success(request, 'User deleted successfully')
    return redirect('users:login')
