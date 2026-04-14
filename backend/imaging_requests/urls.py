"""
Imaging Requests URLs for CCP O2M.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ImagingRequestViewSet, ImagingRequestAttachmentViewSet

router = DefaultRouter()
router.register(r'', ImagingRequestViewSet, basename='imaging-requests')
router.register(r'attachments', ImagingRequestAttachmentViewSet, basename='attachments')

urlpatterns = [
    path('', include(router.urls)),
]
