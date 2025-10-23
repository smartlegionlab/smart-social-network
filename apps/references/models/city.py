from django.db import models


class City(models.Model):
    name = models.CharField(max_length=200)
    region = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Cities'
        verbose_name = 'City'
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"
