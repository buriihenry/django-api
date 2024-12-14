import jwt
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from authentication.models import User
from rest_framework import exceptions
from django.conf import settings

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = get_authorization_header(request).decode('utf-8')
        if not auth_header.startswith('Bearer '):
            raise exceptions.AuthenticationFailed('Invalid token header format. Expected "Bearer <token>"')

        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
            username = payload['username']
            user = User.objects.get(username=username)
            return (user, token)

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token is expired, login again')
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('Token is invalid')
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return None
