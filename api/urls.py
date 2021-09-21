from django.urls import path
from rest_framework.routers import DefaultRouter

from api import viewsets, views

urlpatterns = [
    path('command/<int:command_id>/execute/', views.execute, name='execute')
]

router = DefaultRouter()
router.register(r'machine', viewsets.MachineViewSet, basename='machine')
router.register(r'command', viewsets.CommandViewSet, basename='command')
router.register(r'commandoptions', viewsets.CommandOptionsViewSet, basename='commandoptions')
router.register(r'result', viewsets.ResultViewSet, basename='result')

urlpatterns += router.urls