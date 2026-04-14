"""
Ground Stations views for CCP O2M.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import GroundStation, CommunicationSlot, ForbiddenZone
from .serializers import (
    GroundStationListSerializer, GroundStationDetailSerializer,
    GroundStationCreateUpdateSerializer, CommunicationSlotSerializer,
    CommunicationSlotCreateSerializer, ForbiddenZoneSerializer
)


class GroundStationViewSet(viewsets.ModelViewSet):
    """Ground station management viewset."""
    queryset = GroundStation.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['station_type', 'status']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'created_at', 'station_type']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return GroundStationListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return GroundStationCreateUpdateSerializer
        return GroundStationDetailSerializer
    
    @action(detail=True, methods=['get'])
    def slots(self, request, pk=None):
        """Get communication slots for station."""
        station = self.get_object()
        slots = station.communication_slots.all()
        
        # Filter by date range if provided
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if start_date and end_date:
            slots = slots.filter(start_time__gte=start_date, end_time__lte=end_date)
        
        serializer = CommunicationSlotSerializer(slots, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def forbidden_zones(self, request, pk=None):
        """Get forbidden zones for station."""
        station = self.get_object()
        zones = station.forbidden_zones.all()
        serializer = ForbiddenZoneSerializer(zones, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def import_zones(self, request, pk=None):
        """Import forbidden zones from CSV."""
        # TODO: Implement CSV import
        return Response(
            {'message': 'Импорт зон запрета из CSV'},
            status=status.HTTP_501_NOT_IMPLEMENTED
        )


class CommunicationSlotViewSet(viewsets.ModelViewSet):
    """Communication slot management viewset."""
    queryset = CommunicationSlot.objects.all()
    serializer_class = CommunicationSlotSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['station', 'is_available']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CommunicationSlotCreateSerializer
        return CommunicationSlotSerializer


class ForbiddenZoneViewSet(viewsets.ModelViewSet):
    """Forbidden zone management viewset."""
    queryset = ForbiddenZone.objects.all()
    serializer_class = ForbiddenZoneSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['station']
