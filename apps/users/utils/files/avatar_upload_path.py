import os


def avatar_upload_to(instance, filename):
    return os.path.join('avatars', f'user_{instance.id}', filename)
