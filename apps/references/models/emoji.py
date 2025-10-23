from django.db import models


class Emoji(models.Model):
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Emojis'
        verbose_name = 'Emoji'

    def __str__(self):
        return f"{self.description}"
