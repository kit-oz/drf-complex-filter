from typing import Optional, Type

from django.db.models import Model, QuerySet
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet

from drf_complex_filter.settings import filter_settings
from drf_complex_filter.utils import ComplexFilter


class ComplexQueryFilter:
    """
    A Django REST Framework filter backend that enables complex filtering through JSON-based query parameters.
    
    This filter backend allows for complex AND/OR operations, dynamic value computations,
    and efficient handling of related model queries.
    
    Usage:
        class UserViewSet(ModelViewSet):
            queryset = User.objects.all()
            filter_backends = [ComplexQueryFilter]
    """

    def filter_queryset(
        self,
        request: Request,
        queryset: QuerySet,
        view: Type[ViewSet]
    ) -> QuerySet:
        """
        Apply the complex filter to the queryset based on request parameters.

        Args:
            request: The incoming request containing filter parameters
            queryset: The initial queryset to filter
            view: The viewset instance

        Returns:
            QuerySet: Filtered queryset based on the complex filter conditions

        Example:
            GET /api/users/?filters={"type":"operator","data":{"attribute":"age","operator":">","value":18}}
        """
        filter_string: Optional[str] = request.query_params.get(
            filter_settings["QUERY_PARAMETER"], None
        )

        complex_filter = ComplexFilter(model=queryset.model)
        queryset = complex_filter.filter_queryset(
            queryset=queryset,
            filters=filter_string,
            request=request
        )

        return queryset

    def get_schema_operation_parameters(self, view):
        """
        Define the schema operation parameters for inclusion in the OpenAPI schema.
        """
        return []
