from django.urls import path
from eventing import views

app_name = 'eventing'

urlpatterns = [
 path('home/', views.home_loader, name='home_loader'),
 path('event/list/', views.event_list, name='event_list'),
 path('event/details/<int:event_id>', views.event_details, name='event_details'),
]