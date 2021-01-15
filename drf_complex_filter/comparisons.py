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


class DynamicComparison:
    def get_operators(self):
        return {
            "me": self.current_user,
            "not_me": self.not_current_user,
        }

    @staticmethod
    def current_user(field, value=None, request=None):
        print("REQUEST", request.user)
        if not request or not request.user:
            return Q(**{"{}__isnull".format(field): True})
        return Q(**{"{}".format(field): request.user.id})

    @staticmethod
    def not_current_user(field, value=None, request=None):
        if not request or not request.user:
            return Q(**{"{}__isnull".format(field): False})
        return ~Q(**{"{}".format(field): request.user.id})
