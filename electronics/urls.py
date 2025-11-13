from rest_framework.routers import DefaultRouter
from .views import NetworkNodeViewSet

app_name = 'electronics'

router = DefaultRouter()
router.register(r'network-nodes', NetworkNodeViewSet, basename='networknode')

urlpatterns = router.urls