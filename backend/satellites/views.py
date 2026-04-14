"""
Satellites views for CCP O2M.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Satellite, TLEData, MemoryMask, UnavailabilityPeriod
from .serializers import (
    SatelliteListSerializer, SatelliteDetailSerializer,
    SatelliteCreateUpdateSerializer, TLEDataSerializer, TLEUploadSerializer,
    MemoryMaskSerializer, MemoryMaskCreateSerializer, UnavailabilityPeriodSerializer
)


class SatelliteViewSet(viewsets.ModelViewSet):
    """Satellite management viewset."""
    queryset = Satellite.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'norad_id']
    search_fields = ['name', 'norad_id', 'description']
    ordering_fields = ['name', 'created_at', 'status']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return SatelliteListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return SatelliteCreateUpdateSerializer
        return SatelliteDetailSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Only admin and superuser can modify satellites
            return [IsAuthenticated()]
        return [IsAuthenticated()]
    
    @action(detail=True, methods=['get'])
    def tle_history(self, request, pk=None):
        """Get TLE history for satellite."""
        satellite = self.get_object()
        tle_list = satellite.tle_history.all()[:20]  # Last 20 entries
        serializer = TLEDataSerializer(tle_list, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def upload_tle(self, request, pk=None):
        """Upload new TLE for satellite."""
        satellite = self.get_object()
        serializer = TLEUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Mark previous TLE as not current
        satellite.tle_history.filter(is_current=True).update(is_current=False)
        
        # Create new TLE
        tle = TLEData.objects.create(
            satellite=satellite,
            tle_line1=serializer.validated_data['tle_line1'],
            tle_line2=serializer.validated_data['tle_line2'],
            epoch=serializer.validated_data['epoch'],
            is_current=True
        )
        
        return Response(
            TLEDataSerializer(tle).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['get'])
    def memory_masks(self, request, pk=None):
        """Get memory masks for satellite."""
        satellite = self.get_object()
        masks = satellite.memory_masks.all()
        serializer = MemoryMaskSerializer(masks, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def unavailability_periods(self, request, pk=None):
        """Get unavailability periods for satellite."""
        satellite = self.get_object()
        periods = satellite.unavailability_periods.all()
        serializer = UnavailabilityPeriodSerializer(periods, many=True)
        return Response(serializer.data)


class TLEDataViewSet(viewsets.ReadOnlyModelViewSet):
    """TLE data viewset (read-only)."""
    queryset = TLEData.objects.all()
    serializer_class = TLEDataSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['satellite', 'is_current']


class MemoryMaskViewSet(viewsets.ModelViewSet):
    """Memory mask management viewset."""
    queryset = MemoryMask.objects.all()
    serializer_class = MemoryMaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['satellite', 'is_releasable']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return MemoryMaskCreateSerializer
        return MemoryMaskSerializer


class UnavailabilityPeriodViewSet(viewsets.ModelViewSet):
    """Unavailability period management viewset."""
    queryset = UnavailabilityPeriod.objects.all()
    serializer_class = UnavailabilityPeriodSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['satellite']
