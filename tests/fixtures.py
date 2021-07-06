from datetime import date, datetime

RECORDS = [
    {"group1": "GROUP2",
     "group2": "GROUP1",
     "with_empty": "filled",
     "integer": 0,
     "float": 0,
     "date": date(2020, 11, 2),
     "datetime": datetime(2020, 10, 1, 0, 1),
     "boolean": True},

    {"group1": "GROUP1",
     "group2": "GROUP2",
     "integer": 1,
     "float": 1,
     "date": date(2020, 10, 1),
     "datetime": datetime(2020, 11, 1, 0, 5),
     "boolean": True},

    {"group1": "group1",
     "group2": "GROUP1",
     "with_empty": "",
     "integer": 2,
     "float": 2,
     "date": date(2020, 11, 1),
     "datetime": datetime(2020, 10, 31, 0, 3),
     "boolean": True},

    {"group1": "GROUP3",
     "group2": "GROUP2",
     "with_empty": "filled",
     "integer": 3,
     "float": 3,
     "date": date(2020, 10, 31),
     "datetime": datetime(2020, 11, 1, 0, 4),
     "boolean": False},

    {"group1": "GROUP3",
     "group2": "GROUP1",
     "integer": 4,
     "float": 4,
     "date": date(2020, 11, 1),
     "datetime": datetime(2020, 10, 1, 0, 2),
     "boolean": True},

    {"group1": "GROUP3",
     "group2": "GROUP3",
     "with_empty": "filled",
     "integer": 5,
     "float": 5,
     "date": date(2020, 10, 1),
     "datetime": datetime(2020, 11, 2, 0, 6),
     "boolean": False},
]
