from django.conf import settings

DEFAULTS = {
    "COMPARISON_CLASSES": [
        "drf_complex_filter.comparisons.CommonComparison",
        "drf_complex_filter.comparisons.DynamicComparison",
    ],
    "QUERY_PARAMETER": "filters",
}

COMPLEX_FILTER_SETTINGS = getattr(settings, "COMPLEX_FILTER_SETTINGS", {})

filter_settings = {**DEFAULTS, **COMPLEX_FILTER_SETTINGS}
