import re
from django.contrib import messages
from django.db import transaction
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Email, Phone, Address
from django.db.models import Q


def lista(request):
    q = request.GET.get('q', '').strip()
    estudiantes = Student.objects.all()
    if q:
        estudiantes = estudiantes.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(middle_name__icontains=q) |
            Q(emails__email__icontains=q)
        ).distinct()
    estudiantes = estudiantes.order_by('last_name')
    return render(request, 'alumnos/lista.html', {'estudiantes': estudiantes, 'q': q})


def alta(request):
    errores = []
    datos = request.POST if request.method == 'POST' else {}

    if request.method == 'POST':
        # Leer y limpiar los datos del formulario
        first_name = datos.get('first_name', '').strip()
        last_name = datos.get('last_name', '').strip()
        middle_name = datos.get('middle_name', '').strip()
        gender = datos.get('gender', '')
        email = datos.get('email', '').strip().lower()
        email_type = datos.get('email_type', '')
        country_code = datos.get('country_code', '').strip()
        area_code = datos.get('area_code', '').strip()
        phone = datos.get('phone', '').strip()
        phone_type = datos.get('phone_type', '')
        address_line = datos.get('address_line', '').strip()
        city = datos.get('city', '').strip()
        state = datos.get('state', '').strip()
        zip_postcode = datos.get('zip_postcode', '').strip()

        # Validaciones
        if not first_name or not last_name:
            errores.append('El nombre y el apellido paterno son obligatorios.')
        if gender not in dict(Student.GENDER):
            errores.append('Selecciona un género válido.')
        if not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email):
            errores.append('El correo no tiene un formato válido.')
        elif Email.objects.filter(email=email).exists():
            errores.append('Ese correo ya está registrado.')
        if not (phone.isdigit() and country_code.isdigit() and area_code.isdigit()):
            errores.append('El teléfono, la lada y el código de país solo deben tener números.')
        if not address_line or not city or not state or not zip_postcode:
            errores.append('Todos los campos de la dirección son obligatorios.')

        # Guardar todo junto: si algo falla, no se guarda nada
        if not errores:
            with transaction.atomic():
                estudiante = Student.objects.create(
                    first_name=first_name, last_name=last_name,
                    middle_name=middle_name, gender=gender)
                Email.objects.create(student=estudiante, email=email,
                                     email_type=email_type)
                Phone.objects.create(student=estudiante, phone=phone,
                                     phone_type=phone_type,
                                     country_code=country_code,
                                     area_code=area_code)
                Address.objects.create(student=estudiante,
                                       address_line=address_line, city=city,
                                       state=state, zip_postcode=zip_postcode)
            return redirect('lista')

    return render(request, 'alumnos/alta.html', {
        'errores': errores,
        'datos': datos,
        'generos': Student.GENDER,
        'tipos_email': Email.TYPES,
        'tipos_tel': Phone.TYPES,
    })


def detalle(request, student_id):
    estudiante = get_object_or_404(Student, student_id=student_id)
    return render(request, 'alumnos/detalle.html', {'e': estudiante})


def editar(request, student_id):
    e = get_object_or_404(Student, student_id=student_id)
    errores = []

    if request.method == 'POST':
        datos = request.POST
        first_name = datos.get('first_name', '').strip()
        last_name = datos.get('last_name', '').strip()
        middle_name = datos.get('middle_name', '').strip()
        gender = datos.get('gender', '')

        if not first_name or not last_name:
            errores.append('El nombre y el apellido paterno son obligatorios.')
        if gender not in dict(Student.GENDER):
            errores.append('Selecciona un género válido.')

        if not errores:
            e.first_name = first_name
            e.last_name = last_name
            e.middle_name = middle_name
            e.gender = gender
            e.save()
            return redirect('detalle', student_id=e.student_id)
    else:
        datos = {
            'first_name': e.first_name,
            'last_name': e.last_name,
            'middle_name': e.middle_name,
            'gender': e.gender,
        }

    return render(request, 'alumnos/editar.html', {
        'e': e, 'datos': datos, 'errores': errores, 'generos': Student.GENDER,
    })


def eliminar(request, student_id):
    e = get_object_or_404(Student, student_id=student_id)
    if request.method == 'POST':
        nombre = f'{e.first_name} {e.last_name}'
        e.delete()  # CASCADE borra también sus correos, teléfonos y direcciones
        messages.success(request, f'Se eliminó a {nombre} y toda su información.')
    return redirect('lista')


def eliminar_dato(request, tipo, pk):
    modelos = {'email': Email, 'phone': Phone, 'address': Address}
    Modelo = modelos.get(tipo)
    if Modelo is None:
        raise Http404

    obj = get_object_or_404(Modelo, pk=pk)
    student_id = obj.student_id

    if request.method == 'POST':
        # El diagrama indica 1..*: debe quedar al menos un correo y un teléfono
        restantes = Modelo.objects.filter(student_id=student_id).count()
        if tipo in ('email', 'phone') and restantes == 1:
            messages.error(request, 'El estudiante debe tener al menos un correo y un teléfono.')
        else:
            obj.delete()
            messages.success(request, 'Dato eliminado correctamente.')

    return redirect('detalle', student_id=student_id)

TIPOS = {
    'email': {'modelo': Email, 'nombre': 'correo',
              'campos': ['email', 'email_type']},
    'phone': {'modelo': Phone, 'nombre': 'teléfono',
              'campos': ['country_code', 'area_code', 'phone', 'phone_type']},
    'address': {'modelo': Address, 'nombre': 'dirección',
                'campos': ['address_line', 'city', 'state', 'zip_postcode']},
}


def validar_dato(tipo, datos, pk_actual=None):
    errores = []
    if tipo == 'email':
        if not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', datos['email']):
            errores.append('El correo no tiene un formato válido.')
        elif datos['email'] != pk_actual and Email.objects.filter(email=datos['email']).exists():
            errores.append('Ese correo ya está registrado.')
        if datos['email_type'] not in dict(Email.TYPES):
            errores.append('Selecciona un tipo de correo válido.')
    elif tipo == 'phone':
        if not (datos['phone'].isdigit() and datos['area_code'].isdigit()
                and datos['country_code'].isdigit()):
            errores.append('El teléfono, la lada y el código de país solo deben tener números.')
        if datos['phone_type'] not in dict(Phone.TYPES):
            errores.append('Selecciona un tipo de teléfono válido.')
    else:
        if not all(datos.values()):
            errores.append('Todos los campos de la dirección son obligatorios.')
    return errores


def dato(request, student_id, tipo, pk=None):
    conf = TIPOS.get(tipo)
    if conf is None:
        raise Http404
    estudiante = get_object_or_404(Student, student_id=student_id)
    Modelo = conf['modelo']
    obj = get_object_or_404(Modelo, pk=pk, student=estudiante) if pk else None
    errores = []

    if request.method == 'POST':
        datos = {c: request.POST.get(c, '').strip() for c in conf['campos']}
        if tipo == 'email':
            datos['email'] = datos['email'].lower()
        errores = validar_dato(tipo, datos, obj.pk if obj else None)

        if not errores:
            with transaction.atomic():
                # En email, el correo ES la llave primaria: si cambia, se reemplaza el registro
                if tipo == 'email' and obj and obj.email != datos['email']:
                    obj.delete()
                    obj = None
                if obj is None:
                    Modelo.objects.create(student=estudiante, **datos)
                else:
                    for campo, valor in datos.items():
                        setattr(obj, campo, valor)
                    obj.save()
            messages.success(request, 'Cambios guardados correctamente.')
            return redirect('detalle', student_id=student_id)
    else:
        datos = {c: getattr(obj, c) for c in conf['campos']} if obj else {}

    return render(request, 'alumnos/dato.html', {
        'e': estudiante, 'tipo': tipo, 'nombre': conf['nombre'],
        'editando': obj is not None, 'datos': datos, 'errores': errores,
        'tipos_email': Email.TYPES, 'tipos_tel': Phone.TYPES,
    })