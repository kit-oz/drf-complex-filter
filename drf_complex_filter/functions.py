from datetime import datetime


class DateFunctions:
    def get_functions(self):
        return {
            "now": lambda **kwargs: datetime.now(),
            "date": lambda year, month, day, **kwargs: datetime(year, month, day),
        }
