from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from eventing import views

urlpatterns = [
    path('', views.home_loader, name='home_loader'),
    path('admin/', admin.site.urls),
    path('eventing/', include('eventing.urls')),
    path('accounts/', include('accounts.urls'))
]


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
