import datetime
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.hashers import make_password, identify_hasher

# Create your models here.

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
        return f'{str(self.hora_ini) - str(self.hora_fin)}'

class Seccion(models.Model):
    codigo_seccion = models.IntegerField()
    tipo = models.CharField(max_length=1, null=False)
    ramo_id = models.ForeignKey(Ramo, null=False, on_delete=models.CASCADE)

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

class Alumno_Seccion(models.Model):
    seccion_id = models.ForeignKey(Seccion, on_delete=models.CASCADE)
    alumno_id = models.ForeignKey(Alumno, on_delete=models.CASCADE)

    def __str__(self):
        return f'{str(self.seccion_id)} - {str(self.alumno_id)}'

class Profesor(models.Model):
    profesor_id = models.BigAutoField(primary_key=True)
    usuario = models.CharField(max_length=100, null=False, unique=True)
    contrasena = models.CharField(max_length=2000, null=False)
    nombre = models.CharField(max_length=50, null=False)
    apellido = models.CharField(max_length=50, null=False)

    def save(self, *args, **kwargs):
        try:
            identify_hasher(self.contrasena)
        except ValueError:
            self.contrasena = make_password(self.contrasena)
        super(Profesor, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

class Clase(models.Model):
    clase_id = models.BigAutoField(primary_key=True)
    fecha = models.DateField(null=False)
    profesor_id = models.ForeignKey(Profesor, on_delete=models.CASCADE)
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
    url = models.CharField(max_length=1000)
    fecha_exp = models.DateField(null=True)
    clase_id = models.ForeignKey(Clase, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.fecha_exp = datetime.datetime.now() + datetime.timedelta(minutes=30)
        super(CodigoQR, self).save(*args, **kwargs)

    def __str__(self):
        return f'{str(self.clase_id)} - {self.fecha_exp.day}/{self.fecha_exp.month} {self.fecha_exp.time}'