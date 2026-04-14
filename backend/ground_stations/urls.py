"""
Ground Stations URLs for CCP O2M.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GroundStationViewSet, CommunicationSlotViewSet, ForbiddenZoneViewSet
)

router = DefaultRouter()
router.register(r'', GroundStationViewSet, basename='ground-stations')
router.register(r'slots', CommunicationSlotViewSet, basename='slots')
router.register(r'forbidden-zones', ForbiddenZoneViewSet, basename='forbidden-zones')

urlpatterns = [
    path('', include(router.urls)),
]
