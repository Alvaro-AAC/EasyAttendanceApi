from rest_framework import serializers
from core.models import *

class RamoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ramo
        fields = '__all__'

class SeccionSerializer(serializers.ModelSerializer):

    ramo_id = RamoSerializer(read_only = True)

    class Meta:
        model = Seccion
        fields = ['pk', 'codigo_seccion', 'tipo', 'ramo_id']

class AlumnoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Alumno
        fields = ['alumno_id', 'usuario', 'nombre', 'apellido']

class AlumnoSeccionSerializer(serializers.ModelSerializer):

    seccion_id = SeccionSerializer(read_only = True)
    alumno_id = AlumnoSerializer(read_only = True)

    class Meta:
        model = Alumno_Seccion
        fields = ['seccion_id', 'alumno_id']

class ProfesorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profesor
        fields = ['profesor_id', 'usuario', 'nombre', 'apellido']

class ClaseSerializer(serializers.ModelSerializer):

    profesor_id = ProfesorSerializer(read_only = True)
    seccion_id = SeccionSerializer(read_only = True)

    class Meta:
        model = Clase
        fields = ['clase_id', 'fecha', 'profesor_id', 'seccion_id']

    def to_representation(self, instance):
        representation = super(ClaseSerializer, self).to_representation(instance)
        representation['fecha'] = instance.fecha.strftime('%d/%m/%Y')
        return representation

class AsistenciaSerializer(serializers.ModelSerializer):

    clase_id = ClaseSerializer(read_only = True)
    alumno_id = AlumnoSerializer(read_only = True)

    class Meta:
        model = Asistencia
        fields = ['clase_id', 'alumno_id', 'presente']

class CodigoQrSerializer(serializers.ModelSerializer):

    clase_id = ClaseSerializer(read_only = True)

    class Meta:
        model = CodigoQR
        fields = ['codigoqr_id', 'url', 'fecha_exp', 'clase_id']

class ModuloSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Modulo
        fields = '__all__'

class HorarioSeccionSerializer(serializers.ModelSerializer):

    modulo_id = ModuloSerializer(read_only = True)
    seccion_id = SeccionSerializer(read_only = True)

    class Meta:
        model = Horario_Seccion
        fields = ['dia', 'modulo_id', 'seccion_id']