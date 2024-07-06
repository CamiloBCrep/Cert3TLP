from rest_framework import serializers 
from core.models import combustible

class CombustibleSerializer(serializers.ModelSerializer):
    class Meta:
        model = combustible
        fields = '__all__'