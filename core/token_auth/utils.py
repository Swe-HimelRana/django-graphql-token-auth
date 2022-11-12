from calendar import timegm
from datetime import datetime
import django
from django.contrib.auth import get_user_model
from . import exceptions
from token_auth.functions import get_or_create_token
from token_auth.models import TokenAuth
from .exceptions import AuthTokenError

TOKEN_PREFIX = "Token"
TOKEN_AUTH_HEADER_NAME = "HTTP_AUTHORIZATION"
TOKEN_ALLOW_ARGUMENT = False
TOKEN_ARGUMENT_NAME = "token"


def token_payload(user, context=None):
    payload = get_or_create_token(user.id)

    return payload


def get_http_authorization(request):
    auth = request.META.get(TOKEN_AUTH_HEADER_NAME, "").split()
    prefix = TOKEN_PREFIX

    if len(auth) != 2 or auth[0].lower() != prefix.lower():
        return request.COOKIES.get(TOKEN_PREFIX)
    return auth[1]


def get_token_argument(request, **kwargs):
    if TOKEN_ALLOW_ARGUMENT:
        input_fields = kwargs.get("input")

        if isinstance(input_fields, dict):
            kwargs = input_fields

        return kwargs.get(TOKEN_ARGUMENT_NAME)
    return None


def get_credentials(request, **kwargs):
    return get_token_argument(request, **kwargs) or get_http_authorization(request)


def get_payload(token, context=None):
    if TokenAuth.objects.filter(token=token).exists():
        user_object = TokenAuth.objects.filter(token=token).user
        payload = []
        payload['user_id'] = user_object.user_id
        payload['email'] = user_object.user_email
        payload['isEmailVerified'] = user_object.user_is_email_verified

        return payload
    else:
        return AuthTokenError("Invalid Token")


def get_user_by_natural_key(id):
    UserModel = get_user_model()
    try:
        return UserModel.objects.get(pk=id)
    except UserModel.DoesNotExist:
        return None


def get_user_by_payload(payload):
    UserModel = get_user_model()
    userid = payload['user_id']

    if not userid:
        raise exceptions.AuthTokenError("Invalid payload")

    user = UserModel.objects.filter(pk=userid).first()

    if user is not None and not getattr(user, "is_active", True):
        raise exceptions.AuthTokenError("User is disabled")
    return user


def set_cookie(response, key, value):
    kwargs = {
        "httponly": True,
        "secure": False,
        "path": '/',
        "domain": None,
    }

    response.set_cookie(key, value, **kwargs)


def delete_cookie(response, key):
    response.delete_cookie(
        key,
        path='/',
        domain=None
    )
