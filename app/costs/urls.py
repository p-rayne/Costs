from rest_framework import routers
from app.costs import viewsets

router = routers.DefaultRouter()
router.register(r"costs", viewsets.CostViewSet)
urlpatterns = router.urls
