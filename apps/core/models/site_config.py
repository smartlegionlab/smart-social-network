from django.db import models

from apps.core.models.singletons import SingletonModel


class SiteConfig(SingletonModel):
    name = models.CharField(max_length=100, default='Smart Social Network')
    description = models.TextField(default='Smart Social Network is a modern and convenient social'
                                           ' network created for comfortable communication.')
    email = models.EmailField(default='')
    phone = models.CharField(max_length=11, default='')
    telegram_bot_token = models.CharField(max_length=100, default='')
    telegram_bot_url = models.URLField(max_length=100, default='')

    @property
    def has_empty_fields(self):
        status = all(
            [
                self.name,
                self.description,
                self.description,
                self.phone,
                self.telegram_bot_token,
                self.telegram_bot_url
            ]
        )
        return status

    def __str__(self):
        return self.name
