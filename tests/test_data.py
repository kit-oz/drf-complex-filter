import json

from .serializer import TestCaseModelSerializer
from .fixtures import RECORDS

serialized_data = TestCaseModelSerializer(RECORDS, many=True).data

TEST_COMMON = [
    ({"filters": ""},
     serialized_data),

    # BASE CHECK FOR ALL FIELD TYPES
    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "group1",
                                      "operator": "=",
                                      "value": "GROUP1"}})},
     [r for r in serialized_data if r["group1"] == "GROUP1"]),

    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "integer",
                                      "operator": "=",
                                      "value": 2}})},
     [r for r in serialized_data if r["integer"] == 2]),

    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "float",
                                      "operator": "=",
                                      "value": 2}})},
     [r for r in serialized_data if r["float"] == 2]),

    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "date",
                                      "operator": "=",
                                      "value": "2020-11-01"}})},
     [r for r in serialized_data if r["date"] == "2020-11-01"]),

    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "datetime",
                                      "operator": "=",
                                      "value": "2020-10-31T00:03:00"}})},
     [r for r in serialized_data if r["datetime"] == "2020-10-31T00:03:00"]),

    # CONTAINS AND NOT CONTAINS FILTERS
    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "group1",
                                      "operator": "*",
                                      "value": "P1"}})},
     [r for r in serialized_data
      if r["group1"] == "GROUP1" or r["group1"] == "group1"]),

    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "group1",
                                      "operator": "!",
                                      "value": "P1"}})},
     [r for r in serialized_data
      if r["group1"] != "GROUP1" and r["group1"] != "group1"]),

    # IN ARRAY AND NOT IN ARRAY
    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "group1",
                                      "operator": "in",
                                      "value": ["unknown string"]}})},
     []),

    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "group1",
                                      "operator": "in",
                                      "value": ["GROUP1", "group1"]}})},
     [r for r in serialized_data
      if r["group1"] == "GROUP1" or r["group1"] == "group1"]),

    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "group1",
                                      "operator": "not_in",
                                      "value": ["GROUP1", "group1"]}})},
     [r for r in serialized_data
      if r["group1"] != "GROUP1" and r["group1"] != "group1"]),

    # MATH COMPARISON OPERATORS
    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "integer",
                                      "operator": "!=",
                                      "value": 2}})},
     [r for r in serialized_data if r["integer"] != 2]),

    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "integer",
                                      "operator": "*",
                                      "value": 2}})},
     [r for r in serialized_data if r["integer"] == 2]),

    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "integer",
                                      "operator": "!",
                                      "value": 2}})},
     [r for r in serialized_data if r["integer"] != 2]),

    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "integer",
                                      "operator": ">",
                                      "value": 2}})},
     [r for r in serialized_data if r["integer"] > 2]),

    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "integer",
                                      "operator": ">=",
                                      "value": 2}})},
     [r for r in serialized_data if r["integer"] >= 2]),

    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "integer",
                                      "operator": "<",
                                      "value": 2}})},
     [r for r in serialized_data if r["integer"] < 2]),

    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "integer",
                                      "operator": "<=",
                                      "value": 2}})},
     [r for r in serialized_data if r["integer"] <= 2]),

    # LOGICAL AND GROUP
    ({"filters": json.dumps({"type": "and",
                             "data": [{"type": "operator",
                                       "data": {"attribute": "group1",
                                                "operator": "=",
                                                "value": "GROUP3"}},
                                      {"type": "operator",
                                       "data": {"attribute": "group2",
                                                "operator": "=",
                                                "value": "GROUP1"}}]})},
     [r for r in serialized_data
      if r["group1"] == "GROUP3" and r["group2"] == "GROUP1"]),

    # LOGICAL OR GROUP
    ({"filters": json.dumps({"type": "or",
                             "data": [{"type": "operator",
                                       "data": {"attribute": "group1",
                                                "operator": "=",
                                                "value": "GROUP3"}},
                                      {"type": "operator",
                                       "data": {"attribute": "group2",
                                                "operator": "=",
                                                "value": "GROUP1"}}]})},
     [r for r in serialized_data
      if r["group1"] == "GROUP3" or r["group2"] == "GROUP1"]),

    # NESTED GROUPS
    ({"filters": json.dumps({"type": "and",
                             "data": [{"type": "operator",
                                       "data": {"attribute": "group1",
                                                "operator": "=",
                                                "value": "GROUP3"}},
                                      {"type": "or",
                                       "data": [
                                           {"type": "operator",
                                            "data": {"attribute": "group2",
                                                     "operator": "=",
                                                     "value": "GROUP1"}},
                                           {"type": "operator",
                                            "data": {"attribute": "group2",
                                                     "operator": "=",
                                                     "value": "GROUP2"}}
                                       ]}]})},
     [r for r in serialized_data
      if r["group1"] == "GROUP3"
      and (r["group2"] == "GROUP1" or r["group2"] == "GROUP2")]),

]
