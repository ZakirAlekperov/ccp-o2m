"""
Imaging Requests views for CCP O2M.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import ImagingRequest, ImagingRequestAttachment, RequestHistory
from .serializers import (
    ImagingRequestListSerializer, ImagingRequestDetailSerializer,
    ImagingRequestCreateSerializer, ImagingRequestUpdateSerializer,
    StatusChangeSerializer, ImagingRequestAttachmentSerializer
)


class ImagingRequestViewSet(viewsets.ModelViewSet):
    """Imaging request management viewset."""
    queryset = ImagingRequest.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'imaging_type', 'priority', 'created_by']
    search_fields = ['request_number', 'name', 'description']
    ordering_fields = ['created_at', 'priority', 'earliest_start']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ImagingRequestListSerializer
        elif self.action == 'create':
            return ImagingRequestCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ImagingRequestUpdateSerializer
        return ImagingRequestDetailSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            # Check if user can create requests
            return [IsAuthenticated()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        """Change request status."""
        imaging_request = self.get_object()
        serializer = StatusChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        old_status = imaging_request.status
        new_status = serializer.validated_data['new_status']
        comment = serializer.validated_data.get('comment', '')
        
        # Update request status
        imaging_request.status = new_status
        imaging_request.save()
        
        # Create history entry
        RequestHistory.objects.create(
            request=imaging_request,
            from_status=old_status,
            to_status=new_status,
            changed_by=request.user,
            comment=comment or f'Статус изменён с "{old_status}" на "{new_status}"'
        )
        
        return Response(ImagingRequestDetailSerializer(imaging_request).data)
    
    @action(detail=True, methods=['post'])
    def upload_attachment(self, request, pk=None):
        """Upload attachment to request."""
        imaging_request = self.get_object()
        
        if 'file' not in request.FILES:
            return Response(
                {'error': 'Файл не предоставлен'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        file = request.FILES['file']
        file_type = request.data.get('file_type', 'other')
        
        attachment = ImagingRequestAttachment.objects.create(
            request=imaging_request,
            file=file,
            file_type=file_type
        )
        
        return Response(
            ImagingRequestAttachmentSerializer(attachment).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['post'])
    def import_geojson(self, request):
        """Import request from GeoJSON."""
        # TODO: Implement GeoJSON import
        return Response(
            {'message': 'Импорт GeoJSON'},
            status=status.HTTP_501_NOT_IMPLEMENTED
        )
    
    @action(detail=False, methods=['post'])
    def import_shp(self, request):
        """Import request from Shapefile."""
        # TODO: Implement SHP import
        return Response(
            {'message': 'Импорт Shapefile'},
            status=status.HTTP_501_NOT_IMPLEMENTED
        )


class ImagingRequestAttachmentViewSet(viewsets.ModelViewSet):
    """Imaging request attachment viewset."""
    queryset = ImagingRequestAttachment.objects.all()
    serializer_class = ImagingRequestAttachmentSerializer
    permission_classes = [IsAuthenticated]
