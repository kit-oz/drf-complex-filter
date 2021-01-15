from django.contrib.auth.models import User
from datetime import date, datetime

RECORDS = [
    {"group1": "GROUP2",
     "group2": "GROUP1",
     "integer": 0,
     "float": 0,
     "date": date(2020, 11, 2),
     "datetime": datetime(2020, 10, 1, 0, 1)},

    {"group1": "GROUP1",
     "group2": "GROUP2",
     "integer": 1,
     "float": 1,
     "date": date(2020, 10, 1),
     "datetime": datetime(2020, 11, 1, 0, 5)},

    {"group1": "group1",
     "group2": "GROUP1",
     "integer": 2,
     "float": 2,
     "date": date(2020, 11, 1),
     "datetime": datetime(2020, 10, 31, 0, 3)},

    {"group1": "GROUP3",
     "group2": "GROUP2",
     "integer": 3,
     "float": 3,
     "date": date(2020, 10, 31),
     "datetime": datetime(2020, 11, 1, 0, 4)},

    {"group1": "GROUP3",
     "group2": "GROUP1",
     "integer": 4,
     "float": 4,
     "date": date(2020, 11, 1),
     "datetime": datetime(2020, 10, 1, 0, 2)},

    {"group1": "GROUP3",
     "group2": "GROUP3",
     "integer": 5,
     "float": 5,
     "date": date(2020, 10, 1),
     "datetime": datetime(2020, 11, 2, 0, 6)},
]
