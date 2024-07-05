from django.db import models
from django.utils import timezone

combustible_choices = (('PRG'),('PRD'),('PRA'))

class nuevo_proyecto(models.Model):
    estudiante=models.TextField(max_length=50)
    profesor=models.TextField(max_length=50, null=True)
    proy=models.TextField(max_length=255)
    tema=models.TextField(max_length=50)

class combustible(model.Model):
    codigo = models.TextField(max_length=3)
    litros = models.IntegerField()
    fecha_hora = DateTimeField(auto_now_add=True)
    operario = models.TextField(max_length=40)
#    turno = (agregar choose box)