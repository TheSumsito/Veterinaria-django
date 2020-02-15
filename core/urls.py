from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    #! VISTAS PRINCIPALES 
    path('', home, name='home'),
    path('nosotros/', nosotros, name="nosotros"),
    path('servicios/', servicios , name="servicios"),
    path('planes/', planes, name="planes"),
    path('contacto/', contacto, name="contacto"),
    path('login/', login, name="login"),
    path('registro/', RegistroUsuario, name="RegistroUsuario"),
    path('cerrar/', cerrar, name="cerrar"),
    path('Administrador/', homeAdmin, name="homeAdmin"),
    path('Usuario/', homeUser, name="homeUser"),


    #! VISTAS USUARIO
    path('agendar-cita/', AgendarCita, name="AgendarCita"),
    path('ver-citas/', VerCitas, name="VerCitas"),
    path('anular-cita', AnularCita, name="AnularCita"),
    path('ficha-paciente/', FichaPaciente, name="FichaPaciente"),

    #! VISTAS ADMINISTRADOR
    path('reg-mascota/', regMascota, name="regMascota"),
    path('aprobar-cita/', AprobarCita, name="AprobarCita"),
]
