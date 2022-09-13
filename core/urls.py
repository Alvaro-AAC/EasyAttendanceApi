from django.urls import path

from .views import *

urlpatterns = [
    path('', login),
    path('clases/', home),
    path('verifyLogin/', loginVerify),
    path('logout/', logout),
    path('crearclase/', crearclase),
    path('verificar/<token>/', verificar),
]
