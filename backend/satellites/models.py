"""
Satellites models for CCP O2M.
"""
from django.contrib.gis.db import models as gis_models
from django.db import models


class SatelliteStatus(models.TextChoices):
    """Satellite status choices."""
    ACTIVE = 'active', 'Активен'
    INACTIVE = 'inactive', 'Неактивен'
    MAINTENANCE = 'maintenance', 'Обслуживание'
    DECOMMISSIONED = 'decommissioned', 'Выведен из эксплуатации'


class Satellite(models.Model):
    """
    Satellite (КА) model according to ТЗ.
    """
    name = models.CharField(max_length=100, verbose_name='Название')
    norad_id = models.CharField(max_length=10, unique=True, verbose_name='NORAD ID')
    description = models.TextField(blank=True, verbose_name='Описание')
    
    # Imaging parameters
    swath_width_km = models.FloatField(default=10.0, verbose_name='Полоса захвата, км')
    max_roll_angle = models.FloatField(default=30.0, verbose_name='Макс. угол крена, °')
    max_pitch_angle = models.FloatField(default=30.0, verbose_name='Макс. угол тангажа, °')
    max_yaw_angle = models.FloatField(default=30.0, verbose_name='Макс. угол рыскания, °')
    
    # Memory constraints
    max_memory_gb = models.FloatField(default=100.0, verbose_name='Макс. память, ГБ')
    current_memory_usage_gb = models.FloatField(default=0.0, verbose_name='Текущая загрузка памяти, ГБ')
    
    # Power constraints
    power_consumption_per_image = models.FloatField(default=50.0, verbose_name='Расход энергии на снимок')
    available_power = models.FloatField(default=500.0, verbose_name='Доступная энергия')
    
    # Altitude constraints
    min_altitude_km = models.FloatField(default=400.0, verbose_name='Мин. высота, км')
    max_altitude_km = models.FloatField(default=1200.0, verbose_name='Макс. высота, км')
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=SatelliteStatus.choices,
        default=SatelliteStatus.ACTIVE,
        verbose_name='Статус'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлён')
    
    class Meta:
        verbose_name = 'Космический аппарат'
        verbose_name_plural = 'Космические аппараты'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.norad_id})"
    
    @property
    def memory_usage_percent(self):
        """Calculate memory usage percentage."""
        if self.max_memory_gb > 0:
            return (self.current_memory_usage_gb / self.max_memory_gb) * 100
        return 0


class TLEData(models.Model):
    """
    TLE (Two-Line Element) data for satellite orbit calculation.
    """
    satellite = models.ForeignKey(
        Satellite,
        on_delete=models.CASCADE,
        related_name='tle_history',
        verbose_name='КА'
    )
    tle_line1 = models.CharField(max_length=69, verbose_name='TLE строка 1')
    tle_line2 = models.CharField(max_length=69, verbose_name='TLE строка 2')
    epoch = models.DateTimeField(verbose_name='Эпоха')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Загружено')
    is_current = models.BooleanField(default=True, verbose_name='Актуальное')
    
    class Meta:
        verbose_name = 'TLE данные'
        verbose_name_plural = 'TLE данные'
        ordering = ['-epoch']
        indexes = [
            models.Index(fields=['satellite', '-epoch']),
            models.Index(fields=['is_current']),
        ]
    
    def __str__(self):
        return f"TLE {self.satellite.name} ({self.epoch})"


class MemoryMask(models.Model):
    """
    Memory mask (маска памяти) for satellite data storage.
    Represents occupied memory slots for imaging data.
    """
    satellite = models.ForeignKey(
        Satellite,
        on_delete=models.CASCADE,
        related_name='memory_masks',
        verbose_name='КА'
    )
    start_time = models.DateTimeField(verbose_name='Начало')
    end_time = models.DateTimeField(verbose_name='Конец')
    size_gb = models.FloatField(verbose_name='Размер, ГБ')
    description = models.CharField(max_length=255, blank=True, verbose_name='Описание')
    is_releasable = models.BooleanField(default=True, verbose_name='Можно освободить')
    
    # Optional link to flight task
    flight_task_id = models.IntegerField(null=True, blank=True, verbose_name='ID ПЗ')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    
    class Meta:
        verbose_name = 'Маска памяти'
        verbose_name_plural = 'Маски памяти'
        ordering = ['-start_time']
        indexes = [
            models.Index(fields=['satellite', 'start_time', 'end_time']),
        ]
    
    def __str__(self):
        return f"Маска {self.satellite.name} ({self.start_time} - {self.end_time})"


class UnavailabilityPeriod(models.Model):
    """
    Periods when satellite is unavailable for operations.
    """
    satellite = models.ForeignKey(
        Satellite,
        on_delete=models.CASCADE,
        related_name='unavailability_periods',
        verbose_name='КА'
    )
    start_time = models.DateTimeField(verbose_name='Начало')
    end_time = models.DateTimeField(verbose_name='Конец')
    reason = models.TextField(verbose_name='Причина')
    
    class Meta:
        verbose_name = 'Период недоступности'
        verbose_name_plural = 'Периоды недоступности'
        ordering = ['-start_time']
    
    def __str__(self):
        return f"Недоступность {self.satellite.name} ({self.start_time} - {self.end_time})"
