from typing import Optional
import json
import re
from django.apps import apps
from django.db.models import Q
from django.db.models import Model
from django.utils.module_loading import import_string

from drf_complex_filter.settings import filter_settings


class ComplexFilter:
    def __init__(self, model: Model = None):
        self.model = model
        self.comparisons = {}
        for comparison_path in filter_settings["COMPARISON_CLASSES"]:
            comparison_module = import_string(comparison_path)()
            self.comparisons.update(comparison_module.get_operators())

        self.functions = {}
        for function_path in filter_settings["VALUE_FUNCTIONS"]:
            function_module = import_string(function_path)()
            self.functions.update(function_module.get_functions())

        self.default_comparison = None
        if filter_settings["DEFAULT_COMPARISON_FUNCTION"]:
            self.default_comparison = import_string(filter_settings["DEFAULT_COMPARISON_FUNCTION"])

    def generate_from_string(self, filter_string: str, request=None) -> Optional[Q]:
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
        annotation = {}
        filter_type = filters["type"]
        if filter_type == "operator":
            condition = filters["data"]
            operator = condition["operator"]

            attribute = condition["attribute"].replace(".", "__")
            if '___' in attribute:
                value = condition.get("value")
                attribute, operator, value = self._calculate_subquery(attribute, operator, value, request)
            else:
                value = self.get_filter_value(condition, request)

            if operator in self.comparisons:
                result = self.comparisons[operator](attribute, value, request, self.model)
            elif self.default_comparison:
                result = self.default_comparison(attribute, operator, value, request, self.model)
            else:
                raise ValueError(f"Operator '{operator}' not found")
            (query, annotation) = result if isinstance(result, tuple) else (result, {})
        elif filter_type == "and":
            for filter_data in filters["data"]:
                sub_query, sub_annotation = self.generate_query_from_dict(filter_data, request)
                if sub_query:
                    query = query & sub_query if query else sub_query
                    annotation.update(sub_annotation)
        elif filter_type == "or":
            for filter_data in filters["data"]:
                sub_query, sub_annotation = self.generate_query_from_dict(filter_data, request)
                if sub_query:
                    query = query | sub_query if query else sub_query
                    annotation.update(sub_annotation)
        return query, annotation

    def get_filter_value(self, condition, request=None):
        if "value" not in condition:
            return

        value = condition["value"]
        if isinstance(value, dict) and "func" in value:
            func = value["func"]
            if func in self.functions:
                kwargs = value["kwargs"] if "kwargs" in value else {}
                return self.functions[func](request=request, model=self.model, **kwargs)

        return value

    @staticmethod
    def _get_model_by_name(model_name):
        all_models = apps.get_models(include_auto_created=True, include_swapped=True)
        for model in all_models:
            if model_name.lower() == model.__name__.lower():
                return model

    def _calculate_subquery(self, attribute, operator, value, request):
        """Вычисление внутренних подзапросов отдельным процессом"""
        main_attribute, sub_attribute = attribute.split('___', maxsplit=1)
        sub_model_name = main_attribute.rsplit('__', maxsplit=1)[-1]
        sub_model = self._get_model_by_name(sub_model_name)

        filters = {"type": "operator", "data": {"attribute": sub_attribute, "operator": operator, "value": value}}
        sub_query, sub_annotation = ComplexFilter(sub_model).generate_query_from_dict(filters, request)
        sub_queryset = sub_model.objects.annotate(**sub_annotation).filter(sub_query)

        if '__' in main_attribute:
            sub_model_name = '_' + sub_model_name  # делаем обращение к ID у текущей модели, а не у связанной
        attribute = main_attribute.replace(sub_model_name, 'id')
        operator = 'in'
        value = sub_queryset.values_list('id', flat=True)
        return attribute, operator, value
