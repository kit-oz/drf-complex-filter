import json
from datetime import datetime
from django.db.models import Q
from rest_framework.test import APITestCase
from rest_framework import status
from parameterized import parameterized

from .models import TestCaseModel
from .fixtures import RECORDS
from .serializer import TestCaseModelSerializer


TEST_CASES = [
    ({"filters": ""},
     TestCaseModel.objects.all()),

    # BASE CHECK FOR ALL FIELD TYPES
    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "group1",
                                      "operator": "=",
                                      "value": "GROUP1"}})},
     TestCaseModel.objects.filter(group1="GROUP1")),

    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "integer",
                                      "operator": "=",
                                      "value": 2}})},
     TestCaseModel.objects.filter(integer=2)),

    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "float",
                                      "operator": "=",
                                      "value": 2}})},
     TestCaseModel.objects.filter(float=2)),

    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "date",
                                      "operator": "=",
                                      "value": "2020-11-01"}})},
     TestCaseModel.objects.filter(date="2020-11-01")),

    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "datetime",
                                      "operator": "=",
                                      "value": "2020-10-31T00:03:00"}})},
     TestCaseModel.objects.filter(datetime="2020-10-31T00:03:00")),

    # CONTAINS AND NOT CONTAINS FILTERS
    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "group1",
                                      "operator": "*",
                                      "value": "P1"}})},
     TestCaseModel.objects.filter(group1__icontains="P1")),

    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "group1",
                                      "operator": "!",
                                      "value": "P1"}})},
     TestCaseModel.objects.exclude(group1__icontains="P1")),

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
     TestCaseModel.objects.filter(group1__in=["GROUP1", "group1"])),

    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "group1",
                                      "operator": "not_in",
                                      "value": ["GROUP1", "group1"]}})},
     TestCaseModel.objects.exclude(group1__in=["GROUP1", "group1"])),

    # MATH COMPARISON OPERATORS
    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "integer",
                                      "operator": "!=",
                                      "value": 2}})},
     TestCaseModel.objects.exclude(integer=2)),

    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "integer",
                                      "operator": "*",
                                      "value": 2}})},
     TestCaseModel.objects.filter(integer=2)),

    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "integer",
                                      "operator": "!",
                                      "value": 2}})},
     TestCaseModel.objects.exclude(integer=2)),

    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "integer",
                                      "operator": ">",
                                      "value": 2}})},
     TestCaseModel.objects.filter(integer__gt=2)),

    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "integer",
                                      "operator": ">=",
                                      "value": 2}})},
     TestCaseModel.objects.filter(integer__gte=2)),

    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "integer",
                                      "operator": "<",
                                      "value": 2}})},
     TestCaseModel.objects.filter(integer__lt=2)),

    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "integer",
                                      "operator": "<=",
                                      "value": 2}})},
     TestCaseModel.objects.filter(integer__lte=2)),

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
     TestCaseModel.objects.filter(group1="GROUP3").filter(group2="GROUP1")),

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
     TestCaseModel.objects.filter(Q(group1="GROUP3") | Q(group2="GROUP1"))),

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
     TestCaseModel.objects.filter(group1="GROUP3").filter(Q(group2="GROUP1") | Q(group2="GROUP2"))),

    # EQUAL CHECK ON EMPTY VALUE
    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "with_empty",
                                      "operator": "=",
                                      "value": ""}})},
     TestCaseModel.objects.filter(Q(with_empty="") | Q(with_empty__isnull=True))),

    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "with_empty",
                                      "operator": "!=",
                                      "value": ""}})},
     TestCaseModel.objects.filter(with_empty__isnull=False).exclude(with_empty="")),

    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "with_empty",
                                      "operator": ">",
                                      "value": ""}})},
     TestCaseModel.objects.filter(with_empty__isnull=False).filter(with_empty__gt="")),

    # BOOLEAN FIELDS
    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "boolean",
                                      "operator": "=",
                                      "value": False}})},
     TestCaseModel.objects.filter(boolean=False)),

    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "boolean",
                                      "operator": "!=",
                                      "value": False}})},
     TestCaseModel.objects.filter(boolean=True)),

    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "id",
                                      "operator": "=",
                                      "value": ""}})},
     TestCaseModel.objects.filter(id__isnull=True)),

    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "date",
                                      "operator": "=",
                                      "value": ""}})},
     TestCaseModel.objects.filter(date__isnull=True)),

    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "date",
                                      "operator": "<",
                                      "value": {"func": "now"}}})},
     TestCaseModel.objects.filter(date__lt=datetime.now())),

    ({"filters": json.dumps({"type": "operator",
                             "data": {"attribute": "date",
                                      "operator": "<",
                                      "value": {"func": "date",
                                                "kwargs": {"year": 2020,
                                                           "month": 10,
                                                           "day": 15}}}})},
     TestCaseModel.objects.filter(date__lt=datetime(2020, 10, 15))),
]


class CommonFilterTests(APITestCase):
    URL = "/test/"

    def setUp(self):
        for record in RECORDS:
            TestCaseModel(**record).save()

    @parameterized.expand(TEST_CASES)
    def test_common_filter(self, query, expected_queryset):
        expected_data = TestCaseModelSerializer(expected_queryset, many=True).data
        response = self.client.get(self.URL, query, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         msg=f"Failed on: {query}"
                             f"\nResponse: {response.data}")
        self.assertEqual(len(response.data), len(expected_data),
                         msg=f"Failed on: {query}"
                             f"\nResponse: {response.data}"
                             f"\nExpected: {expected_data}")
        for result in response.data:
            self.assertIn(result, expected_data,
                          msg=f"Failed on: {query}"
                              f"\nResponse: {response.data}"
                              f"\nExpected: {expected_data}")
