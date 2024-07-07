from django.urls import path, include
from rest_framework import serializers, routers
from . import views
from .views import CombustibleViewSet, CombustiblePorFechaAPIView

router = routers.DefaultRouter()
router.register('combustibles',views.CombustibleViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('combustible/<int:year>/<int:month>/', CombustiblePorFechaAPIView.as_view(), name='combustible_por_fecha'),

]