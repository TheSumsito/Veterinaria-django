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
            return render(request, '../templates/usuario/anular-cita.htm', {'per': persona, 'mascotas': mascotas, 'citas': cita_id})
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
            desparacitacion = FichaDesparacitacion.objects.filter(IdMascota=nombre_id)
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


def regMascota(request):
    user = auth.authenticate()
    username = request.user.username
    tamanos = Tamano.objects.all()
    razas = Raza.objects.all()
    generos = Genero.objects.all()


    if request.POST:
        accion = request.POST.get("btnAccion", "")
        if accion == "Buscar":
            rutpersona = request.POST.get("txtRut", "")
            random = randint(0, 99999)
            return render(request, '../templates/administrador/reg-mascota.htm', {'username':username, 'rutpersona':rutpersona, 'random':random, 'razas':razas, 'generos':generos, 'tamanos':tamanos})
        elif accion == "Registrar Mascota":
            identificador = request.POST.get("txtIdentificador", "")
            nombre = request.POST.get("txtNombre", "")
            rut_persona = request.POST.get("txtRutPersona", "")
            color = request.POST.get("txtColor", "")
            idtamano = request.POST.get("cboTamano", "")
            peso = request.POST.get("txtPeso", "")
            idraza = request.POST.get("cboRaza", "")
            idgenero = request.POST.get("cboGenero", "")

            #! INSTANCE
            tamano_id = Tamano.objects.get(IdTamano=idtamano)
            raza_id = Raza.objects.get(IdRaza=idraza)
            genero_id = Genero.objects.get(IdGenero=idgenero)
            rut_id = Persona.objects.get(RutPersona=rut_persona)

            masc = Mascota(
                IdMascota=identificador,
                Nombre=nombre,
                Color=color,
                IdTamano=tamano_id,
                Peso=peso,
                RutPersona=rut_id,
                IdRaza=raza_id,
                IdGenero=genero_id
            )
            masc.save()
            return render(request, '../templates/Administrador/reg-mascota.htm', {'username':username, 'razas':razas, 'generos':generos, 'tamanos':tamanos})
    return render(request, '../templates/administrador/reg-mascota.htm', {'username':username, 'razas':razas, 'generos':generos, 'tamanos':tamanos})

def eliMascota(request):
    user = auth.authenticate()
    username = request.user.username
    return render(request, '../templates/administrador/eli-mascota.htm', {'username':username})

def modMascota(request):
    user = auth.authenticate()
    username = request.user.username

    tamanos = Tamano.objects.all()
    razas = Raza.objects.all()
    generos = Genero.objects.all()

    if request.POST:
        accion = request.POST.get("btnAccion", "")
        if accion == "Buscar":
            rutpersona = request.POST.get("txtRut", "")
            mascotas = Mascota.objects.filter(RutPersona=rutpersona)
            return render(request, '../templates/administrador/mod-mascota.htm', {'mascotas':mascotas, 'rutpersona':rutpersona, 'username':username})
        elif accion == "Ingresar":
            mascota_id = request.POST.get("cboMascota", "")
            mascota = Mascota.objects.get(IdMascota=mascota_id)
            
            rut_per = request.POST.get("txtRut", "")
            mascotas = Mascota.objects.filter(RutPersona=rut_per)
            return render(request, '../templates/administrador/mod-mascota.htm', {'mas':mascota, 'rut_per':rut_per, 'mascotas':mascotas, 'username':username, 'tamanos':tamanos ,'razas': razas, 'generos':generos})

        elif accion == "Actualizar":

            rut_per = request.POST.get("txtRut", "")
            mascotas = Mascota.objects.filter(RutPersona=rut_per)



            name = request.POST.get("txtNombre", "") 
            mas = Mascota.objects.get(Nombre=name)


            nombre = request.POST.get("txtNombre", "")
            color = request.POST.get("txtColor", "")
            tamano = request.POST.get("cboTamano", "")
            peso = request.POST.get("txtPeso", "")
            raza = request.POST.get("cboRaza", "")
            genero = request.POST.get("cboGenero", "")

            #! INSTANCE
            tamano_id = Tamano.objects.get(IdTamano=tamano)
            raza_id = Raza.objects.get(IdRaza=raza)
            genero_id = Genero.objects.get(IdGenero=genero)

            mas.Nombre=nombre
            mas.Color=color
            mas.IdTamano=tamano_id
            mas.Peso=peso
            mas.IdRaza=raza_id
            mas.IdGenero=genero_id

            mas.save()
            return render(request, '../templates/administrador/mod-mascota.htm', {'username':username, 'tamanos':tamanos ,'razas': razas, 'generos':generos, 'rut_per':rut_per, 'mascotas':mascotas})



    return render(request, '../templates/administrador/mod-mascota.htm', {'username':username})

def AprobarCita(request):
    user = auth.authenticate()
    username = request.user.username
    citas = Cita.objects.all()
    return render(request, '../templates/administrador/aprobar-cita.htm', {'username': username, 'citas':citas})