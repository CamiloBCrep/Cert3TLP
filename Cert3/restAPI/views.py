from rest_framework import serializers, viewsets
from core.models import combustible
from .serializers import CombustibleSerializer

class CombustibleViewSet(viewsets.ModelViewSet):
    queryset = combustible.objects.all()
    #Gestión de la información a mostrar por el API
    serializer_class = CombustibleSerializer
