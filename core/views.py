from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.

def home(request):
    ctx = {}
    
    ctx['prof'] = Profesor.objects.filter(usuario = 'v.pobletel').get()
    ctx['clases'] = Clase.objects.filter(profesor_id = ctx['prof']).all()

    return render(request, 'core/home.html', ctx)
def login(request):
    return render(request, 'core/login.html')