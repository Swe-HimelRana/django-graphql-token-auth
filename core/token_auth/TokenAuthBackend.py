from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from .models import TokenAuth


class TokenAuthBackend(ModelBackend):
    """Log in to Django with token.
    """

    def authenticate(self, request, token):
        print("Token From Backend", token)
        User = get_user_model()
        if TokenAuth.objects.filter(token=token).exists():
            token_user_id = TokenAuth.objects.filter(token=token).first().user_id
            user = User.objects.get(pk=token_user_id)

            return user
        else:
            return AnonymousUser

    def get_user(self, request, user_id=None):

        User = get_user_model()

        try:
            user = User.objects.get(pk=user_id)

            return user
        except User.DoesNotExist:
            return AnonymousUser
