"""
External integrations views for CCP O2M.
Export functionality.
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_tasks(request):
    """Export imaging tasks to various formats."""
    export_format = request.query_params.get('format', 'json')
    
    if export_format == 'json':
        return Response({'message': 'Export to JSON'})
    elif export_format == 'xlsx':
        return Response({'message': 'Export to XLSX'})
    elif export_format == 'csv':
        return Response({'message': 'Export to CSV'})
    else:
        return Response(
            {'error': 'Неподдерживаемый формат'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_satellites(request):
    """Export satellite data."""
    return Response({'message': 'Export satellites'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_schedule(request):
    """Export schedule to XLSX/CSV."""
    export_format = request.query_params.get('format', 'xlsx')
    
    if export_format == 'xlsx':
        return Response({'message': 'Export schedule to XLSX'})
    elif export_format == 'csv':
        return Response({'message': 'Export schedule to CSV'})
    else:
        return Response(
            {'error': 'Неподдерживаемый формат'},
            status=status.HTTP_400_BAD_REQUEST
        )
