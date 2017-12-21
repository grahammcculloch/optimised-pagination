import operator
from functools import partial

from graphene_django.utils import maybe_queryset, is_valid_django_model

from graphene_django_extras.utils import get_extra_filters
from graphene_django_extras.fields import DjangoFilterPaginateListField

from .utils import queryset_factory, get_prefetched_attr


class OptimizedDjangoFilterPaginateListField(DjangoFilterPaginateListField):

    def get_queryset(self, root, field_name, field_asts, fragments, **kwargs):
        prefetched = get_prefetched_attr(root, field_name)
        if prefetched:
            return prefetched

        filter_kwargs = {k: v for k,
                         v in kwargs.items() if k in self.filtering_args}
        qs = queryset_factory(self.type.of_type, field_asts,
                              fragments, **kwargs)
        qs = self.filterset_class(data=filter_kwargs, queryset=qs).qs

        return maybe_queryset(qs)

    def list_resolver(self, manager, filterset_class, filtering_args,
                      root, info, **kwargs):

        qs = self.get_queryset(root, info.field_name,
                               info.field_asts, info.fragments, **kwargs)

        # If we've prefetched the queryset, it will be a list object and we don't need to appy the extra filters
        if not isinstance(qs, list) and root and is_valid_django_model(root._meta.model):
            extra_filters = get_extra_filters(root, manager.model)
            qs = qs.filter(**extra_filters)

        if getattr(self, 'pagination', None):
            qs = self.pagination.paginate_queryset(qs, **kwargs)

        return maybe_queryset(qs)
