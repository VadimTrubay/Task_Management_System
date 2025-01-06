import os
from datetime import datetime

import jwt
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

from django.contrib.auth.models import User
from django.db import close_old_connections
import django
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


ALGORITHM = "HS256"


@database_sync_to_async
def get_user(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=ALGORITHM)

    except Exception:
        print("no payload")
        return AnonymousUser()

    token_exp = datetime.fromtimestamp(payload["exp"])
    if token_exp < datetime.utcnow():
        print("no date-time")
        return AnonymousUser()

    try:
        user = get_user_model().objects.get(id=payload["user_id"])
        print("user", user)
    except User.DoesNotExist:
        print("no user")
        return AnonymousUser()

    return user


class TokenAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):
        close_old_connections()
        try:
            token = dict(scope["headers"])[b"authorization"].decode("utf-8")
            if token.startswith("Bearer "):
                token = token[7:]

        except ValueError as e:
            print("Invalid token", e)

        scope["user"] = await get_user(token)
        return await super().__call__(scope, receive, send)


def JwtAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(inner)
