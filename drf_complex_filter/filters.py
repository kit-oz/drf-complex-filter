import json

from rest_framework.filters import BaseFilterBackend

from .utils import generate_query_from_dict


class ComplexQueryFilter(BaseFilterBackend):
    @staticmethod
    def _get_filters(request) -> (dict, None):
        filter_string = request.query_params.get("filters", None)
        try:
            filters = json.loads(filter_string)
        except (TypeError, json.decoder.JSONDecodeError):
            filters = None
        return filters

    def filter_queryset(self, request, queryset, view):
        filters = self._get_filters(request)
        if filters:
            query = generate_query_from_dict(filters=filters)
            if query:
                queryset = queryset.filter(query)

        return queryset
