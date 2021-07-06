from django.db import models


class TestCaseModel(models.Model):
    group1 = models.CharField(max_length=10)
    group2 = models.CharField(max_length=10)
    with_empty = models.CharField(max_length=10, blank=True, null=True)
    integer = models.IntegerField()
    float = models.FloatField()
    date = models.DateField()
    datetime = models.DateTimeField()
    user = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    boolean = models.BooleanField()
