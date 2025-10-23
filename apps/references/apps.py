from django.apps import AppConfig


class ReferencesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.references'

    def ready(self):
        import apps.references.signals
