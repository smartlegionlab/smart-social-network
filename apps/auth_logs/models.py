from django.conf import settings
from django.db import models


class UserAuthLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='auth_logs',
        db_index=True,
        null=True,
        blank=True,
    )
    ip = models.GenericIPAddressField()
    user_agent = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    country = models.CharField(max_length=100, blank=True, null=True)
    country_code = models.CharField(max_length=10, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    region_name = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    timezone = models.CharField(max_length=50, blank=True, null=True)
    isp = models.CharField(max_length=100, blank=True, null=True)
    organization = models.CharField(max_length=100, blank=True, null=True)
    as_number = models.CharField(max_length=50, blank=True, null=True)
    is_mobile = models.BooleanField(default=False)
    is_proxy = models.BooleanField(default=False)
    is_hosting = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    is_updated = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'User auth log'
        verbose_name_plural = 'User auth logs'

    def __str__(self):
        return f"{self.user} logged in at {self.timestamp} from {self.ip}"

    def save_with_ip_info(self, *args, **kwargs):
        from apps.core.utils.informers.ip_informer import IPInfoService

        try:
            ip_service = IPInfoService(self.ip)
            ip_data = ip_service.get_info()

            self.country = ip_data.get('country')
            self.country_code = ip_data.get('countryCode')
            self.region = ip_data.get('region')
            self.region_name = ip_data.get('regionName')
            self.city = ip_data.get('city')
            self.zip_code = ip_data.get('zip')
            self.latitude = ip_data.get('lat')
            self.longitude = ip_data.get('lon')
            self.timezone = ip_data.get('timezone')
            self.isp = ip_data.get('isp')
            self.organization = ip_data.get('org')
            self.as_number = ip_data.get('as')
            self.is_mobile = ip_data.get('mobile', False)
            self.is_proxy = ip_data.get('proxy', False)
            self.is_hosting = ip_data.get('hosting', False)
            self.is_updated = True
            return super().save(*args, **kwargs)

        except Exception:
            raise
