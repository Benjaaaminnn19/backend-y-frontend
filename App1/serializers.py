from rest_framework import serializers
from .models import Reserva, Mesa


class MesaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Mesa"""
    
    class Meta:
        model = Mesa
        fields = ['id', 'numero', 'capacidad']


class ReservaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Reserva"""
    mesa = MesaSerializer(read_only=True)
    mesa_id = serializers.PrimaryKeyRelatedField(
        queryset=Mesa.objects.all(),
        source='mesa',
        write_only=True
    )
    
    class Meta:
        model = Reserva
        fields = [
            'id', 'nombre', 'telefono', 'fecha', 'hora',
            'numero_personas', 'estado', 'mesa', 'mesa_id', 'observacion'
        ]
    
    def validate_numero_personas(self, value):
        """Validar que el número de personas esté entre 1 y 15"""
        if value < 1 or value > 15:
            raise serializers.ValidationError(
                "El número de personas debe estar entre 1 y 15."
            )
        return value
    
    def validate(self, data):
        """Validar que el número de personas no exceda la capacidad de la mesa"""
        mesa = data.get('mesa')
        numero_personas = data.get('numero_personas')
        
        if mesa and numero_personas:
            if numero_personas > mesa.capacidad:
                raise serializers.ValidationError(
                    f"El número de personas ({numero_personas}) excede la capacidad de la mesa ({mesa.capacidad})."
                )
        
        return data


