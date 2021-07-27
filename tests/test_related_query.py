import json
from django.db.models import Q
from rest_framework.test import APITestCase
from rest_framework import status
from parameterized import parameterized

from .models import TestCaseModel
from .models import LookupFieldTestModel
from .models import MultipleLookupFieldsTestModel
from .serializer import TestCaseModelSerializer


TEST_CASES = [
    (
        {
            "filters": json.dumps(
                {
                    "type": "operator",
                    "data": {"attribute": "simple_lookup.lookup_field", "operator": "=", "value": "value1"},
                }
            )
        },
        TestCaseModel.objects.filter(simple_lookup__lookup_field="value1"),
    ),
    (
        {
            "filters": json.dumps(
                {
                    "type": "operator",
                    "data": {"attribute": "simple_lookup.lookup_field", "operator": "*", "value": "value"},
                }
            )
        },
        TestCaseModel.objects.filter(simple_lookup__lookup_field__icontains="value"),
    ),
    (
        {
            "filters": json.dumps(
                {
                    "type": "operator",
                    "data": {"attribute": "simple_lookup", "operator": "*", "value": "value"},
                }
            )
        },
        TestCaseModel.objects.filter(simple_lookup__lookup_field__icontains="value"),
    ),
    (
        {
            "filters": json.dumps(
                {
                    "type": "operator",
                    "data": {"attribute": "simple_lookup", "operator": "!", "value": "value"},
                }
            )
        },
        TestCaseModel.objects.exclude(simple_lookup__lookup_field__icontains="value"),
    ),
    (
        {
            "filters": json.dumps(
                {
                    "type": "operator",
                    "data": {"attribute": "simple_lookup", "operator": ">", "value": "value1"},
                }
            )
        },
        TestCaseModel.objects.filter(simple_lookup__lookup_field__gt="value1"),
    ),
    (
        {
            "filters": json.dumps(
                {
                    "type": "operator",
                    "data": {"attribute": "simple_lookup", "operator": "<", "value": "value2"},
                }
            )
        },
        TestCaseModel.objects.filter(simple_lookup__lookup_field__lt="value2"),
    ),

    (
        {
            "filters": json.dumps(
                {
                    "type": "operator",
                    "data": {"attribute": "multiple_field_lookup", "operator": "*", "value": "value2"},
                }
            )
        },
        TestCaseModel.objects.filter(
            Q(multiple_field_lookup__lookup_field1__icontains="value2")
            | Q(multiple_field_lookup__lookup_field2__icontains="value2")
        ),
    ),

    (
        {
            "filters": json.dumps(
                {
                    "type": "operator",
                    "data": {"attribute": "multiple_field_lookup", "operator": "*", "value": "value1 value2"},
                }
            )
        },
        TestCaseModel.objects
        .filter(Q(multiple_field_lookup__lookup_field1__icontains="value1"))
        .filter(Q(multiple_field_lookup__lookup_field2__icontains="value2")),
    ),

    (
        {
            "filters": json.dumps(
                {
                    "type": "operator",
                    "data": {"attribute": "multiple_field_lookup", "operator": ">", "value": "value2"},
                }
            )
        },
        TestCaseModel.objects.filter(multiple_field_lookup__lookup_field1__gt="value1")
    ),
]


class RelatedQueryTests(APITestCase):
    URL = "/test/"

    def setUp(self):
        lookup_field_record1 = LookupFieldTestModel(lookup_field="value1")
        lookup_field_record1.save()
        lookup_field_record2 = LookupFieldTestModel(lookup_field="value2")
        lookup_field_record2.save()
        multiple_lookup_fields_record1 = MultipleLookupFieldsTestModel(
            lookup_field1="value1",
            lookup_field2="value2",
        )
        multiple_lookup_fields_record1.save()
        multiple_lookup_fields_record2 = MultipleLookupFieldsTestModel(
            lookup_field1="value2",
            lookup_field2="value3",
        )
        multiple_lookup_fields_record2.save()
        multiple_lookup_fields_record3 = MultipleLookupFieldsTestModel(
            lookup_field1="value4",
            lookup_field2="value5",
        )
        multiple_lookup_fields_record3.save()
        TestCaseModel(
            group1="g1",
            group2="g2",
            simple_lookup=lookup_field_record1,
            multiple_field_lookup=multiple_lookup_fields_record1,
        ).save()
        TestCaseModel(
            group1="g1",
            group2="g2",
            simple_lookup=lookup_field_record2,
            multiple_field_lookup=multiple_lookup_fields_record2,
        ).save()
        TestCaseModel(
            group1="g1",
            group2="g2",
            multiple_field_lookup=multiple_lookup_fields_record3,
        ).save()

    @parameterized.expand(TEST_CASES)
    def test_related_field(self, query, expected_queryset):
        expected_data = TestCaseModelSerializer(expected_queryset, many=True).data
        response = self.client.get(self.URL, query, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=f"Failed on: {query}" f"\nResponse: {response}")
        self.assertEqual(
            len(response.data),
            len(expected_data),
            msg=f"Failed on: {query}" f"\nResponse: {response.data}" f"\nExpected: {expected_data}",
        )
        for result in response.data:
            self.assertIn(
                result,
                expected_data,
                msg=f"Failed on: {query}" f"\nResponse: {response.data}" f"\nExpected: {expected_data}",
            )
