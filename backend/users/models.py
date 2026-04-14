"""
Users models for CCP O2M.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    """User roles according to ТЗ."""
    ADMIN = 'admin', 'Администратор'
    SUPERUSER = 'superuser', 'Суперпользователь'
    PLANNER = 'planner', 'Планировщик'
    EXTERNAL_OPERATOR = 'external_operator', 'Внешний оператор'


class User(AbstractUser):
    """
    Custom User model with Keycloak integration support.
    """
    email = models.EmailField(unique=True, verbose_name='Email')
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.EXTERNAL_OPERATOR,
        verbose_name='Роль'
    )
    keycloak_id = models.CharField(
        max_length=36,
        blank=True,
        null=True,
        unique=True,
        verbose_name='Keycloak ID'
    )
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлён')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def has_role(self, roles):
        """Check if user has any of the specified roles."""
        if isinstance(roles, str):
            roles = [roles]
        return self.role in roles

    @property
    def can_manage_users(self):
        """Only admin can manage users."""
        return self.role == UserRole.ADMIN

    @property
    def can_manage_satellites(self):
        """Admin and superuser can manage satellites."""
        return self.role in [UserRole.ADMIN, UserRole.SUPERUSER]

    @property
    def can_create_requests(self):
        """Admin, superuser and planner can create imaging requests."""
        return self.role in [UserRole.ADMIN, UserRole.SUPERUSER, UserRole.PLANNER]

    @property
    def can_plan(self):
        """Admin, superuser and planner can plan."""
        return self.role in [UserRole.ADMIN, UserRole.SUPERUSER, UserRole.PLANNER]

    @property
    def can_export_data(self):
        """All authenticated users except guests can export."""
        return self.role in [
            UserRole.ADMIN,
            UserRole.SUPERUSER,
            UserRole.PLANNER,
            UserRole.EXTERNAL_OPERATOR
        ]

    @property
    def can_view_data(self):
        """All authenticated users can view data."""
        return True
