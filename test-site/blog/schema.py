import graphene
from graphene_django import DjangoObjectType
from graphene_django.debug import DjangoDebug
from graphene_django.filter import DjangoFilterConnectionField
from graphql_util.cursor import CursorPaginatedConnectionField
from .models import Author, Category, Entry


class AuthorNode(DjangoObjectType):

    class Meta:
        model = Author
        interfaces = (graphene.relay.Node, )
        filter_fields = ['first_name', 'last_name']


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        interfaces = (graphene.relay.Node, )
        filter_fields = ['name']


class EntryNode(DjangoObjectType):
    class Meta:
        model = Entry
        interfaces = (graphene.relay.Node, )
        filter_fields = ['title']


class BlogQuery(graphene.ObjectType):
    """ GraphQL query for competitions """
    authors = DjangoFilterConnectionField(AuthorNode)
    categories = DjangoFilterConnectionField(CategoryNode)
    entries = DjangoFilterConnectionField(EntryNode)

    entries_cursor = CursorPaginatedConnectionField(EntryNode)

    debug = graphene.Field(DjangoDebug, name='__debug')


schema = graphene.Schema(query=BlogQuery)
