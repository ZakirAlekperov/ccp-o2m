"""
Planning serializers for CCP O2M.
"""
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import ForecastResult, ImagingOpportunity


class ForecastResultListSerializer(serializers.ModelSerializer):
    """Forecast result list serializer."""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = ForecastResult
        fields = [
            'id', 'name', 'status', 'status_display',
            'start_date', 'end_date', 'is_current',
            'total_requests', 'processed_requests', 'total_opportunities',
            'created_by_name', 'created_at'
        ]


class ForecastResultSerializer(serializers.ModelSerializer):
    """Forecast result detail serializer."""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = ForecastResult
        fields = '__all__'


class ImagingOpportunitySerializer(GeoFeatureModelSerializer):
    """Imaging opportunity serializer."""
    satellite_name = serializers.CharField(source='satellite.name', read_only=True)
    request_number = serializers.CharField(source='request.request_number', read_only=True)
    
    class Meta:
        model = ImagingOpportunity
        geo_field = 'swath_geometry'
        fields = [
            'id', 'satellite', 'satellite_name', 'request', 'request_number',
            'start_time', 'end_time', 'duration_seconds',
            'swath_geometry', 'roll_angle', 'sun_elevation', 'sun_azimuth',
            'score', 'is_selected'
        ]


class ForecastRequestSerializer(serializers.Serializer):
    """Forecast request serializer."""
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False, allow_blank=True)
    start_date = serializers.DateTimeField(required=True)
    end_date = serializers.DateTimeField(required=True)
    satellite_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )
    request_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )


class PlanningRequestSerializer(serializers.Serializer):
    """Planning request serializer."""
    start_time = serializers.DateTimeField(required=True)
    end_time = serializers.DateTimeField(required=True)
    interval_hours = serializers.IntegerField(default=12, min_value=6, max_value=24)
    satellite_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )
    request_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )
