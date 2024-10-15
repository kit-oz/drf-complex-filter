from rest_framework import serializers

from .models import LookupFieldTestModel, MultipleLookupFieldsTestModel, TestCaseModel


class LookupFieldTestModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LookupFieldTestModel
        fields = "__all__"


class MultipleLookupFieldsTestModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleLookupFieldsTestModel
        fields = "__all__"


class TestCaseModelSerializer(serializers.ModelSerializer):
    simple_lookup = LookupFieldTestModelSerializer(read_only=True)
    multiple_field_lookup = MultipleLookupFieldsTestModelSerializer(read_only=True)

    class Meta:
        model = TestCaseModel
        fields = "__all__"
