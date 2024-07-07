from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class codigoPlanta(models.Model):
    clave = models.CharField(max_length=3, unique=True)
    descripcion = models.CharField(max_length=100)
    productos = models.ManyToManyField(producto, related_name='codigos')

    def __str__(self):
        #return f'{self.clave} - {self.descripcion}'
        return self.clave
    
TURNO_CHOICES = (('AM','AM'),
                 ('PM','PM'),
                 ('MM','MM')
)

class combustible(models.Model):
    codigo = models.ForeignKey(codigoPlanta, on_delete=models.CASCADE)
    producto = models.ForeignKey(producto, on_delete=models.CASCADE)
    litros = models.IntegerField()
    fecha_hora = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now_add=True)
    usuario_modificador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='modificaciones')
    eliminado = models.BooleanField(default=False)
    operario = models.ForeignKey(User, on_delete=models.CASCADE)
    turno = models.CharField(
        max_length=2,
        choices=TURNO_CHOICES,
        default='-'
    )

    def __str__(self):
        return f'{self.codigo} - {self.fecha_hora.strftime("%d-%m-%Y %H:%M")} - {self.fecha_modificacion.strftime("%d-%m-%Y %H:%M")}'
    
    def eliminar(self):
        self.eliminado = True
        self.save()