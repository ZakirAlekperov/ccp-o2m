"""
Flight Tasks URLs for CCP O2M.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FlightTaskGroupViewSet, FlightTaskViewSet

router = DefaultRouter()
router.register(r'groups', FlightTaskGroupViewSet, basename='task-groups')
router.register(r'', FlightTaskViewSet, basename='flight-tasks')

urlpatterns = [
    path('', include(router.urls)),
]
