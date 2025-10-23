from PIL import Image


def validate_image(file):
    if not file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
        return False, 'Invalid file type. Only images are allowed.'

    try:
        img = Image.open(file)
        img.verify()
    except (IOError, SyntaxError):
        return False, 'Uploaded file is not a valid image.'

    return True, ''
