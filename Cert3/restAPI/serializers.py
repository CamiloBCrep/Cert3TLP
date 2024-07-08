from rest_framework import serializers 
from core.models import combustible
from django.contrib.auth.models import User  # Suponiendo que User es tu modelo de usuarios

class CombustibleSerializer(serializers.ModelSerializer):
    #usuario_modificador = serializers.SerializerMethodField()
    operario = serializers.SerializerMethodField()
    codigo = serializers.SerializerMethodField()
    fecha = serializers.SerializerMethodField()
    hora = serializers.SerializerMethodField()


    class Meta:
        model = combustible
        fields = ('codigo', 'litros', 'fecha', 'hora', 'turno', 'operario')

    def get_usuario_modificador(self, obj):
        return obj.usuario_modificador.username if obj.usuario_modificador else None
    
    def get_codigo(self, obj):
        return obj.codigo.clave if obj.codigo else None
    
    def get_fecha(self, obj):
        return obj.fecha_hora.strftime('%Y-%m-%d') if obj.fecha_hora else None

    def get_hora(self, obj):
        return obj.fecha_hora.strftime('%H:%M:%S') if obj.fecha_hora else None

    def get_operario(self, obj):
        return obj.operario.username if obj.operario else None