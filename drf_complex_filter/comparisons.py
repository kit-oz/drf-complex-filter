from django.db.models import Q


class CommonComparison:
    def get_operators(self):
        return {
            "=": lambda f, v, r=None: Q(**{"{}".format(f): v}),
            "!=": lambda f, v, r=None: ~Q(**{"{}".format(f): v}),
            "*": lambda f, v, r=None: Q(**{"{}__icontains".format(f): v}),
            "!": lambda f, v, r=None: ~Q(**{"{}__icontains".format(f): v}),
            ">": lambda f, v, r=None: Q(**{"{}__gt".format(f): v}),
            ">=": lambda f, v, r=None: Q(**{"{}__gte".format(f): v}),
            "<": lambda f, v, r=None: Q(**{"{}__lt".format(f): v}),
            "<=": lambda f, v, r=None: Q(**{"{}__lte".format(f): v}),
            "in": lambda f, v, r=None: Q(**{"{}__in".format(f): v}),
            "not_in": lambda f, v, r=None: ~Q(**{"{}__in".format(f): v}),
        }
