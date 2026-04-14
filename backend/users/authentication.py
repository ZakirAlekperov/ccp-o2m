# users/authentication.py
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

User = get_user_model()


class TokenAuthentication(BaseAuthentication):
    """
    Simple token-based authentication.
    Token is stored in User.auth_token field (UUID string).
    Client sends: Authorization: Bearer <token>
    """

    def authenticate(self, request):
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


# Keep old name as alias so settings.py import doesn't break
KeycloakAuthentication = TokenAuthentication
