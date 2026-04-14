"""
Ground Stations serializers for CCP O2M.
"""
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import GroundStation, CommunicationSlot, ForbiddenZone


class GroundStationListSerializer(serializers.ModelSerializer):
    """Ground station list serializer."""
    station_type_display = serializers.CharField(source='get_station_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    latitude = serializers.FloatField(read_only=True)
    longitude = serializers.FloatField(read_only=True)
    
    class Meta:
        model = GroundStation
        fields = [
            'id', 'name', 'code', 'station_type', 'station_type_display',
            'status', 'status_display', 'latitude', 'longitude',
            'min_elevation_angle', 'data_rate_mbps', 'created_at'
        ]


class GroundStationDetailSerializer(GeoFeatureModelSerializer):
    """Ground station detail serializer with geometry."""
    station_type_display = serializers.CharField(source='get_station_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = GroundStation
        geo_field = 'location'
        fields = [
            'id', 'name', 'code', 'station_type', 'station_type_display',
            'description', 'location', 'elevation_m',
            'min_elevation_angle', 'max_elevation_angle', 'data_rate_mbps',
            'status', 'status_display', 'created_at', 'updated_at'
        ]


class GroundStationCreateUpdateSerializer(serializers.ModelSerializer):
    """Ground station create/update serializer."""
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)
    
    class Meta:
        model = GroundStation
        fields = [
            'id', 'name', 'code', 'station_type', 'description',
            'latitude', 'longitude', 'elevation_m',
            'min_elevation_angle', 'max_elevation_angle', 'data_rate_mbps',
            'status'
        ]
    
    def create(self, validated_data):
        from django.contrib.gis.geos import Point
        lat = validated_data.pop('latitude')
        lon = validated_data.pop('longitude')
        validated_data['location'] = Point(lon, lat, srid=4326)
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        from django.contrib.gis.geos import Point
        if 'latitude' in validated_data and 'longitude' in validated_data:
            lat = validated_data.pop('latitude')
            lon = validated_data.pop('longitude')
            validated_data['location'] = Point(lon, lat, srid=4326)
        return super().update(instance, validated_data)


class CommunicationSlotSerializer(serializers.ModelSerializer):
    """Communication slot serializer."""
    station_name = serializers.CharField(source='station.name', read_only=True)
    
    class Meta:
        model = CommunicationSlot
        fields = [
            'id', 'station', 'station_name',
            'start_time', 'end_time', 'is_available', 'reserved_for'
        ]


class CommunicationSlotCreateSerializer(serializers.ModelSerializer):
    """Communication slot create serializer."""
    
    class Meta:
        model = CommunicationSlot
        fields = ['station', 'start_time', 'end_time', 'is_available', 'reserved_for']


class ForbiddenZoneSerializer(GeoFeatureModelSerializer):
    """Forbidden zone serializer."""
    station_name = serializers.CharField(source='station.name', read_only=True)
    
    class Meta:
        model = ForbiddenZone
        geo_field = 'area'
        fields = [
            'id', 'station', 'station_name', 'name',
            'area', 'start_time', 'end_time', 'reason'
        ]
