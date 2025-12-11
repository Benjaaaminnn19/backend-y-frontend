from django.urls import path
from . import views

app_name = 'App1'

urlpatterns = [
    path('', views.home, name='home'),
    path('api/reservas/', views.reserva_list_create, name='reserva-list-create'),
    path('api/reservas/<int:pk>/', views.reserva_detail, name='reserva-detail'),
    path('api/mesas/', views.mesa_list, name='mesa-list'),
]

