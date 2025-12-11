from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Reserva, Mesa
from .serializers import ReservaSerializer, MesaSerializer


def home(request):
    api_info = {
        'mensaje': 'API de Reservas de Restaurante',
        'endpoints_disponibles': {
            'admin': '/admin/ - Panel de administración de Django',
            'listar_reservas': {
                'url': '/api/reservas/',
                'metodo': 'GET',
                'descripcion': 'Lista todas las reservas ordenadas por fecha'
            },
            'crear_reserva': {
                'url': '/api/reservas/',
                'metodo': 'POST',
                'descripcion': 'Crea una nueva reserva',
                'campos_requeridos': {
                    'nombre': 'string (obligatorio)',
                    'telefono': 'string (obligatorio)',
                    'fecha': 'YYYY-MM-DD (obligatorio)',
                    'hora': 'HH:MM:SS (obligatorio)',
                    'numero_personas': 'integer 1-15 (obligatorio)',
                    'estado': 'RESERVADO|COMPLETADA|ANULADA|NO_ASISTEN (opcional, default: RESERVADO)',
                    'mesa_id': 'integer (obligatorio)',
                    'observacion': 'string (opcional)'
                }
            },
            'obtener_reserva': {
                'url': '/api/reservas/<id>/',
                'metodo': 'GET',
                'descripcion': 'Obtiene una reserva específica por su ID'
            },
            'actualizar_reserva': {
                'url': '/api/reservas/<id>/',
                'metodo': 'PUT o PATCH',
                'descripcion': 'Actualiza una reserva existente'
            },
            'eliminar_reserva': {
                'url': '/api/reservas/<id>/',
                'metodo': 'DELETE',
                'descripcion': 'Elimina una reserva'
            }
        }
    }
    return JsonResponse(api_info, json_dumps_params={'ensure_ascii': False, 'indent': 2})


@api_view(['GET', 'POST'])
def reserva_list_create(request):
    if request.method == 'GET':
        reservas = Reserva.objects.all().order_by('fecha', 'hora')
        serializer = ReservaSerializer(reservas, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ReservaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def reserva_detail(request, pk):
    try:
        reserva = Reserva.objects.get(pk=pk)
    except Reserva.DoesNotExist:
        return Response(
            {'error': 'Reserva no encontrada'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        serializer = ReservaSerializer(reserva)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ReservaSerializer(reserva, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PATCH':
        serializer = ReservaSerializer(reserva, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        reserva.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def mesa_list(request):
    mesas = Mesa.objects.all().order_by('numero')
    serializer = MesaSerializer(mesas, many=True)
    return Response(serializer.data)