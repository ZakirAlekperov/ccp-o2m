"""
Ground Stations models for CCP O2M.
ЗСУ - Земная станция управления
ЗС ПД - Земная станция приёма данных
"""
from django.contrib.gis.db import models as gis_models
from django.db import models


class StationType(models.TextChoices):
    """Ground station type choices."""
    CONTROL = 'control', 'ЗСУ (Земная станция управления)'
    DATA_RECEPTION = 'data_reception', 'ЗС ПД (Земная станция приёма данных)'


class StationStatus(models.TextChoices):
    """Ground station status choices."""
    ACTIVE = 'active', 'Активна'
    INACTIVE = 'inactive', 'Неактивна'
    MAINTENANCE = 'maintenance', 'Обслуживание'


class GroundStation(models.Model):
    """
    Ground Station (Наземная станция) model.
    Can be either ЗСУ (control) or ЗС ПД (data reception).
    """
    name = models.CharField(max_length=100, verbose_name='Название')
    code = models.CharField(max_length=20, unique=True, verbose_name='Код')
    station_type = models.CharField(
        max_length=20,
        choices=StationType.choices,
        verbose_name='Тип станции'
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    
    # Geographic location
    location = gis_models.PointField(
        geography=True,
        verbose_name='Координаты'
    )
    elevation_m = models.FloatField(default=0.0, verbose_name='Высота над уровнем моря, м')
    
    # Communication parameters
    min_elevation_angle = models.FloatField(
        default=5.0,
        verbose_name='Мин. угол возвышения, °'
    )
    max_elevation_angle = models.FloatField(
        default=90.0,
        verbose_name='Макс. угол возвышения, °'
    )
    data_rate_mbps = models.FloatField(
        default=100.0,
        verbose_name='Скорость передачи, Мбит/с'
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=StationStatus.choices,
        default=StationStatus.ACTIVE,
        verbose_name='Статус'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлена')
    
    class Meta:
        verbose_name = 'Наземная станция'
        verbose_name_plural = 'Наземные станции'
        ordering = ['name']
        indexes = [
            gis_models.Index(fields=['location']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_station_type_display()})"
    
    @property
    def latitude(self):
        """Get latitude from location point."""
        return self.location.y if self.location else None
    
    @property
    def longitude(self):
        """Get longitude from location point."""
        return self.location.x if self.location else None


class CommunicationSlot(models.Model):
    """
    Communication time slots for ground stations.
    Временные слоты для сеансов связи.
    """
    station = models.ForeignKey(
        GroundStation,
        on_delete=models.CASCADE,
        related_name='communication_slots',
        verbose_name='Станция'
    )
    start_time = models.DateTimeField(verbose_name='Начало слота')
    end_time = models.DateTimeField(verbose_name='Конец слота')
    is_available = models.BooleanField(default=True, verbose_name='Доступен')
    reserved_for = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Зарезервирован для'
    )
    
    class Meta:
        verbose_name = 'Слот связи'
        verbose_name_plural = 'Слоты связи'
        ordering = ['start_time']
        indexes = [
            models.Index(fields=['station', 'start_time', 'end_time']),
            models.Index(fields=['is_available']),
        ]
    
    def __str__(self):
        return f"Слот {self.station.name} ({self.start_time} - {self.end_time})"


class ForbiddenZone(models.Model):
    """
    Forbidden zones (зоны запрета) for ground stations.
    Areas where communication is prohibited.
    """
    station = models.ForeignKey(
        GroundStation,
        on_delete=models.CASCADE,
        related_name='forbidden_zones',
        verbose_name='Станция'
    )
    name = models.CharField(max_length=100, verbose_name='Название зоны')
    # Polygon representing forbidden area
    area = gis_models.PolygonField(
        geography=True,
        verbose_name='Область запрета'
    )
    start_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Начало действия'
    )
    end_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Конец действия'
    )
    reason = models.TextField(blank=True, verbose_name='Причина')
    
    class Meta:
        verbose_name = 'Зона запрета'
        verbose_name_plural = 'Зоны запрета'
        indexes = [
            gis_models.Index(fields=['area']),
        ]
    
    def __str__(self):
        return f"Запрет {self.station.name} - {self.name}"
