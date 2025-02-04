from django.db import models

# Create your models here.

class ErrorLog(models.Model):
    codigo = models.CharField(max_length=10)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.codigo} - {self.mensaje}"