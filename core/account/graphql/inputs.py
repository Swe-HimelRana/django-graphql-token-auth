import graphene


class UserRegisterInput(graphene.InputObjectType):
    email = graphene.String(required=True)
    phone = graphene.String(required=True)
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    password = graphene.String(required=True)

class UserListInput(graphene.InputObjectType):
    email = graphene.String()
    phone = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    password = graphene.String()