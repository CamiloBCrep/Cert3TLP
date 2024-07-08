from django.urls import path, include
from rest_framework import serializers, routers
from . import views
from .views import CombustibleViewSet, CombustibleByCodigoView, CombustibleByYearMonthView

router = routers.DefaultRouter()
router.register('combustibles',views.CombustibleViewSet)

urlpatterns = [
    path('combustibles/<str:codigo>/', CombustibleByCodigoView.as_view(), name='combustible-by-codigo'),
    path('combustibles/<int:year>/<int:month>/', CombustibleByYearMonthView.as_view(), name='combustible-by-year-month'),
    path('',include(router.urls)),
]