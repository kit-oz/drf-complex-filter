import json
from typing import Any, Callable, Dict, Optional, Tuple, Type, Union

from django.apps import apps
from django.db.models import Model, Q, QuerySet
from django.utils.module_loading import import_string
from rest_framework.request import Request

from drf_complex_filter.settings import filter_settings


class ComplexFilter:
    """
    A utility class for building complex Django ORM queries from JSON-like filter structures.

    This class allows building complex queries with AND/OR operations, dynamic value computations,
    and efficient handling of related model queries.

    Attributes:
        model: The Django model to filter
        comparisons: Dictionary of available comparison operators
        functions: Dictionary of available value computation functions
        default_comparison: Default comparison function for custom operators
    """

    def __init__(self, model: Optional[Type[Model]] = None):
        """
        Initialize the ComplexFilter.

        Args:
            model: Django model class to filter
        """
        self.model = model
        self.comparisons: Dict[str, Callable] = {}
        self._load_comparisons()

        self.functions: Dict[str, Callable] = {}
        self._load_functions()

        self.default_comparison = self._load_default_comparison()

    def _load_comparisons(self) -> None:
        """Load comparison operators from settings."""
        for comparison_path in filter_settings["COMPARISON_CLASSES"]:
            comparison_module = import_string(comparison_path)()
            self.comparisons.update(comparison_module.get_operators())

    def _load_functions(self) -> None:
        """Load value computation functions from settings."""
        for function_path in filter_settings["VALUE_FUNCTIONS"]:
            function_module = import_string(function_path)()
            self.functions.update(function_module.get_functions())

    def _load_default_comparison(self) -> Optional[Callable]:
        """Load default comparison function from settings."""
        if filter_settings["DEFAULT_COMPARISON_FUNCTION"]:
            return import_string(filter_settings["DEFAULT_COMPARISON_FUNCTION"])
        return None

    def filter_queryset(
        self,
        queryset: QuerySet,
        filters: Union[dict, str, None],
        request: Optional[Request] = None
    ) -> QuerySet:
        """
        Apply complex filters to a queryset.

        Args:
            queryset: Base queryset to filter
            filters: Filter configuration as dict or JSON string
            request: Optional request object for context-aware filtering

        Returns:
            Filtered queryset

        Example:
            >>> filter_config = {
            ...     "type": "and",
            ...     "data": [
            ...         {
            ...             "type": "operator",
            ...             "data": {"attribute": "age", "operator": ">", "value": 18}
            ...         },
            ...         {
            ...             "type": "operator",
            ...             "data": {"attribute": "is_active", "operator": "=", "value": True}
            ...         }
            ...     ]
            ... }
            >>> filtered_qs = complex_filter.filter_queryset(User.objects.all(), filter_config)
        """
        query, annotation = self.generate_query(filters, request)
        if query:
            queryset = queryset.annotate(**annotation).filter(query)

        return queryset

    def generate_query(
        self,
        filters: Union[dict, str, None],
        request: Optional[Request] = None
    ) -> Tuple[Optional[Q], Dict[str, Any]]:
        """
        Generate Django Q object from filter configuration.

        Args:
            filters: Filter configuration as dict or JSON string
            request: Optional request object for context-aware filtering

        Returns:
            Tuple of (Q object for filtering, Dict of annotations)
        """
        if not filters:
            return None, {}

        if isinstance(filters, str):
            try:
                filters = json.loads(filters)
            except (TypeError, json.decoder.JSONDecodeError):
                return None, {}

        return self.generate_query_from_dict(filters, request)

    def generate_query(self, filters: Union[dict, str, None], request: Optional[Request] = None):
        if not filters:
            return None, {}

        if isinstance(filters, str):
            try:
                filters = json.loads(filters)  # Converts string to dictionary
            except (TypeError, json.decoder.JSONDecodeError):
                return None, {}

        return self.generate_query_from_dict(filters, request)

    def generate_query_from_dict(
        self,
        filters: dict,
        request: Optional[Request] = None
    ) -> Tuple[Optional[Q], Dict[str, Any]]:
        """
        Create a Django Q object from a dictionary of filter conditions.

        Args:
            filters: Dictionary containing filter configuration
            request: Optional request object for context-aware filtering

        Returns:
            Tuple of (Q object for filtering, Dict of annotations)

        Raises:
            ValueError: If an invalid operator is specified and no default comparison is set
        """
        query = None
        annotation: Dict[str, Any] = {}

        filter_type = filters["type"]
        if filter_type == "operator":
            query, annotation = self._handle_operator(filters["data"], request)
        elif filter_type in ("and", "or"):
            query, annotation = self._handle_logical_operation(filter_type, filters["data"], request)

        return query, annotation

    def _handle_operator(
        self,
        condition: dict,
        request: Optional[Request]
    ) -> Tuple[Optional[Q], Dict[str, Any]]:
        """Handle single operator condition."""
        operator = condition["operator"]
        attribute = condition["attribute"].replace(".", "__")

        if "___" in attribute:
            attribute, operator, value = self._calculate_subquery(
                attribute, operator, condition.get("value"), request
            )
        else:
            value = self.get_filter_value(condition, request)

        if operator in self.comparisons:
            result = self.comparisons[operator](attribute, value, request, self.model)
        elif self.default_comparison:
            result = self.default_comparison(attribute, operator, value, request, self.model)
        else:
            raise ValueError(f"Operator '{operator}' not found")

        return result if isinstance(result, tuple) else (result, {})

    def _handle_logical_operation(
        self,
        operation: str,
        conditions: list,
        request: Optional[Request]
    ) -> Tuple[Optional[Q], Dict[str, Any]]:
        """Handle AND/OR operations."""
        query = None
        annotation: Dict[str, Any] = {}

        for filter_data in conditions:
            sub_query, sub_annotation = self.generate_query_from_dict(filter_data, request)
            if sub_query:
                if operation == "and":
                    query = query & sub_query if query else sub_query
                else:  # operation == "or"
                    query = query | sub_query if query else sub_query
                annotation.update(sub_annotation)

        return query, annotation

    def get_filter_value(
        self,
        condition: dict,
        request: Optional[Request] = None
    ) -> Any:
        """
        Get the filter value, computing it if necessary using a function.

        Args:
            condition: Filter condition dictionary
            request: Optional request object for context-aware value computation

        Returns:
            Computed or raw filter value
        """
        if "value" not in condition:
            return None

        value = condition["value"]
        if isinstance(value, dict) and "func" in value:
            func = value["func"]
            if func in self.functions:
                kwargs = value.get("kwargs", {})
                return self.functions[func](request=request, model=self.model, **kwargs)

        return value

    @staticmethod
    def _get_model_by_name(model_name: str) -> Optional[Type[Model]]:
        """Get Django model class by its name."""
        all_models = apps.get_models(include_auto_created=True, include_swapped=True)
        for model in all_models:
            if model_name.lower() == model.__name__.lower():
                return model
        return None

    def _calculate_subquery(
        self,
        attribute: str,
        operator: str,
        value: Any,
        request: Optional[Request]
    ) -> Tuple[str, str, Any]:
        """
        Calculate subquery for related model filtering.

        This method handles filtering by related model fields by creating a subquery
        that gets the IDs of matching related objects.

        Args:
            attribute: Field path with model prefix (e.g., "Profile___is_verified")
            operator: Comparison operator
            value: Filter value
            request: Optional request object

        Returns:
            Tuple of (modified attribute, new operator, computed value)
        """
        main_attribute, sub_attribute = attribute.split("___", maxsplit=1)
        sub_model_name = main_attribute.rsplit("__", maxsplit=1)[-1]
        sub_model = self._get_model_by_name(sub_model_name)

        if not sub_model:
            raise ValueError(f"Model '{sub_model_name}' not found")

        filters = {
            "type": "operator",
            "data": {"attribute": sub_attribute, "operator": operator, "value": value},
        }
        sub_query, sub_annotation = ComplexFilter(sub_model).generate_query_from_dict(
            filters, request
        )
        sub_queryset = sub_model.objects.annotate(**sub_annotation).filter(sub_query)

        if "__" in main_attribute:
            # Make reference to current model's ID instead of related model
            sub_model_name = "_" + sub_model_name

        attribute = main_attribute.replace(sub_model_name, "id")
        return attribute, "in", sub_queryset.values_list("id", flat=True)
