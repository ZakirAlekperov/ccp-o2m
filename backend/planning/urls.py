"""
Planning URLs for CCP O2M.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'forecasts', views.ForecastResultViewSet, basename='forecasts')
router.register(r'opportunities', views.ImagingOpportunityViewSet, basename='opportunities')

urlpatterns = [
    path('', include(router.urls)),
    path('forecast/', views.run_forecast, name='run-forecast'),
    path('schedule/', views.run_planning, name='run-planning'),
]
