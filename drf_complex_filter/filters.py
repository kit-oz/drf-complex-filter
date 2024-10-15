from drf_complex_filter.settings import filter_settings
from drf_complex_filter.utils import ComplexFilter


class ComplexQueryFilter:
    def filter_queryset(self, request, queryset, view):
        filter_string = request.query_params.get(
            filter_settings["QUERY_PARAMETER"], None
        )

        complex_filter = ComplexFilter(model=queryset.model)
        queryset = complex_filter.filter_queryset(
            queryset=queryset, filters=filter_string, request=request
        )

        return queryset
