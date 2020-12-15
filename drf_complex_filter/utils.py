import json
from django.db.models import Q


OPERATORS = {
    "=": lambda k, v: Q(**{"{}".format(k): v}),
    "!=": lambda k, v: ~Q(**{"{}".format(k): v}),
    ">": lambda k, v: Q(**{"{}__gt".format(k): v}),
    ">=": lambda k, v: Q(**{"{}__gte".format(k): v}),
    "<": lambda k, v: Q(**{"{}__lt".format(k): v}),
    "<=": lambda k, v: Q(**{"{}__lte".format(k): v}),
    "*": lambda k, v: Q(**{"{}__icontains".format(k): v}),
    "!": lambda k, v: ~Q(**{"{}__icontains".format(k): v}),
    "cont": lambda k, v: Q(**{"{}__contains".format(k): v}),
    "ncnt": lambda k, v: ~Q(**{"{}__contains".format(k): v}),
}


def parse_filter_string(filter_string: str) -> dict:
    try:
        filters = json.loads(filter_string)
    except (TypeError, json.decoder.JSONDecodeError):
        filters = None
    return filters


def generate_query_from_dict(filters: dict) -> Q:
    """Creating a Django Q object from a dictionary

    :param filters: dictionary
    :return: Django Q object
    """
    query = None
    filter_type = filters["type"]
    if filter_type == "operator":
        condition = filters["data"]
        operator = condition["operator"]
        if operator in OPERATORS:
            query = OPERATORS[operator](
                condition["attribute"], condition["value"]
            )
    elif filter_type == "and":
        for filter_data in filters["data"]:
            sub_query = generate_query_from_dict(filter_data)
            if sub_query:
                query = query & sub_query if query else sub_query
    elif filter_type == "or":
        for filter_data in filters["data"]:
            sub_query = generate_query_from_dict(filter_data)
            if sub_query:
                query = query | sub_query if query else sub_query
    return query
