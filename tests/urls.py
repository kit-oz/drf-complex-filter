from rest_framework import routers

from .views import TestCaseViewSet


router = routers.SimpleRouter()
router.register(r"test", TestCaseViewSet)
urlpatterns = router.urls
