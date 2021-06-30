import re
from typing import Optional
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

    def generate_from_string(self, filter_string: str, request=None) -> Optional[Q]:
        try:
            filters = json.loads(filter_string)
        except (TypeError, json.decoder.JSONDecodeError):
            filters = self._parse_filter_string(filter_string)
        if not filters:
            return None

        return self.generate_query_from_dict(filters, request)

    def _parse_filter_string(self, filter_string: str):
        filters = [self._parse_and_filters(filter) for filter in filter_string.split("^NQ")]
        return {"type": "or", "data": filters} if len(filters) > 1 else None if len(filters) == 0 else filters[0]

    def _parse_and_filters(self, filter_string: str):
        filters = [self._parse_or_filters(filter) for filter in filter_string.split("^AND")]
        return {"type": "and", "data": filters} if len(filters) > 1 else None if len(filters) == 0 else filters[0]

    def _parse_or_filters(self, filter_string: str):
        filters = [self._parse_operator(filter) for filter in filter_string.split("^OR")]
        return {"type": "or", "data": filters} if len(filters) > 1 else None if len(filters) == 0 else filters[0]

    def _parse_operator(self, filter_string: str):
        operators = "|".join(key.replace("*", "\\*") for key in self.comparisons.keys())
        regex = re.compile(operators)
        operator_search = regex.search(filter_string)
        if not operator_search:
            return None
        operator = operator_search.group()
        parsed = filter_string.split(operator, 1)
        filters = {"type": "operator", "data": {"attribute": parsed[0], "operator": operator, "value": parsed[1]}}
        return filters

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
                attribute = condition["attribute"].replace(".", "__")
                value = condition["value"] if "value" in condition else None
                query = self.comparisons[operator](attribute, value, request)
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
