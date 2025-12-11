from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class Mesa(models.Model):
    numero = models.IntegerField(unique=True, verbose_name=_("Número de Mesa"))
    capacidad = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(15)],
        verbose_name=_("Capacidad")
    )
    
    class Meta:
        verbose_name = _("Mesa")
        verbose_name_plural = _("Mesas")
        ordering = ['numero']
    
    def __str__(self):
        return f"Mesa {self.numero} (Capacidad: {self.capacidad})"


class Reserva(models.Model):
    class EstadoReserva(models.TextChoices):
        RESERVADO = 'RESERVADO', _('Reservado')
        COMPLETADA = 'COMPLETADA', _('Completada')
        ANULADA = 'ANULADA', _('Anulada')
        NO_ASISTEN = 'NO_ASISTEN', _('No Asisten')
    
    nombre = models.CharField(max_length=100, verbose_name=_("Nombre"))
    telefono = models.CharField(max_length=20, verbose_name=_("Teléfono"))
    fecha = models.DateField(verbose_name=_("Fecha de Reserva"))
    hora = models.TimeField(verbose_name=_("Hora de Reserva"))
    numero_personas = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(15)],
        verbose_name=_("Número de Personas")
    )
    estado = models.CharField(
        max_length=20,
        choices=EstadoReserva.choices,
        default=EstadoReserva.RESERVADO,
        verbose_name=_("Estado")
    )
    mesa = models.ForeignKey(
        Mesa,
        on_delete=models.CASCADE,
        related_name='reservas',
        verbose_name=_("Mesa Asignada")
    )
    observacion = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Observación")
    )
    
    class Meta:
        verbose_name = _("Reserva")
        verbose_name_plural = _("Reservas")
        ordering = ['fecha', 'hora']
    
    def __str__(self):
        return f"Reserva de {self.nombre} - {self.fecha} {self.hora}"
