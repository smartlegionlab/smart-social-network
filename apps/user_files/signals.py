from django.db.models.signals import pre_delete
from django.dispatch import receiver

from apps.user_files.models.doc import DocumentFile


@receiver(pre_delete, sender=DocumentFile)
def doc_delete_handler(sender, instance, **kwargs):
    instance.file.delete(save=False)
