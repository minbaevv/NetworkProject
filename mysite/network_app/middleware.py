from channels.db import database_sync_to_async
from urllib.parse import parse_qs


@database_sync_to_async
def get_user(token_key):
    try:
        from django.contrib.auth import get_user_model
        from rest_framework_simplejwt.tokens import AccessToken

        User = get_user_model()
        token = AccessToken(token_key)
        user = User.objects.get(id=token['user_id'])
        return user
    except Exception:
        from django.contrib.auth.models import AnonymousUser
        return AnonymousUser()


class JWTAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        from django.contrib.auth.models import AnonymousUser

        query_string = scope.get('query_string', b'').decode()
        params = parse_qs(query_string)
        token = params.get('token', [None])[0]

        scope['user'] = await get_user(token) if token else AnonymousUser()

        return await self.app(scope, receive, send)