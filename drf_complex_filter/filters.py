from rest_framework.filters import BaseFilterBackend

from .utils import generate_query_from_dict
from .utils import parse_filter_string


class ComplexQueryFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filter_string = request.query_params.get("filters", None)
        filters = parse_filter_string(filter_string)
        if filters:
            query = generate_query_from_dict(filters=filters)
            if query:
                queryset = queryset.filter(query)

        return queryset
