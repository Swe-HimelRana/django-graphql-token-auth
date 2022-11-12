import graphene
import account.graphql.queries
import account.graphql.mutations
import account.graphql.types


class Query(account.graphql.queries.Query, graphene.ObjectType):
    pass

class Mutation(account.graphql.mutations.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)