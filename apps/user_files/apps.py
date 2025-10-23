from django.apps import AppConfig


class UserFilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.user_files'

    def ready(self):
        import apps.user_files.signals
