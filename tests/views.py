from rest_framework.viewsets import ReadOnlyModelViewSet

from drf_complex_filter.filters import ComplexQueryFilter

from .models import TestCaseModel
from .serializer import TestCaseModelSerializer


class TestCaseViewSet(ReadOnlyModelViewSet):
    queryset = TestCaseModel.objects.all()
    serializer_class = TestCaseModelSerializer
    filter_backends = [ComplexQueryFilter]
