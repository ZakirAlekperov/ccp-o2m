"""
Flight Tasks views for CCP O2M.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import FlightTaskGroup, FlightTask
from .serializers import (
    FlightTaskGroupListSerializer, FlightTaskGroupDetailSerializer,
    FlightTaskSerializer, FlightTaskListSerializer
)


class FlightTaskGroupViewSet(viewsets.ModelViewSet):
    """Flight task group management viewset."""
    queryset = FlightTaskGroup.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['group_number', 'name']
    ordering_fields = ['created_at', 'start_time']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return FlightTaskGroupListSerializer
        return FlightTaskGroupDetailSerializer


class FlightTaskViewSet(viewsets.ModelViewSet):
    """Flight task management viewset."""
    queryset = FlightTask.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'task_type', 'satellite', 'group']
    search_fields = ['task_number']
    ordering_fields = ['start_time', 'created_at']
    ordering = ['start_time']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return FlightTaskListSerializer
        return FlightTaskSerializer
    
    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        """Change task status."""
        task = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(FlightTask.FlightTaskStatus.choices):
            return Response(
                {'error': 'Неверный статус'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        task.status = new_status
        task.save()
        
        return Response(FlightTaskSerializer(task).data)
    
    @action(detail=False, methods=['post'])
    def export_to_kup(self, request):
        """Export tasks to КУП."""
        # TODO: Implement export to КУП
        return Response(
            {'message': 'Экспорт в КУП'},
            status=status.HTTP_501_NOT_IMPLEMENTED
        )
