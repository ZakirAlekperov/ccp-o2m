"""
Users models for CCP O2M.
"""
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    ADMIN = 'admin', 'Администратор'
    OPERATOR = 'operator', 'Оператор'
    ANALYST = 'analyst', 'Аналитик'
    VIEWER = 'viewer', 'Наблюдатель'


class User(AbstractUser):
    """
    Custom User model with roles and token-based auth.
    """
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.VIEWER,
        verbose_name='Роль'
    )
    keycloak_id = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Keycloak ID'
    )
    auth_token = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Auth Token'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        verbose_name='Аватарка'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def can_manage_users(self):
        return self.role == UserRole.ADMIN or self.is_superuser

    @property
    def can_manage_satellites(self):
        return self.role in [UserRole.ADMIN, UserRole.OPERATOR] or self.is_superuser

    @property
    def can_create_requests(self):
        return self.role in [UserRole.ADMIN, UserRole.OPERATOR, UserRole.ANALYST] or self.is_superuser

    @property
    def can_plan(self):
        return self.role in [UserRole.ADMIN, UserRole.OPERATOR] or self.is_superuser

    @property
    def can_export_data(self):
        return self.role in [UserRole.ADMIN, UserRole.ANALYST] or self.is_superuser

    @property
    def can_view_data(self):
        return True

    def generate_token(self):
        self.auth_token = str(uuid.uuid4())
        self.save(update_fields=['auth_token'])
        return self.auth_token

    def revoke_token(self):
        self.auth_token = ''
        self.save(update_fields=['auth_token'])
