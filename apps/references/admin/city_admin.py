from django.contrib import admin

from ..models.city import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'region')
    search_fields = ('name', 'region')
