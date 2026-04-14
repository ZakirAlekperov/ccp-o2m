"""
Users serializers for CCP O2M.
"""
from rest_framework import serializers
from .models import User, UserRole


class UserSerializer(serializers.ModelSerializer):
    """User serializer for read operations."""
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'role_display', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    """User serializer for create operations."""
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password',
            'first_name', 'last_name', 'role', 'is_active'
        ]
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """User serializer for update operations."""
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email',
            'first_name', 'last_name', 'role', 'is_active'
        ]


class LoginSerializer(serializers.Serializer):
    """Login request serializer."""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class TokenSerializer(serializers.Serializer):
    """Token response serializer."""
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    expires_in = serializers.IntegerField()
    token_type = serializers.CharField(default='Bearer')


class UserProfileSerializer(serializers.ModelSerializer):
    """Current user profile serializer."""
    permissions = serializers.SerializerMethodField()
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'role_display', 'is_active', 'permissions', 'created_at'
        ]
    
    def get_permissions(self, obj):
        return {
            'can_manage_users': obj.can_manage_users,
            'can_manage_satellites': obj.can_manage_satellites,
            'can_create_requests': obj.can_create_requests,
            'can_plan': obj.can_plan,
            'can_export_data': obj.can_export_data,
            'can_view_data': obj.can_view_data,
        }
