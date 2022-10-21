from django.urls import path

from .views import *

urlpatterns = [
    path('v1/lista_asistencia/<id>/', lista_asistencia),
    path('v1/registrar_asistencia/<token_clase>/<token_usuario>/', registrar_asistencia),
    path('v1/generar_codigo_clase/', codigo_asistencia),
    path('v1/generar_codigo_alumno/', codigo_usuario),
    path('v1/generar_codigo_login/', codigo_login),
    path('v1/verified/<user>/', is_verificado),
    path('v1/isalumno/<nombre>/', is_alumno),
    path('v1/clases/<id>/', clases),
    path('v1/secciones/<id>/<prof>/', secciones),
    path('v1/delclase/', delete_clase),
    path('v1/crearalumno/', crear_alumno),
    path('v1/login/', login),
    path('v1/horario/<token>/', horario),
    path('v1/asistencia/<token>/', calcularAsistencia),
    path('v1/asistenciatotal/<id>/', traerAsistencia)
]
