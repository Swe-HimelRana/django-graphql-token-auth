from django.contrib.auth import authenticate
from django.contrib.auth.middleware import get_user
from django.contrib.auth.models import AnonymousUser
from .path import PathDict
from token_auth import utils
from .utils import get_http_authorization, get_token_argument
from token_auth.models import TokenAuth

try:
    from graphql.execution.execute import GraphQLResolveInfo
except ImportError:
    from graphql.execution.base import ResolveInfo as GraphQLResolveInfo  # noqa


def get_operation_name(operation):
    if hasattr(operation, "value"):
        return operation.value
    return operation


__all__ = [
    "allow_any",
    "TokenAuthMiddleWare",
]


def allow_any(info, **kwargs):
    operation_name = get_operation_name(info.operation.operation).title()
    field = info.schema.get_type(operation_name).fields.get(info.field_name)

    if field is None:
        return False

    graphene_type = getattr(field.type, "graphene_type", None)

    return graphene_type is not None and issubclass(
        graphene_type, tuple(())
    )


def _authenticate(request):
    is_anonymous = not hasattr(request, "user") or request.user.is_anonymous
    return is_anonymous and get_http_authorization(request) is not None


class TokenAuthMiddleWare:
    def __init__(self):
        self.cached_allow_any = set()

        if utils.TOKEN_ALLOW_ARGUMENT:
            self.cached_authentication = PathDict()

    def authenticate_context(self, info, **kwargs):
        root_path = info.path[0]

        if root_path not in self.cached_allow_any:
            if allow_any(info, **kwargs):
                self.cached_allow_any.add(root_path)
            else:
                return True
        return False

    def resolve(self, next, root, info, **kwargs):
        context = info.context
        token_header = info.context.META.get("HTTP_AUTHORIZATION")
        token = token_header.split(" ")[1]
        print("request header from Middleware: ", token)

        print("Context from Middleware: ", context)
        token_argument = get_token_argument(context, **kwargs)
        print("Token Arguments From Middleware: ", token_argument)

        if info.context.user is None:

            user = authenticate(info.context, token=token)
            self.cached_authentication.insert(info.path, user)
            print("User from Miiddleware New: ", user)

        elif hasattr(context, "user"):
            if hasattr(context, "session"):
                context.user = get_user(context)
                self.cached_authentication.insert(info.path, context.user)
            else:
                context.user = AnonymousUser()

        if (
                _authenticate(context) or token_argument is not None
        ) and self.authenticate_context(info, **kwargs):

            user = authenticate(request=context, **kwargs)

            if user is not None:
                context.user = user

                if utils.TOKEN_ALLOW_ARGUMENT:
                    self.cached_authentication.insert(info.path, user)

        return next(root, info, **kwargs)
