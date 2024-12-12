from django.db import models
from django.utils import timezone

# Create your models here.
class Usuario(models.Model):    
    nombre = models.CharField(max_length=50)
    edad = models.IntegerField()

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    puede_tener_promociones = models.BooleanField()

    def __str__(self):
        return self.nombre

class Promocion(models.Model):
    nombre = models.CharField(unique=True, max_length=50)
    descripcion = models.CharField(max_length=200)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    usuario = models.ManyToManyField(Usuario)
    descuento = models.IntegerField()
    fecha_inicio = models.DateField()
    fecha_fin  = models.DateField()
    activa = models.BooleanField(default=False)


