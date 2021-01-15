from rest_framework.filters import BaseFilterBackend

from drf_complex_filter.utils import ComplexFilter
from drf_complex_filter.settings import filter_settings


class ComplexQueryFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filter_string = request.query_params.get(
            filter_settings["QUERY_PARAMETER"], None)
        if not filter_string:
            return queryset

        complex_filter = ComplexFilter()
        query = complex_filter.generate_from_string(filter_string, request)
        if query:
            queryset = queryset.filter(query)

        return queryset
