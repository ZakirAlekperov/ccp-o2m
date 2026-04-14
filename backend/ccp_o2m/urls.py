"""
URL configuration for ccp_o2m project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/satellites/', include('satellites.urls')),
    path('api/ground-stations/', include('ground_stations.urls')),
    path('api/imaging-requests/', include('imaging_requests.urls')),
    path('api/planning/', include('planning.urls')),
    path('api/flight-tasks/', include('flight_tasks.urls')),
    path('api/export/', include('external.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
