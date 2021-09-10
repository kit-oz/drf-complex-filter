from django.utils.timezone import now


class DateFunctions:
    def get_functions(self):
        return {
            "now": lambda **kwargs: now(),
            "date": lambda year, month, day, **kwargs: datetime(year, month, day),
        }
