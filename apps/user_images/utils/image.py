

def user_image_upload_to(instance, filename):
    return f'images/{instance.uploaded_by.id}/{filename}'
