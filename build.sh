#!/usr/bin/env bash
set -o errexit

# --- 1. INSTALAR DEPENDENCIAS ---
pip install -r requirements.txt

# --- 3. MIGRACIONES DESDE CERO ---
python manage.py makemigrations
python manage.py migrate

# --- 4. COLECTAR ARCHIVOS ESTÁTICOS ---
python manage.py collectstatic --no-input

# --- 5. CREAR SUPERUSUARIO DESDE CERO ---
echo "from django.contrib.auth import get_user_model; \
User = get_user_model(); \
User.objects.filter(username='Dayana').exists() or \
User.objects.create_superuser('Dayana', 'Dayana@gmail.com', '123')" \
| python manage.py shell
