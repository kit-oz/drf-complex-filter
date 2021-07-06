from django.db.models import Q


class CommonComparison:
    def get_operators(self):
        return {
            "=": self.equal,
            "!=": self.not_equal,
            "*": lambda f, v, r=None: Q(**{f"{f}__icontains": v}),
            "!": lambda f, v, r=None: ~Q(**{f"{f}__icontains": v}),
            ">": lambda f, v, r=None: Q(**{f"{f}__gt": v}),
            ">=": lambda f, v, r=None: Q(**{f"{f}__gte": v}),
            "<": lambda f, v, r=None: Q(**{f"{f}__lt": v}),
            "<=": lambda f, v, r=None: Q(**{f"{f}__lte": v}),
            "in": lambda f, v, r=None: Q(**{f"{f}__in": v}),
            "not_in": lambda f, v, r=None: ~Q(**{f"{f}__in": v}),
        }

    @staticmethod
    def equal(field, value=None, request=None):
        if value == "":
            return Q(**{f"{field}__isnull": True}) | Q(**{f"{field}__exact": ""})
        return Q(**{f"{field}": value})

    @staticmethod
    def not_equal(field, value=None, request=None):
        if value == "":
            return Q(**{f"{field}__isnull": False}) & ~Q(**{f"{field}": ""})
        return ~Q(**{f"{field}": value})


class DynamicComparison:
    def get_operators(self):
        return {
            "me": self.current_user,
            "not_me": self.not_current_user,
        }

    @staticmethod
    def current_user(field, value=None, request=None):
        if not request or not request.user:
            return Q(**{"{}__isnull".format(field): True})
        return Q(**{"{}".format(field): request.user.id})

    @staticmethod
    def not_current_user(field, value=None, request=None):
        if not request or not request.user:
            return Q(**{"{}__isnull".format(field): False})
        return ~Q(**{"{}".format(field): request.user.id})
