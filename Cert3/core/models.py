from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

CODIGO_CHOICES = (
    ('PRG', 'PRG'),
    ('PRD', 'PRD'),
    ('PRA', 'PRA'),
    ('RPG','RPG')
)
TURNO_CHOICES = (('AM','AM'),
                 ('PM','PM'),
                 ('MM','MM')
)

class combustible(models.Model):
    codigo = models.CharField(
        max_length=3,
        choices=CODIGO_CHOICES,
        default='-'
    )
    litros = models.IntegerField()
    fecha_hora = models.DateTimeField(auto_now_add=True)
    operario = models.ForeignKey(User, on_delete=models.CASCADE)
    turno = models.CharField(
        max_length=2,
        choices=TURNO_CHOICES,
        default='-'
    )

    def __str__(self):
        return f'{self.codigo} - {self.fecha_hora.strftime("%d-%m-%Y %H:%M")}'