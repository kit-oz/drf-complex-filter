from typing import Optional

from django.db.models import Model
from django.db.models import Q
from django.db.models import fields

from drf_complex_filter.settings import filter_settings


class CommonComparison:
    def get_operators(self):
        return {
            "=": self.equal,
            "!=": self.not_equal,
            "*": lambda f, v, r=None, m=None: self.get_q_object(f, v, r, m, "icontains"),
            "!": lambda f, v, r=None, m=None: ~self.get_q_object(f, v, r, m, "icontains"),
            ">": lambda f, v, r=None, m=None: self.get_q_object(f, v, r, m, "gt"),
            ">=": lambda f, v, r=None, m=None: self.get_q_object(f, v, r, m, "gte"),
            "<": lambda f, v, r=None, m=None: self.get_q_object(f, v, r, m, "lt"),
            "<=": lambda f, v, r=None, m=None: self.get_q_object(f, v, r, m, "lte"),
            "in": lambda f, v, r=None, m=None: Q(**{f"{f}__in": v}),
            "not_in": lambda f, v, r=None, m=None: ~Q(**{f"{f}__in": v}),
        }

    def equal(self, field: str, value=None, request=None, model: Model = None):
        if value == "":
            query = Q(**{f"{field}__isnull": True})
            _, target_field = self._get_field_model_by_name(model, field)
            if isinstance(target_field, fields.CharField) or isinstance(target_field, fields.TextField):
                query = query | Q(**{f"{field}__exact": ""})
            return query
        return Q(**{f"{field}": value})

    def not_equal(self, field: str, value=None, request=None, model: Model = None):
        if value == "":
            query = Q(**{f"{field}__isnull": False})
            _, target_field = self._get_field_model_by_name(model, field)
            if isinstance(target_field, fields.CharField) or isinstance(target_field, fields.TextField):
                query = query & ~Q(**{f"{field}": ""})
            return query
        return ~Q(**{f"{field}": value})

    def get_q_object(self, field: str, value=None, request=None, model: Model = None, comparison: str = 'icontains'):
        target_model, field_model = self._get_field_model_by_name(model, field)
        if not field_model.is_relation:
            return Q(**{f"{field}__{comparison}": value})

        return self._related_object_lookup(target_model, field, value, comparison)

    @staticmethod
    def _get_field_model_by_name(model, column_name: str) -> Optional[fields.Field]:
        column_path = column_name.split("__")

        field = None
        current_model = model
        for current_column_name in column_path:
            field = current_model._meta.get_field(current_column_name)
            if field.remote_field:
                current_model = field.remote_field.model

        return current_model, field

    def _related_object_lookup(self, model, field_path, value, comparison):
        lookup_by_model = getattr(model._meta, "lookup_by_model", None)
        if lookup_by_model:
            return lookup_by_model(field_path, value, comparison)

        lookup_fields = getattr(model._meta, "lookup_fields", None)
        if not lookup_fields:
            lookup_fields = filter_settings["DEFAULT_LOOKUP_FIELD"]
        if lookup_fields and hasattr(model, lookup_fields):
            return Q(**{f"{field_path}__{lookup_fields}__{comparison}": value})


class DynamicComparison:
    def get_operators(self):
        return {
            "me": self.current_user,
            "not_me": self.not_current_user,
        }

    @staticmethod
    def current_user(field: str, value=None, request=None, model: Model = None):
        if not request or not request.user:
            return Q(**{f"{field}__isnull": True})
        return Q(**{f"{field}": request.user.id})

    @staticmethod
    def not_current_user(field: str, value=None, request=None, model: Model = None):
        if not request or not request.user:
            return Q(**{f"{field}__isnull": False})
        return ~Q(**{f"{field}": request.user.id})
