"""
External integrations URLs for CCP O2M.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('export/tasks/', views.export_tasks, name='export-tasks'),
    path('export/satellites/', views.export_satellites, name='export-satellites'),
    path('export/schedule/', views.export_schedule, name='export-schedule'),
]
