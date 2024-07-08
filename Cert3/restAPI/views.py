from rest_framework import serializers, viewsets, generics,status
from core.models import combustible
from .serializers import CombustibleSerializer
from rest_framework.response import Response

class CombustibleViewSet(viewsets.ModelViewSet):
    queryset = combustible.objects.all()
    serializer_class = CombustibleSerializer

class CombustibleByCodigoView(generics.ListAPIView):
    serializer_class = CombustibleSerializer

    def get_queryset(self):
        codigo = self.kwargs['codigo']
        queryset = combustible.objects.filter(codigo__clave=codigo)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CombustibleByYearMonthView(generics.ListAPIView):
    serializer_class = CombustibleSerializer

    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        queryset = combustible.objects.filter(fecha_hora__year=year, fecha_hora__month=month)
        print(f"Debug: Filtrando por año {year} y mes {month}, obteniendo {queryset.count()} registros")
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)