CONTROL DE ESTUDIANTES - Diego
Python 3.12 + Django 5.2 + MySQL 8.0

Cómo ejecutarlo:
1. Ejecutar base_datos.sql en MySQL (crea la base estudiante_db con datos de ejemplo).
2. En sistema/settings.py, poner la contraseña de MySQL en 'PASSWORD'.
3. En una terminal, dentro de la carpeta:
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
4. Abrir http://127.0.0.1:8000

El diagrama de la base de datos está en DIAGRAMA.png.