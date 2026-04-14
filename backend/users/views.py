"""
Users views for CCP O2M.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth import authenticate
from .models import User
from .serializers import (
    UserSerializer, UserCreateSerializer, UserUpdateSerializer,
    LoginSerializer, UserProfileSerializer,
    UpdateProfileSerializer, ChangePasswordSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer

    def get_queryset(self):
        user = self.request.user
        if user.can_manage_users:
            return User.objects.all()
        return User.objects.filter(id=user.id)

    # ------------------------------------------------------------------ #
    #  AUTH
    # ------------------------------------------------------------------ #

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )

        if user is None:
            return Response({'error': 'Неверное имя пользователя или пароль'}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.is_active:
            return Response({'error': 'Пользователь неактивен'}, status=status.HTTP_403_FORBIDDEN)

        token = user.generate_token()
        return Response({
            'access_token': token,
            'token_type': 'Bearer',
            'user': UserProfileSerializer(user, context={'request': request}).data
        })

    @action(detail=False, methods=['post'])
    def logout(self, request):
        request.user.revoke_token()
        return Response({'message': 'Успешный выход'})

    # ------------------------------------------------------------------ #
    #  PROFILE
    # ------------------------------------------------------------------ #

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user profile."""
        serializer = UserProfileSerializer(request.user, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['patch'], url_path='me/update')
    def update_profile(self, request):
        """Update own name / email / username."""
        serializer = UpdateProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserProfileSerializer(request.user, context={'request': request}).data)

    @action(detail=False, methods=['patch'], url_path='me/avatar',
            parser_classes=[MultiPartParser, FormParser])
    def update_avatar(self, request):
        """Upload / replace avatar image."""
        if 'avatar' not in request.FILES:
            return Response({'error': 'Передайте файл в поле avatar'}, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        user.avatar = request.FILES['avatar']
        user.save(update_fields=['avatar'])
        return Response(UserProfileSerializer(user, context={'request': request}).data)

    @action(detail=False, methods=['post'], url_path='me/change-password')
    def change_password(self, request):
        """Change own password."""
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        # Re-generate token so old sessions are invalidated
        request.user.save()
        new_token = request.user.generate_token()
        return Response({'message': 'Пароль успешно изменён', 'access_token': new_token})
