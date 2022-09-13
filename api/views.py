import datetime
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import *
from .serializers import *
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.hashers import check_password


# Create your views here.

@api_view(['GET',])
def lista_asistencia(request, id):
    if request.method == 'GET':
        clase = Clase.objects.get(pk = id)
        alumnos = Asistencia.objects.filter(clase_id = clase).all()
        serializer = AsistenciaSerializer(alumnos, many = True)
        if serializer.is_valid:
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'error', 'data': serializer.errors}, status=status.HTTP_200_OK)
    else:
        return Response({'status': 'error'}, status=status.HTTP_200_OK)

@api_view(['GET',])
def registrar_asistencia(request, token_clase, token_usuario):
    if request.method == 'GET':
        clase = CodigoQR.objects.get(url = token_clase).clase_id
        alumno = TokenAlumno.objects.get(token = token_usuario).alumno_id
        asist = Asistencia.objects.get(clase_id = clase, alumno_id = alumno)
        asist.presente = True
        asist.save()
        data = {
            'clase': str(clase),
            'alumno': str(alumno),
            'presente': 'Verdadero',
        }
        return Response({'status': 'success', 'data': data})
    else:
        return Response({'status': 'error'}, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['POST',])
def codigo_asistencia(request):
    if request.method == 'POST':
        id = request.POST['id'][0]
        code = CodigoQR(clase_id = Clase.objects.get(pk = id))
        code.save()
        data = {
            'token': code.url
        }
        return Response({'status': 'success', 'data': data}, status=status.HTTP_200_OK)
    else:
        return Response({'status': 'error'}, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['POST',])
def codigo_usuario(request):
    if request.method == 'POST':
        id = request.POST['id'][0]
        username = request.POST['username'][0]
        code = TokenAlumno(alumno_id = Alumno.objects.get(usuario = username, pk = id))
        code.save()
        data = {
            'token': code.token
        }
        return Response({'status': 'success', 'data': data}, status=status.HTTP_200_OK)
    else:
        return Response({'status': 'error'}, status=status.HTTP_200_OK)

@api_view(['POST',])
def codigo_login(request):
    if request.method == 'POST':
        try:
            authToken = request.POST['auth']
            if 'z_gHXCkfMAuv703l_F2J6' not in authToken:
                return Response({'status': 'unauthorized'} ,status=status.HTTP_200_OK)
        except KeyError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if 'username' in request.POST:
            username = request.POST['username']
            if Alumno.objects.filter(usuario = username).exists():
                return Response({'status': 'existe'}, status=status.HTTP_200_OK)
            else:
                for elem in username:
                    if not (elem.isalpha() or elem == '.'):
                        return Response({'status': 'errorvalidacion'}, status=status.HTTP_200_OK)
                    else:
                        if TokenLogin.objects.filter(usuario = username).exists():
                            ... #TokenLogin.objects.get(usuario = username).delete()
                        token = TokenLogin(usuario = username)
        else:
            return Response({'status': 'error'}, status=status.HTTP_200_OK)
        # token.save()
        subject = 'Registrarse en Easy Attendance'
        html_message = render_to_string('mail_template.html', {'token': token.token})
        plain_message = strip_tags(html_message)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [f'{username}@duocuc.cl']

        # send_mail(subject, plain_message, email_from, recipient_list, html_message=html_message )

        data = {
            'token': token.token
        }
        
        return Response({'status': 'success', 'data': data}, status=status.HTTP_200_OK)
    else:
        return Response({'status': 'error'}, status=status.HTTP_200_OK)

@api_view(['GET',])
def is_verificado(request, user):
    if request.method == 'GET':
        try:
            vToken = TokenLogin.objects.get(usuario = user)
            verificado = True if (vToken.verificado and vToken.fecha_exp.replace(tzinfo=None) > datetime.datetime.now()) else False
            data = {
                'verificado': verificado
            }
            return Response({'status': 'success', 'data': data}, status=status.HTTP_200_OK)
        except TokenLogin.DoesNotExist:
            return Response({'status': 'error'}, status=status.HTTP_200_OK)
    else:
        return Response({'status': 'error'}, status=status.HTTP_200_OK)

@api_view(['POST',])
def crear_alumno(request):
    if request.method == 'POST':
        Alumno(**{key: str(value) for key, value in request.POST.items()}).save()
        return Response({'status': 'success'}, status=status.HTTP_200_OK)
    else:
        return Response({'status': 'error'}, status=status.HTTP_200_OK)

@api_view(['GET',])
def is_alumno(request, nombre):
    if request.method == 'GET':
        isAlumn = Alumno.objects.filter(usuario = nombre).exists()
        data = {'existe': isAlumn}
        return Response({'status': 'success', 'data': data}, status=status.HTTP_200_OK)
    else:
        return Response({'status': 'error'}, status=status.HTTP_200_OK)

@api_view(['GET'],)
def clases(request, id):
    if request.method == 'GET':
        try:
            seccion = Seccion.objects.get(pk = id)
        except Seccion.DoesNotExist:
            return Response({'status': 'error'}, status=status.HTTP_200_OK)
        if Clase.objects.filter(seccion_id = seccion).exists():
            clases = Clase.objects.filter(seccion_id = seccion)
            serializer = ClaseSerializer(clases, many = True)
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'error'}, status=status.HTTP_200_OK)
    else:
        return Response({'status': 'error'}, status=status.HTTP_200_OK)

@api_view(['GET'],)
def secciones(request, id, prof):
    if request.method == 'GET':
        try:
            ramo = Ramo.objects.get(pk = id)
            profe = Profesor.objects.get(pk = prof)
        except (Ramo.DoesNotExist, Profesor.DoesNotexist):
            return Response({'status': 'error'}, status=status.HTTP_200_OK)
        if Seccion.objects.filter(ramo_id = ramo).exists():
            secciones = Seccion.objects.filter(ramo_id = ramo, profesor_id = prof)
            serializer = SeccionSerializer(secciones, many = True)
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'error'}, status=status.HTTP_200_OK)
    else:
        return Response({'status': 'error'}, status=status.HTTP_200_OK)

@api_view(['POST'],)
def delete_clase(request):
    if request.method == 'POST':
        if Clase.objects.filter(pk = str(request.POST['id'])).exists():
            clase = Clase.objects.get(pk = str(request.POST['id']))
            clase.delete()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'error'}, status=status.HTTP_200_OK)
    else:
        return Response({'status': 'error'}, status=status.HTTP_200_OK)

@api_view(['POST'],)
def login(request):
    if request.method == 'POST':
        try:
            pwd = request.POST['pwd']
            user = request.POST['user']
        except KeyError:
            return Response({'status': 'error'}, status=status.HTTP_200_OK)
        if Alumno.objects.filter(usuario = user).exists():
            alumno = Alumno.objects.get(usuario = user)
            valid = check_password(pwd, alumno.contrasena)
            if valid:
                return Response({'status': 'success'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'invalid'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'invalid'}, status=status.HTTP_200_OK)
    else:
        return Response({'status': 'error'}, status=status.HTTP_200_OK)