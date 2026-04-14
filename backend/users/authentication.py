from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class TokenAuthentication(BaseAuthentication):
    """
    Simple token-based authentication.
    Reads Authorization: Bearer <token>, looks up User by auth_token field.
    get_user_model() is called lazily inside the method to avoid AppRegistryNotReady.
    """

    def authenticate(self, request):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ', 1)[1].strip()
        if not token:
            return None

        try:
            user = User.objects.get(auth_token=token, is_active=True)
        except User.DoesNotExist:
            raise AuthenticationFailed('Неверный или просроченный токен')

        return (user, token)


# Alias for backwards compatibility with settings.py
KeycloakAuthentication = TokenAuthentication
