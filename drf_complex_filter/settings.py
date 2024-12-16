"""
Django Rest Framework Complex Filter settings module.

This module handles the configuration settings for the DRF Complex Filter package.
Settings can be overridden in your Django settings file using the COMPLEX_FILTER_SETTINGS dictionary.
"""

from typing import Any, Dict

from django.conf import settings

DEFAULTS: Dict[str, Any] = {
    # Classes that provide filter operators
    "COMPARISON_CLASSES": [
        "drf_complex_filter.comparisons.CommonComparison",
        "drf_complex_filter.comparisons.DynamicComparison",
    ],
    
    # Classes that provide dynamic value functions
    "VALUE_FUNCTIONS": [
        "drf_complex_filter.functions.DateFunctions",
    ],
    
    # The query parameter name for filters in the URL
    "QUERY_PARAMETER": "filters",
    
    # Default field to use when no field is specified
    "DEFAULT_LOOKUP_FIELD": None,
    
    # Default comparison function to use when no operator is specified
    "DEFAULT_COMPARISON_FUNCTION": None,
}

# Get user-defined settings
COMPLEX_FILTER_SETTINGS: Dict[str, Any] = getattr(settings, "COMPLEX_FILTER_SETTINGS", {})

# Merge default settings with user-defined settings
filter_settings: Dict[str, Any] = {**DEFAULTS, **COMPLEX_FILTER_SETTINGS}
