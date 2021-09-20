from rest_framework.routers import DefaultRouter

from api import viewsets

router = DefaultRouter()
router.register(r'machine', viewsets.MachineViewSet, basename='machine')
router.register(r'command', viewsets.CommandViewSet, basename='command')
router.register(r'commandoptions', viewsets.CommandOptionsViewSet, basename='commandoptions')

urlpatterns = router.urls