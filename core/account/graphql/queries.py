import graphene
from django.contrib.auth import get_user_model
from .types import UserType
from django.contrib.auth import authenticate, login, get_user_model
from token_auth.decorators import login_required, not_suspended_required

User = get_user_model()


class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    current_user = graphene.List(UserType)

    def resolve_all_users(self, info):
        return User.objects.all()

    @login_required
    def resolve_current_user(self, info):
        return User.objects.filter(pk=info.context.user.id)
