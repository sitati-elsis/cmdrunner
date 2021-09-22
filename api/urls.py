from django.views.generic import TemplateView
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as rest_auth_views
from rest_framework.schemas import get_schema_view
from rest_framework.permissions import AllowAny
from rest_framework_nested import routers as drf_nested_routers

from api import viewsets, views

urlpatterns = [
    path('command/<int:command_id>/execute/', views.execute, name='execute'),
    path('login/', rest_auth_views.obtain_auth_token, name='login'),
    path('openapi', get_schema_view(
        title="CMDRunner API",
        description="API for CMDRunner API SSH Platform.",
        version="1.0.0",
        permission_classes=[AllowAny]
    ), name='openapi-schema'),
    path('docs/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
]

router = DefaultRouter()
router.register(r'machine', viewsets.MachineViewSet, basename='machine')
router.register(r'result', viewsets.ResultViewSet, basename='result')
router.register(r'signup', viewsets.SignupViewSet, basename='signup')

urlpatterns += router.urls

router = drf_nested_routers.SimpleRouter()
router.register(r'command', viewsets.CommandViewSet)

domains_router = drf_nested_routers.NestedSimpleRouter(router, r'command', lookup='command')
domains_router.register(r'commandoption', viewsets.CommandOptionsViewSet, basename='commandoptions')

urlpatterns += router.urls
urlpatterns += domains_router.urls