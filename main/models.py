from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Solicitud(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('ACEPTADA', 'Aceptada'),
        ('RECHAZADA', 'Rechazada'),
        ('EXPIRADA', 'Expirada'),
    ]

    # Relación con el usuario que realiza la solicitud
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    rut = models.CharField(max_length=12)  # RUT del solicitante
    nombre = models.CharField(max_length=100)  # Nombre del solicitante
    apellidos = models.CharField(max_length=100)  # Apellidos del solicitante
    direccion = models.CharField(max_length=255)  # Dirección del solicitante
    telefono = models.CharField(max_length=15)  # Teléfono del solicitante
    comuna = models.CharField(max_length=100)  # Comuna del solicitante
    fecha_solicitud = models.DateTimeField(default=timezone.now)  # Fecha de la solicitud
    fecha_aceptacion = models.DateTimeField(null=True, blank=True)  # Fecha de aceptación (puede estar vacía si está pendiente)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='PENDIENTE')  # Estado de la solicitud

    def __str__(self):
        return f"Solicitud de {self.nombre} {self.apellidos} - {self.estado}"

    def esta_expirada(self):
        if self.fecha_aceptacion:
            return timezone.now() > self.fecha_aceptacion + timezone.timedelta(days=30)
        return False

    def cambiar_estado(self):
        if self.estado == 'ACEPTADA' and not self.fecha_aceptacion:
            self.fecha_aceptacion = timezone.now()  # Establece la fecha de aceptación al momento de aceptación
        elif self.estado == 'ACEPTADA' and self.esta_expirada():
            self.estado = 'EXPIRADA'
            self.save()

    def save(self, *args, **kwargs):
        """Se asegura de que el estado se actualice automáticamente al guardar la solicitud."""
        self.cambiar_estado()
        super().save(*args, **kwargs)
