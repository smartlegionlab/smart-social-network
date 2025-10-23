

def user_document_upload_to(instance, filename):
    return f'docs/{instance.uploaded_by.id}/{filename}'
