from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from apps.user_images.forms.image_upload_form import UserImageForm
from apps.user_images.services import UserImageService


@login_required
def image_upload_view(request):
    if request.method == 'POST':
        form = UserImageForm(request.POST, request.FILES)
        try:
            image = UserImageService.upload_image(request.user, request.POST, request.FILES)
            messages.success(request, 'The image file has been successfully uploaded!')
            return redirect('user_images:user_image_list')
        except ValidationError as e:
            for error in e.messages:
                form.add_error(None, error)
        except Exception as e:
            print(e)
            messages.error(request, 'Error uploading image.')
    else:
        form = UserImageForm()

    context = {
        'form': form,
        'active_page': 'images',
    }
    return render(request, 'user_images/image_upload_form.html', context)
