import graphene
from graphene_django import DjangoObjectType
from graphene_django.debug import DjangoDebug
from graphql_util.cursor import CursorPaginatedConnectionField
from django.db.models import Prefetch
from .models import Author, Category, Entry


class EntryNode(DjangoObjectType):
    class Meta:
        model = Entry
        interfaces = (graphene.relay.Node, )
        filter_fields = ['title']

    def prefetch_author(queryset, related_queryset):
        return queryset.select_related('author')

    def prefetch_category(queryset, related_queryset):
        return queryset.select_related('category')


class EntryConnection(graphene.relay.Connection):
    class Meta:
        node = EntryNode


class AuthorNode(DjangoObjectType):
    entries = CursorPaginatedConnectionField(EntryNode)

    class Meta:
        model = Author
        interfaces = (graphene.relay.Node, )
        filter_fields = ['first_name', 'last_name']

    def prefetch_entries(queryset, related_queryset):
        assert(false, "prefetch_### is never called for related/ManyToOne fields")
        return queryset.prefetch_related(Prefetch('entries', queryset=related_queryset))

    def optimize_entries(queryset, **kwargs):
        # Would be nice if prefetch_entries was called instead.
        # Alternatively we could improve the logic to auto-generate the Prefetch queryset argument
        # based on the subfields (if we passed the node_type and subfields to this method)
        return queryset.prefetch_related(Prefetch('entries', queryset=Entry.objects.select_related('category')))


class AuthorConnection(graphene.relay.Connection):
    class Meta:
        node = AuthorNode


class CategoryNode(DjangoObjectType):
    entries = CursorPaginatedConnectionField(EntryNode)

    class Meta:
        model = Category
        interfaces = (graphene.relay.Node, )
        filter_fields = ['name']


class CategoryConnection(graphene.relay.Connection):
    class Meta:
        node = CategoryNode


class BlogQuery(graphene.ObjectType):
    entries = CursorPaginatedConnectionField(EntryNode)
    authors = CursorPaginatedConnectionField(AuthorNode)
    categories = CursorPaginatedConnectionField(CategoryNode)

    debug = graphene.Field(DjangoDebug, name='__debug')

    def resolve_entries(self, info, **kwargs):
        return Entry.objects.all()

    def resolve_authors(self, info, **kwargs):
        return Author.objects.all()

    def resolve_categories(self, info, **kwargs):
        return Category.objects.all()


schema = graphene.Schema(query=BlogQuery)
