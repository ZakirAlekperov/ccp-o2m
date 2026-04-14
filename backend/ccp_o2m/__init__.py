"""
CCP O2M - Комплекс целевого планирования
"""
from .celery import app as celery_app

__all__ = ('celery_app',)
