# users/authentication.py
from rest_framework.authentication import BaseAuthentication

class KeycloakAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Заглушка для Keycloak
        return None
