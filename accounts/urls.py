from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
 path('login/', views.login_operation, name='login'),
 path('logout/', views.logout_operation, name='logout'),
 path('profile/', views.profile_view, name='profile'),
 path('profile/myevent/', views.my_events, name='my_event'),
 path('profile/addnew/', views.add_new_event, name='add_new'),
 path('profile/register/', views.register_user, name='register_user'),
 path('profile/change_password/', views.change_password, name='change_password'),
 path('profile/event_submitted/<int:event_id>', views.event_submitted, name='event_submitted'),
 path('profile/edit_event/<int:event_id>', views.edit_own_event, name='edit_own_event'),
 path('profile/admin_panel/', views.admin_panel, name='admin_panel'),
 path('profile/verify_event/<int:event_id>', views.verify_event, name='verify_event')
]
