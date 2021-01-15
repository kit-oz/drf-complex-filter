import json
from django.db.models import Q
from django.utils.module_loading import import_string

from drf_complex_filter.settings import filter_settings


class ComplexFilter:
    def __init__(self):
        self.comparisons = {}
        for comparison_path in filter_settings["COMPARISON_CLASSES"]:
            comparison_module = import_string(comparison_path)()
            self.comparisons.update(comparison_module.get_operators())

    def generate_from_string(self, filter_string: str, request=None) -> (Q, None):
        try:
            filters = json.loads(filter_string)
        except (TypeError, json.decoder.JSONDecodeError):
            return None

        return self.generate_query_from_dict(filters, request)

    def generate_query_from_dict(self, filters: dict, request=None) -> Q:
        """Creating a Django Q object from a dictionary

        :param filters: dictionary
        :param request: request object
        :return: Django Q object
        """
        query = None
        filter_type = filters["type"]
        if filter_type == "operator":
            condition = filters["data"]
            operator = condition["operator"]
            if operator in self.comparisons:
                query = self.comparisons[operator](condition["attribute"],
                                                   condition["value"],
                                                   request)
        elif filter_type == "and":
            for filter_data in filters["data"]:
                sub_query = self.generate_query_from_dict(filter_data, request)
                if sub_query:
                    query = query & sub_query if query else sub_query
        elif filter_type == "or":
            for filter_data in filters["data"]:
                sub_query = self.generate_query_from_dict(filter_data, request)
                if sub_query:
                    query = query | sub_query if query else sub_query
        return query
