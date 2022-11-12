import graphene
from .inputs import UserRegisterInput
from .types import UserType
from django.contrib.auth import authenticate, login, get_user_model
from token_auth.functions import get_or_create_token
from token_auth.models import TokenAuth
import graphql_jwt

User = get_user_model()


class UserLoginMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
    token = graphene.String()
    user = graphene.Field(UserType)

    def mutate(self, info, email, password):
        res_user = authenticate(info.context, username=email, password=password)

        if res_user is not None:
            try:
                token = get_or_create_token(res_user.id, info.context)
                return UserLoginMutation(user=res_user, token=token)
            except Exception as e:
                print(str(e))
                return str(e)
        else:
            return Exception("Incorrect Credentials")


class UserCreateMutation(graphene.Mutation):
    class Arguments:
        user_data = UserRegisterInput(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, user_data):
        print("Mutate Called")
        print(user_data.email)
        try:
            User = get_user_model()
            new = User.objects.create_user(email="user2@gmail.com", phone="+8801315774222", first_name="Live",
                                           last_name="Test", password="@Pass123")
        except Exception as E:
            return Exception(str(E))

        return UserCreateMutation(user=new)


class Mutation:
    token_auth = UserLoginMutation.Field()
    jwt_token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    jwt_verify_token = graphql_jwt.Verify.Field()
    jwt_refresh_token = graphql_jwt.Refresh.Field()
    user_create = UserCreateMutation.Field()

