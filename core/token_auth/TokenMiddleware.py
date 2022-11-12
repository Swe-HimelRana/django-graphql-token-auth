from token_auth.models import TokenAuth
from django.contrib.auth import authenticate
from django.utils.functional import SimpleLazyObject


class CustomMiddleware(object):
    def __init__(self, get_response):
        """
        One-time configuration and initialisation.
        """
        self.get_response = get_response

    def __call__(self, request):
        print("Middleware called")
        user = SimpleLazyObject(lambda: self.get_token_user(request))

        if user:
            print("user is not None", user)
            request.user = user

        return self.get_response(request)

    def get_token_user(self, request):
        """Return user from token."""
        if request.META.get("HTTP_AUTHORIZATION"):
            try:
                token_header = request.META.get("HTTP_AUTHORIZATION")
                token = token_header.split(" ")[1]
                user = None
                if TokenAuth.objects.filter(token=token).exists():
                    user = authenticate(request, token=token)
                if user is not None:
                    return user
                else:
                    return None
            except Exception as e:
                print(str(e))
                return None

    def process_template_response(self, request, response):
        """
        Called just after the view has finished executing.
        """
        return response
