import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.debug import DjangoDebug
from graphene_django_extras import PageGraphqlPagination, LimitOffsetGraphqlPagination, DjangoListObjectType
from graphene_django_extras import DjangoObjectField as DOF
from graphql_util.cursor import CursorPaginatedConnectionField
from django.db.models import Prefetch
from graphql_util.fields import OptimizedDjangoFilterPaginateListField as DjangoFilterPaginateListField
from .models import Author, Category, Entry, Tag


class TagNode(DjangoObjectType):
    class Meta:
        model = Tag
        filter_fields = ['name']


class EntryNode(DjangoObjectType):
    tags = DjangoFilterPaginateListField(
        TagNode, pagination=PageGraphqlPagination(page_size_query_param='page_size'))

    class Meta:
        model = Entry
        filter_fields = ['title']


class EntryFilter(django_filters.FilterSet):
    class Meta:
        model = Entry
        fields = {
            'author__first_name': ['exact'],
            'category__name': ['exact'],
            'title': ['exact', 'startswith'],
        }

    order_by = django_filters.OrderingFilter(
        fields=(
            ('title', 'title'),
            ('author__last_name', 'author'),
        )
    )


class CategoryNode(DjangoObjectType):
    entries = DjangoFilterPaginateListField(
        EntryNode, pagination=PageGraphqlPagination(page_size_query_param='page_size'), filterset_class=EntryFilter)

    class Meta:
        model = Category
        filter_fields = ['name']


class AuthorNode(DjangoObjectType):
    entries = DjangoFilterPaginateListField(
        EntryNode, pagination=PageGraphqlPagination(page_size_query_param='page_size'), filterset_class=EntryFilter)
    moderated_categories = DjangoFilterPaginateListField(
        CategoryNode, pagination=PageGraphqlPagination())

    class Meta:
        model = Author
        filter_fields = ['first_name', 'last_name']


class BlogQuery(graphene.ObjectType):
    entries = DjangoFilterPaginateListField(
        EntryNode, pagination=PageGraphqlPagination(page_size_query_param='page_size'), filterset_class=EntryFilter)
    authors = DjangoFilterPaginateListField(
        AuthorNode, pagination=PageGraphqlPagination(page_size_query_param='page_size'))
    categories = DjangoFilterPaginateListField(
        CategoryNode, pagination=PageGraphqlPagination(page_size_query_param='page_size'))

    debug = graphene.Field(DjangoDebug, name='__debug')


schema = graphene.Schema(query=BlogQuery)
