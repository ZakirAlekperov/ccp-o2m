"""
Satellites URLs for CCP O2M.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SatelliteViewSet, TLEDataViewSet,
    MemoryMaskViewSet, UnavailabilityPeriodViewSet
)

router = DefaultRouter()
router.register(r'', SatelliteViewSet, basename='satellites')
router.register(r'tle-data', TLEDataViewSet, basename='tle-data')
router.register(r'memory-masks', MemoryMaskViewSet, basename='memory-masks')
router.register(r'unavailability', UnavailabilityPeriodViewSet, basename='unavailability')

urlpatterns = [
    path('', include(router.urls)),
]
