-- Script para crear la base de datos DJANGO_RESERVAS
-- Ejecutar desde MySQL command line: mysql -u root -p < crear_base_datos.sql
-- O copiar y pegar estos comandos en la línea de comandos de MySQL

CREATE DATABASE IF NOT EXISTS DJANGO_RESERVAS CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Verificar que la base de datos se creó correctamente
SHOW DATABASES LIKE 'DJANGO_RESERVAS';

-- Usar la base de datos
USE DJANGO_RESERVAS;


