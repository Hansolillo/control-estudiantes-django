from django.db import models

# Las tablas se crean con base_datos.sql, fiel al diagrama.
# managed = False: Django las usa, pero no las crea ni las modifica.


class Student(models.Model):
    GENDER = [('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')]

    student_id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=45)
    middle_name = models.CharField(max_length=45, blank=True)
    first_name = models.CharField(max_length=45)
    gender = models.CharField(max_length=1, choices=GENDER)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        managed = False
        db_table = 'student'


class Email(models.Model):
    TYPES = [('personal', 'Personal'), ('trabajo', 'Trabajo')]

    # En la BD la llave es (email, student_id); en Django se identifica por el correo
    email = models.CharField(max_length=100, primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE,
                                db_column='student_id', related_name='emails')
    email_type = models.CharField(max_length=10, choices=TYPES)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        managed = False
        db_table = 'email'


class Phone(models.Model):
    TYPES = [('celular', 'Celular'), ('casa', 'Casa'), ('trabajo', 'Trabajo')]

    phone_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE,
                                db_column='student_id', related_name='phones')
    phone = models.CharField(max_length=30)
    phone_type = models.CharField(max_length=10, choices=TYPES)
    country_code = models.CharField(max_length=5, null=True, blank=True)
    area_code = models.CharField(max_length=5, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        managed = False
        db_table = 'phone'


class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE,
                                db_column='student_id', related_name='addresses')
    address_line = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=45, null=True, blank=True)
    zip_postcode = models.CharField(max_length=45, null=True, blank=True)
    state = models.CharField(max_length=45, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'address'