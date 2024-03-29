from functools import wraps
from token_auth.exceptions import PermissionDenied
from graphql.execution.execute import GraphQLResolveInfo


def context(f):
    def decorator(func):
        def wrapper(*args, **kwargs):
            info = next(arg for arg in args if isinstance(arg, GraphQLResolveInfo))
            return func(info.context, *args, **kwargs)

        return wrapper

    return decorator


def user_passes_test(test_func, exc=PermissionDenied):
    def decorator(f):
        @wraps(f)
        @context(f)
        def wrapper(context, *args, **kwargs):
            if test_func(context.user):
                return f(*args, **kwargs)
            raise exc

        return wrapper

    return decorator


not_suspended_required = user_passes_test(lambda u: not u.is_suspended)
login_required = user_passes_test(lambda u: u.is_authenticated)
staff_member_required = user_passes_test(lambda u: u.is_staff)
superuser_required = user_passes_test(lambda u: u.is_superuser)
email_verification_required = user_passes_test(lambda u: u.is_email_verified)
phone_verification_required = user_passes_test(lambda u: u.is_phone_verified)
identity_verification_required = user_passes_test(lambda u: u.is_identity_verified)
