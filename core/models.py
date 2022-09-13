import datetime
from django.db.utils import IntegrityError
from django.db import models, transaction
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.hashers import make_password, identify_hasher
import secrets

# Create your models here.

def tokenize():
    return secrets.token_urlsafe(100)

def exp_date():
    return datetime.datetime.now() + datetime.timedelta(minutes=20)

class Ramo(models.Model):
    codigo_letra = models.CharField(max_length=3, null=False)
    codigo_numero = models.IntegerField(null=False)
    descripcion = models.CharField(max_length=100, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['codigo_letra', 'codigo_numero'], name='constraint_ramo_codigo'
            ),
        ]

    def __str__(self):
        return f'{self.codigo_letra}{self.codigo_numero}'

class Modulo(models.Model):
    modulo_id = models.BigAutoField(primary_key=True)
    hora_ini = models.TimeField(null=False)
    hora_fin = models.TimeField(null=False)

    def __str__(self):
        return f'{str(self.hora_ini)} - {str(self.hora_fin)}'

class Profesor(models.Model):
    profesor_id = models.BigAutoField(primary_key=True)
    usuario = models.CharField(max_length=100, null=False, unique=True)
    contrasena = models.CharField(max_length=2000, null=False)
    nombre = models.CharField(max_length=50, null=False)
    apellido = models.CharField(max_length=50, null=False)

    class Meta:
        verbose_name_plural = 'Profesores'

    def save(self, *args, **kwargs):
        try:
            identify_hasher(self.contrasena)
        except ValueError:
            self.contrasena = make_password(self.contrasena)
        super(Profesor, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

class Seccion(models.Model):
    codigo_seccion = models.IntegerField()
    tipo = models.CharField(max_length=1, null=False, choices=[('D', 'Diurno'), ('V', 'Vespertino')])
    ramo_id = models.ForeignKey(Ramo, null=False, on_delete=models.CASCADE)
    profesor_id = models.ForeignKey(Profesor, null=False, blank= False, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check = models.Q(tipo__in=('D', 'V')),
                name = 'constraint_seccion_check_tipo'
            ),
            models.UniqueConstraint(
                fields = ['codigo_seccion', 'ramo_id', 'tipo'],
                name = 'constraint_seccion_codigo'
            )
        ]
        verbose_name_plural = 'Secciones'

    def __str__(self):
        return f'{str(self.ramo_id)}-{self.codigo_seccion}{self.tipo}'


class Horario_Seccion(models.Model):

    DIAS_SEMANA = [
        ('LUN', 'Lunes'),
        ('MAR', 'Martes'),
        ('MIE', 'Miercoles'),
        ('JUE', 'Jueves'),
        ('VIE', 'Viernes'),
        ('SAB', 'Sabado'),
        ('DOM', 'Domingo'),
    ]

    modulo_id = models.ForeignKey(Modulo, null=False, on_delete=models.CASCADE)
    seccion_id = models.ForeignKey(Seccion, null=False, on_delete=models.CASCADE)
    dia = models.CharField(max_length=3, choices=DIAS_SEMANA, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['modulo_id', 'seccion_id', 'dia'],
                name = 'horario_seccion_constraint_uk'
            )
        ]
        verbose_name_plural = 'Horario Secciones'
        verbose_name = 'horario sección'

    def __str__(self):
        return f'{str(self.seccion_id)} | {self.dia} | {str(self.modulo_id)}'

class Alumno(models.Model):
    alumno_id = models.BigAutoField(primary_key=True)
    usuario = models.CharField(max_length=100, null=False, unique=True)
    contrasena = models.CharField(max_length=2000, null=False)
    nombre = models.CharField(max_length=50, null=False)
    apellido = models.CharField(max_length=50, null=False)

    def save(self, *args, **kwargs):
        try:
            identify_hasher(self.contrasena)
        except ValueError:
            self.contrasena = make_password(self.contrasena)
        super(Alumno, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        del self

class Alumno_Seccion(models.Model):
    seccion_id = models.ForeignKey(Seccion, on_delete=models.CASCADE)
    alumno_id = models.ForeignKey(Alumno, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Alumnos de sección'
        verbose_name = 'alumno de sección'

    def __str__(self):
        return f'{str(self.seccion_id)} - {str(self.alumno_id)}'

class Clase(models.Model):
    clase_id = models.BigAutoField(primary_key=True)
    fecha = models.DateField(null=False)
    seccion_id = models.ForeignKey(Seccion, on_delete=models.CASCADE)

    def __str__(self):
        return f'{str(self.seccion_id)} - {self.fecha}'

class Asistencia(models.Model):
    clase_id = models.ForeignKey(Clase, on_delete=models.CASCADE)
    alumno_id = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    presente = models.BooleanField(null=False, default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['clase_id', 'alumno_id'],
                name = 'constraint_asistencia_pk'
            )
        ]

    def __str__(self):
        return f'{str(self.clase_id)} - {str(self.alumno_id)} | presente: {self.presente}'

class CodigoQR(models.Model):
    codigoqr_id = models.BigAutoField(primary_key=True)
    url = models.CharField(max_length=1000, unique=True, default=tokenize)
    fecha_exp = models.DateTimeField(default = exp_date)
    clase_id = models.ForeignKey(Clase, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Codigos QR'

    def __str__(self):
        return f'{str(self.clase_id)} - {self.fecha_exp.day}/{self.fecha_exp.month} {self.fecha_exp.time().strftime("%H:%M:%S")}'

class TokenAlumno(models.Model):
    tokenAlumno_id = models.BigAutoField(primary_key=True)
    token = models.CharField(max_length=1000, unique=True, null=True, blank=True, default=tokenize)
    fecha_exp = models.DateTimeField(default = exp_date)
    alumno_id = models.ForeignKey(Alumno, on_delete=models.CASCADE)


class TokenLogin(models.Model):
    tokenLogin_id = models.BigAutoField(primary_key=True)
    usuario = models.CharField(max_length=100, unique=True)
    token = models.CharField(max_length=1000, unique=True, null=True, blank=True, default=tokenize)
    fecha_exp = models.DateTimeField(default = exp_date)
    verificado = models.BooleanField(default=False)

def post_save_clase(sender, instance, created, **kwargs):
    if created:
        alumnos = Alumno_Seccion.objects.filter(seccion_id = instance.seccion_id).all()
        for elem in alumnos:
            with Alumno.objects.get(pk = elem.alumno_id.pk) as alumno:
                tempAlumno = Asistencia(clase_id = instance, alumno_id = alumno, presente = False)
                try:
                    with transaction.atomic():
                        tempAlumno.save()
                except IntegrityError:
                    ...

post_save.connect(post_save_clase, sender = Clase)