"""
Flight Tasks serializers for CCP O2M.
"""
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import FlightTaskGroup, FlightTask


class FlightTaskGroupListSerializer(serializers.ModelSerializer):
    """Flight task group list serializer."""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    total_tasks = serializers.IntegerField(read_only=True)
    imaging_tasks_count = serializers.IntegerField(read_only=True)
    dump_tasks_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = FlightTaskGroup
        fields = [
            'id', 'group_number', 'name', 'status', 'status_display',
            'start_time', 'end_time', 'total_tasks',
            'imaging_tasks_count', 'dump_tasks_count',
            'created_by_name', 'created_at'
        ]


class FlightTaskGroupDetailSerializer(serializers.ModelSerializer):
    """Flight task group detail serializer."""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    tasks = serializers.SerializerMethodField()
    
    class Meta:
        model = FlightTaskGroup
        fields = '__all__'
    
    def get_tasks(self, obj):
        tasks = obj.flight_tasks.all()
        return FlightTaskListSerializer(tasks, many=True).data


class FlightTaskListSerializer(serializers.ModelSerializer):
    """Flight task list serializer."""
    task_type_display = serializers.CharField(source='get_task_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    satellite_name = serializers.CharField(source='satellite.name', read_only=True)
    
    class Meta:
        model = FlightTask
        fields = [
            'id', 'task_number', 'group', 'task_type', 'task_type_display',
            'status', 'status_display', 'satellite', 'satellite_name',
            'start_time', 'end_time', 'duration_seconds',
            'roll_angle', 'data_volume_gb'
        ]


class FlightTaskSerializer(GeoFeatureModelSerializer):
    """Flight task detail serializer."""
    task_type_display = serializers.CharField(source='get_task_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    execution_quality_display = serializers.CharField(source='get_execution_quality_display', read_only=True)
    satellite_name = serializers.CharField(source='satellite.name', read_only=True)
    ground_station_name = serializers.CharField(source='ground_station.name', read_only=True)
    request_number = serializers.CharField(source='imaging_request.request_number', read_only=True)
    
    class Meta:
        model = FlightTask
        geo_field = 'swath_geometry'
        fields = [
            'id', 'task_number', 'group', 'task_type', 'task_type_display',
            'status', 'status_display', 'satellite', 'satellite_name',
            'start_time', 'end_time', 'duration_seconds',
            'imaging_request', 'request_number', 'opportunity',
            'roll_angle', 'pitch_angle', 'swath_geometry',
            'ground_station', 'ground_station_name', 'data_volume_gb',
            'kup_status', 'execution_result', 'execution_quality', 'execution_quality_display',
            'created_at', 'executed_at'
        ]
