
class AuthTokenExceptions(Exception):
    default_message = None

    def __init__(self, message=None):
        if message is None:
            message = self.default_message

        super().__init__(message)


class PermissionDenied(AuthTokenExceptions):
    default_message = "You are not authenticated"


class SuspendedUser(AuthTokenExceptions):
    default_message = "Your account has been suspended"


class AuthTokenError(AuthTokenExceptions):
    default_message = "Invalid Token"
