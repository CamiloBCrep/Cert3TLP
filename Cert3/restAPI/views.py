from rest_framework import serializers, viewsets, generics
from core.models import combustible
from .serializers import CombustibleSerializer


class CombustibleViewSet(viewsets.ModelViewSet):
    queryset = combustible.objects.all()
    serializer_class = CombustibleSerializer

class CombustiblePorFechaAPIView(generics.ListAPIView):
    serializer_class = CombustibleSerializer

    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        return combustible.objects.filter(fecha_hora__year=year, fecha_hora__month=month)