from django.db import models

# Create your models here.
class Contacto(models.Model):
    Correo = models.CharField(max_length=50)
    Nombre = models.CharField(max_length=50)
    Apellido = models.CharField(max_length=50)
    Telefono = models.IntegerField()
    Asunto = models.CharField(max_length=50)
    Mensaje = models.CharField(max_length=50)

    def __str__(self):
        return self.Correo

class Usuario(models.Model):
    RutPersona = models.CharField(primary_key=True, max_length=50)
    Contrasena = models.CharField(max_length=50)
    Tipo = models.BooleanField()

    def __str__(self):
        return self.RutPersona

class Provincia(models.Model):
    IdProvincia = models.IntegerField(primary_key=True)
    Descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.Descripcion

class Comuna(models.Model):
    IdComuna = models.IntegerField(primary_key=True)
    Descripcion = models.CharField(max_length=50)
    IdProvincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)

    def __str__(self):
        return self.Descripcion


class Persona(models.Model):
    RutPersona = models.CharField(primary_key=True, max_length=50)
    Nombre = models.CharField(max_length=50)
    Apellido = models.CharField(max_length=50)
    Correo = models.CharField(max_length=50)
    Telefono = models.IntegerField()
    Direccion = models.CharField(max_length=50)
    IdComuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)

    def __str__(self):
        return self.Nombre


class TipoMascota(models.Model):
    IdTipo = models.IntegerField(primary_key=True)
    Descripcion = models.CharField(max_length=50)
    
    def __str__(self):
        return self.Descripcion

class Raza(models.Model):
    IdRaza = models.IntegerField(primary_key=True)
    Descripcion = models.CharField(max_length=50)
    IdTipo = models.ForeignKey(TipoMascota, on_delete=models.CASCADE)

    def __str__(self):
        return self.Descripcion

class Genero(models.Model):
    IdGenero = models.IntegerField(primary_key=True)
    Descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.Descripcion

class Tamano(models.Model):
    IdTamano = models.IntegerField(primary_key=True)
    Descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.Descripcion


class Mascota(models.Model):
    IdMascota = models.IntegerField(primary_key=True)
    Nombre = models.CharField(max_length=50)
    Color = models.CharField(max_length=50)
    IdTamano = models.ForeignKey(Tamano, on_delete=models.CASCADE)
    Peso = models.IntegerField()
    RutPersona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    IdRaza = models.ForeignKey(Raza, on_delete=models.CASCADE)
    IdGenero = models.ForeignKey(Genero, on_delete=models.CASCADE)

    def __str__(self):
        return self.Nombre

class TipoConsulta(models.Model):
    IdTipo = models.IntegerField(primary_key=True)
    Descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.Descripcion

class Cita(models.Model):
    IdCita = models.IntegerField(primary_key=True)
    Descripcion = models.CharField(max_length=50)
    Fecha = models.DateField()
    Hora = models.TimeField()
    IdMascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    IdTipo = models.ForeignKey(TipoConsulta, on_delete=models.CASCADE)
    Estado = models.BooleanField()

    def __str__(self):
        return self.Descripcion