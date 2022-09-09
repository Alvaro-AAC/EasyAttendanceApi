from django.urls import path

from .views import *

urlpatterns = [
    path('v1/lista_asistencia/<id>/', lista_asistencia),
    path('v1/registrar_asistencia/<token_clase>/<token_usuario>/', registrar_asistencia),
    path('v1/generar_codigo_clase/', codigo_asistencia),
    path('v1/generar_codigo_alumno/', codigo_usuario),
    path('v1/generar_codigo_login/', codigo_login),
    path('v1/registrarse/<token>/', register),
    path('v1/verified/<user>/', is_verificado),
    path('v1/isalumno/<nombre>/', is_alumno),
]
