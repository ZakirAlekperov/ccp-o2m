"""
Satellites serializers for CCP O2M.
"""
from rest_framework import serializers
from rest_framework_gis.serializers import GeoModelSerializer
from .models import Satellite, TLEData, MemoryMask, UnavailabilityPeriod


class SatelliteListSerializer(serializers.ModelSerializer):
    """Satellite list serializer."""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    memory_usage_percent = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Satellite
        fields = [
            'id', 'name', 'norad_id', 'status', 'status_display',
            'swath_width_km', 'max_roll_angle', 'max_memory_gb',
            'current_memory_usage_gb', 'memory_usage_percent',
            'created_at'
        ]


class SatelliteDetailSerializer(serializers.ModelSerializer):
    """Satellite detail serializer."""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    memory_usage_percent = serializers.FloatField(read_only=True)
    current_tle = serializers.SerializerMethodField()
    
    class Meta:
        model = Satellite
        fields = '__all__'
    
    def get_current_tle(self, obj):
        """Get current TLE for satellite."""
        current_tle = obj.tle_history.filter(is_current=True).first()
        if current_tle:
            return TLEDataSerializer(current_tle).data
        return None


class SatelliteCreateUpdateSerializer(serializers.ModelSerializer):
    """Satellite create/update serializer."""
    
    class Meta:
        model = Satellite
        fields = [
            'id', 'name', 'norad_id', 'description',
            'swath_width_km', 'max_roll_angle', 'max_pitch_angle', 'max_yaw_angle',
            'max_memory_gb', 'current_memory_usage_gb',
            'power_consumption_per_image', 'available_power',
            'min_altitude_km', 'max_altitude_km', 'status'
        ]


class TLEDataSerializer(serializers.ModelSerializer):
    """TLE data serializer."""
    satellite_name = serializers.CharField(source='satellite.name', read_only=True)
    
    class Meta:
        model = TLEData
        fields = [
            'id', 'satellite', 'satellite_name',
            'tle_line1', 'tle_line2', 'epoch',
            'uploaded_at', 'is_current'
        ]
        read_only_fields = ['uploaded_at']


class TLEUploadSerializer(serializers.Serializer):
    """TLE upload serializer."""
    tle_line1 = serializers.CharField(max_length=69, required=True)
    tle_line2 = serializers.CharField(max_length=69, required=True)
    epoch = serializers.DateTimeField(required=True)


class MemoryMaskSerializer(serializers.ModelSerializer):
    """Memory mask serializer."""
    satellite_name = serializers.CharField(source='satellite.name', read_only=True)
    
    class Meta:
        model = MemoryMask
        fields = [
            'id', 'satellite', 'satellite_name',
            'start_time', 'end_time', 'size_gb',
            'description', 'is_releasable', 'flight_task_id',
            'created_at'
        ]


class MemoryMaskCreateSerializer(serializers.ModelSerializer):
    """Memory mask create serializer."""
    
    class Meta:
        model = MemoryMask
        fields = [
            'satellite', 'start_time', 'end_time',
            'size_gb', 'description', 'is_releasable'
        ]


class UnavailabilityPeriodSerializer(serializers.ModelSerializer):
    """Unavailability period serializer."""
    satellite_name = serializers.CharField(source='satellite.name', read_only=True)
    
    class Meta:
        model = UnavailabilityPeriod
        fields = [
            'id', 'satellite', 'satellite_name',
            'start_time', 'end_time', 'reason'
        ]
