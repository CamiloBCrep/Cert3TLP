from django.urls import path, include
from rest_framework import serializers, routers
from . import views
from .views import CombustibleViewSet

router = routers.DefaultRouter()
router.register('combustibles',views.CombustibleViewSet)

urlpatterns = [
    path('',include(router.urls))
]