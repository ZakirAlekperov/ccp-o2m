"""
Imaging Requests serializers for CCP O2M.
"""
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import ImagingRequest, ImagingRequestAttachment, RequestHistory, RequestStatus


class ImagingRequestListSerializer(serializers.ModelSerializer):
    """Imaging request list serializer."""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    imaging_type_display = serializers.CharField(source='get_imaging_type_display', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    area_km2 = serializers.FloatField(read_only=True)
    
    class Meta:
        model = ImagingRequest
        fields = [
            'id', 'request_number', 'name', 'status', 'status_display',
            'imaging_type', 'imaging_type_display', 'priority',
            'required_resolution', 'earliest_start', 'latest_end',
            'area_km2', 'created_by_name', 'created_at'
        ]


class ImagingRequestDetailSerializer(GeoFeatureModelSerializer):
    """Imaging request detail serializer."""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    imaging_type_display = serializers.CharField(source='get_imaging_type_display', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    area_km2 = serializers.FloatField(read_only=True)
    attachments = serializers.SerializerMethodField()
    history = serializers.SerializerMethodField()
    
    class Meta:
        model = ImagingRequest
        geo_field = 'target_area'
        fields = [
            'id', 'request_number', 'name', 'description',
            'target_area', 'status', 'status_display',
            'imaging_type', 'imaging_type_display',
            'required_resolution', 'priority',
            'earliest_start', 'latest_end',
            'external_id', 'external_system',
            'area_km2', 'created_by_name', 'created_at', 'updated_at',
            'attachments', 'history'
        ]
    
    def get_attachments(self, obj):
        attachments = obj.attachments.all()
        return ImagingRequestAttachmentSerializer(attachments, many=True).data
    
    def get_history(self, obj):
        history = obj.history.all()[:10]  # Last 10 entries
        return RequestHistorySerializer(history, many=True).data


class ImagingRequestCreateSerializer(serializers.ModelSerializer):
    """Imaging request create serializer."""
    
    class Meta:
        model = ImagingRequest
        fields = [
            'name', 'description', 'target_area',
            'imaging_type', 'required_resolution', 'priority',
            'earliest_start', 'latest_end',
            'external_id', 'external_system'
        ]
    
    def create(self, validated_data):
        # Generate request number
        import uuid
        from datetime import datetime
        
        validated_data['request_number'] = f"REQ-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        validated_data['created_by'] = self.context['request'].user
        
        request = super().create(validated_data)
        
        # Create history entry
        RequestHistory.objects.create(
            request=request,
            to_status=request.status,
            changed_by=self.context['request'].user,
            comment='Заявка создана'
        )
        
        return request


class ImagingRequestUpdateSerializer(serializers.ModelSerializer):
    """Imaging request update serializer."""
    
    class Meta:
        model = ImagingRequest
        fields = [
            'name', 'description', 'target_area',
            'imaging_type', 'required_resolution', 'priority',
            'earliest_start', 'latest_end'
        ]


class StatusChangeSerializer(serializers.Serializer):
    """Status change serializer."""
    new_status = serializers.ChoiceField(choices=RequestStatus.choices)
    comment = serializers.CharField(required=False, allow_blank=True)


class ImagingRequestAttachmentSerializer(serializers.ModelSerializer):
    """Imaging request attachment serializer."""
    
    class Meta:
        model = ImagingRequestAttachment
        fields = ['id', 'file', 'file_type', 'uploaded_at']


class RequestHistorySerializer(serializers.ModelSerializer):
    """Request history serializer."""
    from_status_display = serializers.CharField(source='get_from_status_display', read_only=True)
    to_status_display = serializers.CharField(source='get_to_status_display', read_only=True)
    changed_by_name = serializers.CharField(source='changed_by.username', read_only=True)
    
    class Meta:
        model = RequestHistory
        fields = [
            'id', 'from_status', 'from_status_display',
            'to_status', 'to_status_display',
            'changed_by_name', 'comment', 'created_at'
        ]
