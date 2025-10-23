from django.urls import path

from apps.visits.views.guest_visits_remove import guest_visits_remove_view
from apps.visits.views.my_visits_remove import my_visits_remove_view
from apps.visits.views.guest_visit_list import guest_visit_list_view
from apps.visits.views.my_visit_list import my_visit_list_view
from apps.visits.views.visit_delete import visit_delete_view

app_name = 'visits'


urlpatterns = [
    path('', guest_visit_list_view, name='guest_visits'),
    path('my/', my_visit_list_view, name='my_visits'),
    path('my/clear/', my_visits_remove_view, name='clear_my_visits'),
    path('guests/clear/', guest_visits_remove_view, name='clear_guests_visits'),
    path('remove/<int:visit_id>/', visit_delete_view, name='remove_visit'),
]
