"""
Planning views for CCP O2M.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import ForecastResult, ImagingOpportunity
from .serializers import (
    ForecastResultSerializer, ForecastResultListSerializer,
    ImagingOpportunitySerializer
)


class ForecastResultViewSet(viewsets.ReadOnlyModelViewSet):
    """Forecast result viewset."""
    queryset = ForecastResult.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'is_current']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ForecastResultListSerializer
        return ForecastResultSerializer


class ImagingOpportunityViewSet(viewsets.ReadOnlyModelViewSet):
    """Imaging opportunity viewset."""
    queryset = ImagingOpportunity.objects.all()
    serializer_class = ImagingOpportunitySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['satellite', 'request', 'is_selected']


@api_view(['POST'])
def run_forecast(request):
    """Run forecasting calculation."""
    # TODO: Implement forecasting with Celery
    return Response(
        {'message': 'Прогнозирование запущено'},
        status=status.HTTP_202_ACCEPTED
    )


@api_view(['POST'])
def run_planning(request):
    """Run planning calculation."""
    # TODO: Implement planning with Celery
    return Response(
        {'message': 'Планирование запущено'},
        status=status.HTTP_202_ACCEPTED
    )
