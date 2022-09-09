from django.contrib import admin
import core.models

# Register your models here.

admin.site.register(core.models.Ramo)
admin.site.register(core.models.Modulo)
admin.site.register(core.models.Seccion)
admin.site.register(core.models.Horario_Seccion)
admin.site.register(core.models.Alumno)
admin.site.register(core.models.Alumno_Seccion)
admin.site.register(core.models.Profesor)
admin.site.register(core.models.Clase)
admin.site.register(core.models.Asistencia)
admin.site.register(core.models.CodigoQR)
admin.site.register(core.models.TokenAlumno)
admin.site.register(core.models.TokenLogin)