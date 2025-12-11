from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Reserva, Mesa


@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    """Configuración del admin para el modelo Mesa"""
    list_display = ('numero', 'capacidad')
    list_filter = ('capacidad',)
    search_fields = ('numero',)
    ordering = ('numero',)


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    """Configuración del admin para el modelo Reserva"""
    list_display = (
        'id', 'nombre', 'telefono', 'fecha', 'hora',
        'numero_personas', 'estado', 'mesa', 'observacion'
    )
    list_filter = ('estado', 'fecha', 'mesa')
    search_fields = ('nombre', 'telefono', 'mesa__numero')
    ordering = ('fecha', 'hora')
    date_hierarchy = 'fecha'
    
    fieldsets = (
        (_('Información del Cliente'), {
            'fields': ('nombre', 'telefono')
        }),
        (_('Detalles de la Reserva'), {
            'fields': ('fecha', 'hora', 'numero_personas', 'mesa', 'estado')
        }),
        (_('Información Adicional'), {
            'fields': ('observacion',),
            'classes': ('collapse',)
        }),
    )


# Configurar el título del sitio admin en español
admin.site.site_header = _("Administración de Reservas")
admin.site.site_title = _("Sitio de Administración")
admin.site.index_title = _("Panel de Control")

