from django.db import models
from django.utils import timezone



class nuevo_proyecto(models.Model):
    estudiante=models.TextField(max_length=50)
    profesor=models.TextField(max_length=50, null=True)
    proy=models.TextField(max_length=255)
    tema=models.TextField(max_length=50)

CODIGO_CHOICES = (('PRG'),('PRD'),('PRA'))
TURNO_CHOICES = (('AM'),('PM'),('MM'))

class combustible(model.Model):
    codigo = models.ChoiceField(
        max_length=3,
        choices=CODIGO_CHOICES,
        default='-'
    )
    litros = models.IntegerField()
    fecha_hora = models.DateTimeField(auto_now_add=True)
    operario = models.ForeignKey(User, on_delete=models.CASCADE)
    turno = models.ChoiceField(
        max_length=2,
        choices=TURNO_CHOICES,
        default='-'
    )