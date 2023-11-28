#!/bin/bash

# Esperar que PostgreSQL esté listo
while ! pg_isready -h postgres -p 5432; do
  sleep 1
done

# Ejecutar el script Python en loop
while true 
do
  python3 /visualizar_estaciones.py
  sleep 60
done