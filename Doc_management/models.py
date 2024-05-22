from django.db import models

# Create your models here.

class Taller(models.Model):
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.nombre}"

class Estudiante(models.Model):
    cedula = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=15)
    taller = models.ForeignKey(Taller, on_delete=models.CASCADE)
    edad = models.CharField(max_length=10)
    image = models.ImageField(upload_to='estudiantes/images/',blank=True, null=True, default='Doc_management\estudiantes\images\DSC_1379.JPG')
    

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
