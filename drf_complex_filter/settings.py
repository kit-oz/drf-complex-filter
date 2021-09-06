from django.conf import settings

DEFAULTS = {
    "COMPARISON_CLASSES": [
        "drf_complex_filter.comparisons.CommonComparison",
        "drf_complex_filter.comparisons.DynamicComparison",
    ],
    "VALUE_FUNCTIONS": [
        "drf_complex_filter.functions.DateFunctions"
    ],
    "QUERY_PARAMETER": "filters",
    "DEFAULT_LOOKUP_FIELD": None,
}

COMPLEX_FILTER_SETTINGS = getattr(settings, "COMPLEX_FILTER_SETTINGS", {})

filter_settings = {**DEFAULTS, **COMPLEX_FILTER_SETTINGS}
