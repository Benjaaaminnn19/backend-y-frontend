"""
Script para crear el usuario administrador con las credenciales requeridas:
Usuario: admin
Contraseña: secret
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Eva4.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Crear o actualizar el usuario admin
username = 'admin'
password = 'secret'
email = 'admin@example.com'

if User.objects.filter(username=username).exists():
    user = User.objects.get(username=username)
    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print(f'Usuario "{username}" actualizado exitosamente.')
else:
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Usuario "{username}" creado exitosamente.')

print(f'Credenciales:')
print(f'  Usuario: {username}')
print(f'  Contraseña: {password}')


