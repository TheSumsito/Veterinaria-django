from django.shortcuts import render
from .models import Contacto, Provincia, Comuna, Persona, Usuario

#! IMPORTACION PARA TRABAJAR CON USUARIO
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate


#! FUNCION PARA REDIRECCIONAR LOGOUT
from django.http import HttpResponse,HttpResponseRedirect

# Create your views here.

#! VISTAS PRINCIPALES


def home(request):
    return render(request, '../templates/index.htm')

def homeAdmin(request):
    user = auth.authenticate()
    rutpersona = request.user.username
    persona = Persona.objects.get(RutPersona=rutpersona)
    return render(request, '../templates/administrador/index.htm', {'per':persona})

def homeUser(request):
    user = auth.authenticate()
    rutpersona = request.user.username
    persona = Persona.objects.get(RutPersona=rutpersona)
    return render(request, '../templates/usuario/index.htm', {'per':persona})

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



def RegistroUsuario(request):
    pro = Provincia.objects.all()
    com = Comuna.objects.all()
    if request.POST:
        nombre = request.POST.get("txtNombre", "")
        apellido = request.POST.get("txtApellido", "")
        correo = request.POST.get("txtCorreo", "")
        direccion = request.POST.get("txtDireccion", "")
        telefono = request.POST.get("txtTelefono", "")
        comuna = request.POST.get("cboComuna", "")

        #! USUARIO - CONTRASEÑA
        rutpersona = request.POST.get("txtRut", "")
        contrasena = request.POST.get("txtContrasena", "")

        #! INSTANCES
        comu_id = Comuna.objects.get(IdComuna=comuna)

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
            email=correo,
            username=rutpersona,
            password=contrasena,
            is_staff=False
        )
        per.save()
        usu.save()
        return render(request, '../templates/registro.htm', {'comuna': com, 'provincia': pro})
    else:
        return render(request, '../templates/registro.htm', {'comuna':com, 'provincia':pro})
