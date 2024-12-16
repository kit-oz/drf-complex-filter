from datetime import datetime
from typing import Any, Callable, Dict

from django.utils.timezone import now


class DateFunctions:
    """
    Built-in date-related functions for dynamic value computation in filters.
    
    These functions can be used in filter queries to compute date values dynamically
    on the server side instead of hardcoding them in the query.
    """

    def get_functions(self) -> Dict[str, Callable[..., Any]]:
        """
        Get all available date functions.

        Returns:
            Dict[str, Callable]: A dictionary mapping function names to their implementations

        Example:
            {
                "type": "operator",
                "data": {
                    "attribute": "created_at",
                    "operator": ">",
                    "value": {"func": "now"}
                }
            }
        """
        return {
            "now": lambda **kwargs: now(),
            "date": lambda year, month, day, **kwargs: datetime(year, month, day),
        }
