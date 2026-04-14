"""
Flight Tasks (Полётные задания - ПЗ) models for CCP O2M.
"""
from django.contrib.gis.db import models as gis_models
from django.db import models
from django.conf import settings


class FlightTaskStatus(models.TextChoices):
    """Flight task status according to ТЗ."""
    NEW = 'new', 'Новое'
    APPROVAL = 'approval', 'Согласование'
    SENT = 'sent', 'Отправлено'
    APPROVED = 'approved', 'Одобрено'
    REJECTED = 'rejected', 'Отклонено'
    EXECUTING = 'executing', 'Выполняется'
    COMPLETED = 'completed', 'Выполнено'
    CANCELLED = 'cancelled', 'Отменено'


class FlightTaskGroup(models.Model):
    """
    Flight Task Group (Группа ПЗ) - collection of related flight tasks.
    """
    group_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Номер группы'
    )
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    
    # Planning period
    start_time = models.DateTimeField(verbose_name='Начало периода')
    end_time = models.DateTimeField(verbose_name='Конец периода')
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=FlightTaskStatus.choices,
        default=FlightTaskStatus.NEW,
        verbose_name='Статус'
    )
    
    # External IDs
    kup_task_id = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='ID в КУП'
    )
    
    # Metadata
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Создан пользователем'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлена')
    sent_to_kup_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Отправлено в КУП'
    )
    
    class Meta:
        verbose_name = 'Группа ПЗ'
        verbose_name_plural = 'Группы ПЗ'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.group_number} - {self.name}"
    
    @property
    def total_tasks(self):
        return self.flight_tasks.count()
    
    @property
    def imaging_tasks_count(self):
        return self.flight_tasks.filter(task_type='imaging').count()
    
    @property
    def dump_tasks_count(self):
        return self.flight_tasks.filter(task_type='dump').count()


class FlightTask(models.Model):
    """
    Flight Task (Полётное задание) - individual task for satellite.
    """
    TASK_TYPE_CHOICES = [
        ('imaging', 'Съёмка'),
        ('dump', 'Сброс'),
        ('maneuver', 'Манёвр'),
    ]
    
    task_number = models.CharField(
        max_length=50,
        verbose_name='Номер ПЗ'
    )
    group = models.ForeignKey(
        FlightTaskGroup,
        on_delete=models.CASCADE,
        related_name='flight_tasks',
        verbose_name='Группа'
    )
    task_type = models.CharField(
        max_length=20,
        choices=TASK_TYPE_CHOICES,
        default='imaging',
        verbose_name='Тип задания'
    )
    
    # Satellite
    satellite = models.ForeignKey(
        'satellites.Satellite',
        on_delete=models.CASCADE,
        related_name='flight_tasks',
        verbose_name='КА'
    )
    
    # Time
    start_time = models.DateTimeField(verbose_name='Начало')
    end_time = models.DateTimeField(verbose_name='Конец')
    duration_seconds = models.FloatField(verbose_name='Длительность, сек')
    
    # For imaging tasks
    imaging_request = models.ForeignKey(
        'imaging_requests.ImagingRequest',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='flight_tasks',
        verbose_name='Заявка на съёмку'
    )
    opportunity = models.ForeignKey(
        'planning.ImagingOpportunity',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='flight_task',
        verbose_name='Возможность съёмки'
    )
    
    # Imaging parameters
    roll_angle = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Угол крена, °'
    )
    pitch_angle = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Угол тангажа, °'
    )
    swath_geometry = gis_models.PolygonField(
        geography=True,
        null=True,
        blank=True,
        verbose_name='Геометрия полосы'
    )
    
    # For dump tasks
    ground_station = models.ForeignKey(
        'ground_stations.GroundStation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='dump_tasks',
        verbose_name='Наземная станция'
    )
    data_volume_gb = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Объём данных, ГБ'
    )
    memory_masks_released = models.ManyToManyField(
        'satellites.MemoryMask',
        blank=True,
        verbose_name='Освобождаемые маски'
    )
    
    # Execution status
    status = models.CharField(
        max_length=20,
        choices=FlightTaskStatus.choices,
        default=FlightTaskStatus.NEW,
        verbose_name='Статус'
    )
    
    # Feedback from КУП
    kup_status = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Статус в КУП'
    )
    execution_result = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Результат выполнения'
    )
    execution_quality = models.CharField(
        max_length=50,
        choices=[
            ('', 'Не указано'),
            ('success', 'Успешно'),
            ('partial', 'Частично'),
            ('failed', 'Неудача'),
            ('requires_reshoot', 'Требуется пересъёмка'),
            ('requires_redump', 'Требуется пересброс'),
        ],
        default='',
        blank=True,
        verbose_name='Качество выполнения'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    executed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Выполнено'
    )
    
    class Meta:
        verbose_name = 'Полётное задание'
        verbose_name_plural = 'Полётные задания'
        ordering = ['start_time']
        unique_together = ['group', 'task_number']
        indexes = [
            models.Index(fields=['satellite', 'start_time']),
            models.Index(fields=['status']),
            models.Index(fields=['task_type']),
        ]
    
    def __str__(self):
        return f"ПЗ {self.task_number} ({self.get_task_type_display()})"


class FlightTaskHistory(models.Model):
    """
    History of flight task status changes.
    """
    flight_task = models.ForeignKey(
        FlightTask,
        on_delete=models.CASCADE,
        related_name='history',
        verbose_name='ПЗ'
    )
    from_status = models.CharField(
        max_length=20,
        choices=FlightTaskStatus.choices,
        blank=True,
        verbose_name='Из статуса'
    )
    to_status = models.CharField(
        max_length=20,
        choices=FlightTaskStatus.choices,
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
        verbose_name = 'История ПЗ'
        verbose_name_plural = 'История ПЗ'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.flight_task.task_number}: {self.from_status} -> {self.to_status}"
