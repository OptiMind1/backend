from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import close_old_connections
from rest_framework_simplejwt.exceptions import InvalidToken

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token", [None])[0]

        if token is None:
            scope["user"] = AnonymousUser()
            return await super().__call__(scope, receive, send)

        try:
            # JWT 인증 처리
            jwt_auth = JWTAuthentication()
            validated_token = jwt_auth.get_validated_token(token)
            user = jwt_auth.get_user(validated_token)
            scope["user"] = user
        except InvalidToken:  # InvalidToken 예외 처리
            scope["user"] = AnonymousUser()
        except Exception:
            scope["user"] = AnonymousUser()

        close_old_connections()
        return await super().__call__(scope, receive, send)
