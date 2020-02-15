from django.shortcuts import render
from .models import *

#! IMPORTACION PARA TRABAJAR CON USUARIO
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate


#! FUNCION PARA REDIRECCIONAR LOGOUT
from django.http import HttpResponse, HttpResponseRedirect

#! NUMERO RANDOM
from random import randint

from datetime import date, time, datetime

# Create your views here.

#! VISTAS PRINCIPALES


def home(request):
    return render(request, '../templates/index.htm')


def nosotros(request):
    return render(request, '../templates/nosotros.htm')


def servicios(request):
    return render(request, '../templates/servicios.htm')


def planes(request):
    return render(request, '../templates/planes.htm')


def contacto(request):
    if request.POST:
        correo = request.POST.get("txtCorreo", "")
        nombre = request.POST.get("txtNombre", "")
        apellido = request.POST.get("txtApellido", "")
        telefono = request.POST.get("txtTelefono", "")
        asunto = request.POST.get("txtAsunto", "")
        mensaje = request.POST.get("txtMensaje", "")

        con = Contacto(
            Correo=correo,
            Nombre=nombre,
            Apellido=apellido,
            Telefono=telefono,
            Asunto=asunto,
            Mensaje=mensaje
        )
        con.save()
        resp = True
        return render(request, '../templates/contacto.htm', {'resp': True})
    else:
        return render(request, '../templates/contacto.htm', {'resp': False})


def RegistroUsuario(request):
    pro = Provincia.objects.all()
    com = Comuna.objects.all()

    if request.POST:
        rutpersona = request.POST.get("txtRut", "")
        nombre = request.POST.get("txtNombre", "")
        apellido = request.POST.get("txtApellido", "")
        correo = request.POST.get("txtCorreo", "")
        direccion = request.POST.get("txtDireccion", "")
        telefono = request.POST.get("txtTelefono", "")
        comuna = request.POST.get("cboComuna", "")
        provincia = request.POST.get("cboProvincia", "")

        #! USUARIO - CONTRASEÑA
        correo_usu = request.POST.get("txtCorreo", "")
        contrasena = request.POST.get("txtContrasena", "")

        #! INSTANCES
        comu_id = Comuna.objects.get(IdComuna=comuna)
        provi_id = Provincia.objects.get(IdProvincia=provincia)

        per = Persona(
            RutPersona=rutpersona,
            Nombre=nombre,
            Apellido=apellido,
            Correo=correo,
            Direccion=direccion,
            Telefono=telefono,
            IdComuna=comu_id
        )

        usu = User.objects.create_user(
            first_name=nombre,
            last_name=apellido,
            email=correo_usu,
            username=correo_usu,
            password=contrasena,
            is_staff=False
        )
        per.save()
        usu.save()
        return render(request, '../templates/registro.htm', {'comuna': com, 'provincia': pro})
    else:
        return render(request, '../templates/registro.htm', {'comuna': com, 'provincia': pro})


def login(request):
    if request.POST:
        rutpersona = request.POST.get("txtRut", "")
        contrasena = request.POST.get("txtPass", "")

        user = auth.authenticate(username=rutpersona, password=contrasena)

        if user is not None and User.is_active:
            auth.login(request, user)
            resp = request.user.is_staff
            if resp == True:
                return HttpResponseRedirect('../Administrador')
            else:
                return HttpResponseRedirect('../Usuario')
        else:
            return render(request, '../templates/login.htm')
    return render(request, '../templates/login.htm')


@login_required(login_url='/')
def cerrar(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url='/')
def homeUser(request):
    user = auth.authenticate()
    correo = request.user.username
    persona = Persona.objects.get(Correo=correo)
    rutpersona = persona.RutPersona
    mascotas = Mascota.objects.filter(RutPersona=rutpersona)
    return render(request, '../templates/usuario/index.htm', {'per': persona, 'mascotas': mascotas})

#! ARREGLAR ESTA VIEWS
@login_required(login_url='/')
def AgendarCita(request):
    user = auth.authenticate()
    correo = request.user.username
    persona = Persona.objects.get(Correo=correo)
    
    rutpersona = persona.RutPersona
    mascotas = Mascota.objects.filter(RutPersona=rutpersona)

    random = randint(0, 99999)

    tipo = TipoConsulta.objects.all()

    if request.POST:
        nombreMascota = request.POST.get("cboMascota", "")
        tipoConsulta = request.POST.get("cboTipo", "")
        fecha = request.POST.get("txtFecha", "")

        #!INSTANCES
        tipo_id = TipoConsulta.objects.get(IdTipo=tipoConsulta)
        mascota_id = Mascota.objects.get(IdMascota=nombreMascota)

        cita = Cita(
            IdCita=random,
            Descripcion="N/A",
            Fecha=fecha,
            Hora=time.max,
            IdMascota=mascota_id,
            IdTipo=tipo_id,
            Estado=False
        )
        cita.save()
        return render(request, '../templates/usuario/agendar-cita.htm', {'per': persona, 'name': nombreMascota, 'tipoConsulta': tipo_id, 'fecha': fecha})
    else:
        return render(request, '../templates/usuario/agendar-cita.htm', {'per': persona, 'mascotas': mascotas, 'tipo': tipo})
    return render(request, '../templates/usuario/agendar-cita.htm', {'per': persona, 'mascotas': mascotas, 'tipo': tipo})


@login_required(login_url='/')
def VerCitas(request):
    user = auth.authenticate()
    correo = request.user.username
    persona = Persona.objects.get(Correo=correo)

    rutpersona = persona.RutPersona
    mascotas = Mascota.objects.filter(RutPersona=rutpersona)

    if request.POST:
        accion = request.POST.get("btnAccion", "")
        if accion == "Buscar":
            nombre_id = request.POST.get("cboNombre", "")
            citas = Cita.objects.filter(IdMascota=nombre_id)
            name = Mascota.objects.get(IdMascota=nombre_id)
            return render(request, '../templates/usuario/ver-citas.htm', {'per': persona, 'mascota': mascotas, 'citas': citas, 'name': name})
        else:
            return render(request, '../templates/usuario/ver-citas.htm')
    return render(request, '../templates/usuario/ver-citas.htm', {'per': persona, 'mascota': mascotas})


@login_required(login_url='/')
def AnularCita(request):
    user = auth.authenticate()
    correo = request.user.username
    persona = Persona.objects.get(Correo=correo)

    rutpersona = persona.RutPersona
    mascotas = Mascota.objects.filter(RutPersona=rutpersona)

    if request.POST:
        accion = request.POST.get("btnAccion", "")
        if accion == "Buscar":
            nombre_id = request.POST.get("cboNombre", "")
            citas = Cita.objects.filter(IdMascota=nombre_id)
            name = Mascota.objects.get(IdMascota=nombre_id)
            return render(request, '../templates/usuario/anular-cita.htm', {'per': persona, 'mascotas': mascotas, 'citas': citas, 'name': name})
        elif accion == "Anular":
            identificador = request.POST.get("txtIdentificador")
            cita_id = Cita.objects.filter(IdCita=identificador)
            cita_id.delete()
            return render(request, '../Templates/usuario/anular-cita.htm', {'per': persona, 'mascotas': mascotas, 'citas': cita_id})

        else:
            return render(request, '../templates/usuario/anular-cita.htm', {'per': persona, 'mascotas': mascotas, 'citas': cita})
    return render(request, '../templates/usuario/anular-cita.htm', {'per': persona, 'mascotas': mascotas})


@login_required(login_url='/')
def FichaPaciente(request):
    user = auth.authenticate()
    correo = request.user.username
    persona = Persona.objects.get(Correo=correo)

    rutpersona = persona.RutPersona
    mascotas = Mascota.objects.filter(RutPersona=rutpersona)

    if request.POST:
        accion = request.POST.get("btnAccion", "")
        if accion == "Buscar":
            nombre_id = request.POST.get("cboNombre", "")
            desparacitacion = FichaDesparacitacion.objects.filter(
                IdMascota=nombre_id)
            vacunas = FichaVacunacion.objects.filter(IdMascota=nombre_id)
            name = Mascota.objects.get(IdMascota=nombre_id)
            mascota = Mascota.objects.filter(IdMascota=nombre_id)
            return render(request, '../templates/usuario/ficha-paciente.htm', {'per': persona, 'mascotas': mascotas, 'masc': mascota, 'vacunas': vacunas, 'desparacitacion': desparacitacion, 'name': name})
    return render(request, '../templates/usuario/ficha-paciente.htm', {'per': persona, 'mascotas': mascotas})


#! ADMINISTRADOR
@login_required(login_url=('/'))
def homeAdmin(request):
    contactos = Contacto.objects.all()
    user = auth.authenticate()
    username = request.user.username
    last_name = request.user.last_name

    return render(request, '../templates/administrador/index.htm', {'username': username, 'contactos': contactos})


def AdminMascota(request):
    mascotas = Mascota.objects.all()
    return render(request, '../templates/administrador/admin-mascota.htm', {'mascotas':mascotas})

def AprobarCita(request):
    user = auth.authenticate()
    username = request.user.username
    citas = Cita.objects.all()
    return render(request, '../templates/administrador/aprobar-cita.htm', {'username': username, 'citas':citas})