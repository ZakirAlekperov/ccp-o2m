"""
Imaging Requests models for CCP O2M.
Заявки на съёмку.
"""
from django.contrib.gis.db import models as gis_models
from django.db import models
from django.conf import settings


class RequestStatus(models.TextChoices):
    """Imaging request status choices according to ТЗ."""
    NEW = 'new', 'Новая'
    APPROVED = 'approved', 'Согласована'
    IN_PROGRESS = 'in_progress', 'Выполняется'
    COMPLETED = 'completed', 'Завершена'
    CANCELLED = 'cancelled', 'Отменена'


class ImagingType(models.TextChoices):
    """Imaging type choices."""
    STANDARD = 'standard', 'Стандартная'
    NIGHT = 'night', 'Ночная (угол солнца < 10°)'
    MULTI_POLYGON = 'multi_polygon', 'Мультиполигон'
    WITH_CUTOUTS = 'with_cutouts', 'С вырезами'


class ImagingRequest(models.Model):
    """
    Imaging Request (Заявка на съёмку) model.
    """
    # Identification
    request_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Номер заявки'
    )
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    
    # Target area (can be Point, Polygon, or MultiPolygon)
    target_area = gis_models.GeometryField(
        geography=True,
        verbose_name='Целевая область'
    )
    
    # Imaging parameters
    imaging_type = models.CharField(
        max_length=20,
        choices=ImagingType.choices,
        default=ImagingType.STANDARD,
        verbose_name='Тип съёмки'
    )
    required_resolution = models.FloatField(
        default=1.0,
        verbose_name='Требуемое разрешение, м'
    )
    priority = models.IntegerField(
        default=5,
        verbose_name='Приоритет (1-10)',
        help_text='1 - низкий, 10 - критический'
    )
    
    # Time window for imaging
    earliest_start = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Раннее начало'
    )
    latest_end = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Позднее окончание'
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=RequestStatus.choices,
        default=RequestStatus.NEW,
        verbose_name='Статус'
    )
    
    # External source (from КВП)
    external_id = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Внешний ID'
    )
    external_system = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Внешняя система'
    )
    
    # Metadata
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_requests',
        verbose_name='Создана пользователем'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлена')
    
    class Meta:
        verbose_name = 'Заявка на съёмку'
        verbose_name_plural = 'Заявки на съёмку'
        ordering = ['-created_at']
        indexes = [
            gis_models.Index(fields=['target_area']),
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['earliest_start', 'latest_end']),
        ]
    
    def __str__(self):
        return f"{self.request_number} - {self.name}"
    
    @property
    def area_km2(self):
        """Calculate area in square kilometers."""
        if self.target_area:
            # Transform to a projected CRS for accurate area calculation
            return self.target_area.transform(3857, clone=True).area / 1e6
        return 0


class ImagingRequestAttachment(models.Model):
    """
    Attachments for imaging requests (SHP, GeoJSON files).
    """
    request = models.ForeignKey(
        ImagingRequest,
        on_delete=models.CASCADE,
        related_name='attachments',
        verbose_name='Заявка'
    )
    file = models.FileField(upload_to='request_attachments/', verbose_name='Файл')
    file_type = models.CharField(
        max_length=20,
        choices=[
            ('shp', 'Shapefile'),
            ('geojson', 'GeoJSON'),
            ('kml', 'KML'),
            ('other', 'Другое'),
        ],
        verbose_name='Тип файла'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Загружен')
    
    class Meta:
        verbose_name = 'Вложение заявки'
        verbose_name_plural = 'Вложения заявок'
    
    def __str__(self):
        return f"{self.file.name} ({self.request.request_number})"


class RequestHistory(models.Model):
    """
    History log for imaging request status changes.
    """
    request = models.ForeignKey(
        ImagingRequest,
        on_delete=models.CASCADE,
        related_name='history',
        verbose_name='Заявка'
    )
    from_status = models.CharField(
        max_length=20,
        choices=RequestStatus.choices,
        blank=True,
        verbose_name='Из статуса'
    )
    to_status = models.CharField(
        max_length=20,
        choices=RequestStatus.choices,
        verbose_name='В статус'
    )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Изменено пользователем'
    )
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата изменения')
    
    class Meta:
        verbose_name = 'История заявки'
        verbose_name_plural = 'История заявок'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.request.request_number}: {self.from_status} -> {self.to_status}"
