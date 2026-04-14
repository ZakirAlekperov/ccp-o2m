"""
Planning models for CCP O2M.
Прогнозирование и планирование съёмок.
"""
from django.contrib.gis.db import models as gis_models
from django.db import models
from django.conf import settings


class ForecastStatus(models.TextChoices):
    """Forecast calculation status."""
    PENDING = 'pending', 'В очереди'
    RUNNING = 'running', 'Выполняется'
    COMPLETED = 'completed', 'Завершено'
    FAILED = 'failed', 'Ошибка'
    CANCELLED = 'cancelled', 'Отменено'


class ForecastResult(models.Model):
    """
    Forecast calculation result (Результат прогнозирования).
    """
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    
    # Time parameters
    start_date = models.DateTimeField(verbose_name='Начало периода')
    end_date = models.DateTimeField(verbose_name='Конец периода')
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=ForecastStatus.choices,
        default=ForecastStatus.PENDING,
        verbose_name='Статус'
    )
    is_current = models.BooleanField(
        default=True,
        verbose_name='Актуальный прогноз'
    )
    
    # Calculation results
    total_requests = models.IntegerField(default=0, verbose_name='Всего заявок')
    processed_requests = models.IntegerField(default=0, verbose_name='Обработано заявок')
    total_opportunities = models.IntegerField(default=0, verbose_name='Всего окон съёмки')
    
    # Error info
    error_message = models.TextField(blank=True, verbose_name='Сообщение об ошибке')
    
    # Metadata
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Создан пользователем'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Завершён')
    
    class Meta:
        verbose_name = 'Результат прогнозирования'
        verbose_name_plural = 'Результаты прогнозирования'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Прогноз {self.name} ({self.start_date.date()} - {self.end_date.date()})"


class ForecastRequestMapping(models.Model):
    """
    Mapping between forecast and imaging requests with coverage info.
    """
    forecast = models.ForeignKey(
        ForecastResult,
        on_delete=models.CASCADE,
        related_name='request_mappings',
        verbose_name='Прогноз'
    )
    request = models.ForeignKey(
        'imaging_requests.ImagingRequest',
        on_delete=models.CASCADE,
        related_name='forecast_mappings',
        verbose_name='Заявка'
    )
    coverage_percent = models.FloatField(
        default=0.0,
        verbose_name='Процент покрытия'
    )
    opportunity_count = models.IntegerField(
        default=0,
        verbose_name='Количество окон'
    )
    
    class Meta:
        verbose_name = 'Связь прогноз-заявка'
        verbose_name_plural = 'Связи прогноз-заявки'
        unique_together = ['forecast', 'request']


class ImagingOpportunity(models.Model):
    """
    Imaging opportunity (возможность съёмки) - calculated window.
    """
    forecast = models.ForeignKey(
        ForecastResult,
        on_delete=models.CASCADE,
        related_name='opportunities',
        verbose_name='Прогноз',
        null=True,
        blank=True
    )
    request = models.ForeignKey(
        'imaging_requests.ImagingRequest',
        on_delete=models.CASCADE,
        related_name='opportunities',
        verbose_name='Заявка'
    )
    satellite = models.ForeignKey(
        'satellites.Satellite',
        on_delete=models.CASCADE,
        related_name='imaging_opportunities',
        verbose_name='КА'
    )
    
    # Time window
    start_time = models.DateTimeField(verbose_name='Начало съёмки')
    end_time = models.DateTimeField(verbose_name='Конец съёмки')
    duration_seconds = models.FloatField(verbose_name='Длительность, сек')
    
    # Geometry
    swath_geometry = gis_models.PolygonField(
        geography=True,
        null=True,
        blank=True,
        verbose_name='Геометрия полосы'
    )
    
    # Parameters
    roll_angle = models.FloatField(verbose_name='Угол крена, °')
    sun_elevation = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Угол возвышения солнца, °'
    )
    sun_azimuth = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Азимут солнца, °'
    )
    
    # Scoring
    score = models.FloatField(
        default=0.0,
        verbose_name='Оценка возможности'
    )
    
    # Selection status
    is_selected = models.BooleanField(
        default=False,
        verbose_name='Выбрана для планирования'
    )
    
    class Meta:
        verbose_name = 'Возможность съёмки'
        verbose_name_plural = 'Возможности съёмки'
        ordering = ['start_time']
        indexes = [
            models.Index(fields=['satellite', 'start_time']),
            models.Index(fields=['request', 'start_time']),
            models.Index(fields=['is_selected']),
        ]
    
    def __str__(self):
        return f"Съёмка {self.satellite.name} ({self.start_time})"


class WeatherForecast(models.Model):
    """
    Weather forecast data for cloud coverage prediction.
    """
    forecast_time = models.DateTimeField(verbose_name='Время прогноза')
    area = gis_models.PolygonField(
        geography=True,
        verbose_name='Область'
    )
    cloud_coverage_percent = models.FloatField(
        verbose_name='Облачность, %'
    )
    source = models.CharField(
        max_length=100,
        default='GRIB2',
        verbose_name='Источник'
    )
    raw_data = models.JSONField(
        default=dict,
        verbose_name='Сырые данные'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Загружен')
    
    class Meta:
        verbose_name = 'Прогноз погоды'
        verbose_name_plural = 'Прогнозы погоды'
        ordering = ['-forecast_time']
        indexes = [
            gis_models.Index(fields=['area']),
            models.Index(fields=['forecast_time']),
        ]
    
    def __str__(self):
        return f"Погода {self.forecast_time} ({self.cloud_coverage_percent}%)"
