from rest_framework.routers import DefaultRouter

from api import viewsets

router = DefaultRouter()
router.register(r'machine', viewsets.MachineViewSet, basename='machine')

urlpatterns = router.urls