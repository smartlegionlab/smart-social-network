from django.apps import AppConfig


class UserImagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.user_images'

    def ready(self):
        import apps.user_images.signals
