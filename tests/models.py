from django.db import models
from django.db.models import functions


class LookupFieldTestModel(models.Model):
    lookup_field = models.CharField(max_length=64)

    class Meta:
        lookup_fields = "lookup_field"


class MultipleLookupFieldsTestModel(models.Model):
    lookup_field1 = models.CharField(max_length=64)
    lookup_field2 = models.CharField(max_length=64)

    class Meta:
        def lookup_by_model(prefix, value, comparison):
            query = models.Q(**{f"{prefix}__union_field__{comparison}": value})
            annotation = {
                f"{prefix}__union_field": functions.Concat(
                    models.F(f"{prefix}__lookup_field1"),
                    models.Value(" "),
                    models.F(f"{prefix}__lookup_field2"),
                )
            }
            return query, annotation


class TestCaseModel(models.Model):
    group1 = models.CharField(max_length=10)
    group2 = models.CharField(max_length=10)
    with_empty = models.CharField(max_length=10, blank=True, null=True)
    integer = models.IntegerField(blank=True, null=True)
    float = models.FloatField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    boolean = models.BooleanField(default=False)
    simple_lookup = models.ForeignKey(LookupFieldTestModel, on_delete=models.CASCADE, blank=True, null=True)
    multiple_field_lookup = models.ForeignKey(
        MultipleLookupFieldsTestModel, on_delete=models.CASCADE, blank=True, null=True
    )
