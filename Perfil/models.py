from django.db import models

# --- 1. DATOS PERSONALES ---
class DatosPersonales(models.Model):
    descripcionperfil = models.CharField(max_length=50)
    perfilactivo = models.IntegerField(default=1)
    apellidos = models.CharField(max_length=60)
    nombres = models.CharField(max_length=60)
    nacionalidad = models.CharField(max_length=20)
    lugarnacimiento = models.CharField(max_length=60, blank=True, null=True)
    fechanacimiento = models.DateField()
    numerocedula = models.CharField(max_length=10, unique=True)
    
    SEXO_CHOICES = [('H', 'Hombre'), ('M', 'Mujer')]
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    
    estadocivil = models.CharField(max_length=50, blank=True, null=True)
    licenciaconducir = models.CharField(max_length=6, blank=True, null=True)
    telefonoconvencional = models.CharField(max_length=15, blank=True, null=True)
    telefonofijo = models.CharField(max_length=15, blank=True, null=True)
    direcciontrabajo = models.CharField(max_length=50, blank=True, null=True)
    direcciondomiciliaria = models.CharField(max_length=50, blank=True, null=True)
    sitioweb = models.CharField(max_length=60, blank=True, null=True)

    # NUEVO CAMPO PARA LA FOTO
    foto = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    class Meta:
        verbose_name = "Datos Personales"
        verbose_name_plural = "Datos Personales"


# --- 2. EXPERIENCIA LABORAL ---
class ExperienciaLaboral(models.Model):
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, related_name='experiencias')
    cargodesempenado = models.CharField(max_length=100)
    nombrempresa = models.CharField(max_length=50)
    lugarempresa = models.CharField(max_length=50, blank=True, null=True)
    emailempresa = models.CharField(max_length=100, blank=True, null=True)
    sitiowebempresa = models.CharField(max_length=100, blank=True, null=True)
    nombrecontactoempresarial = models.CharField(max_length=100, blank=True, null=True)
    telefonocontactoempresarial = models.CharField(max_length=60, blank=True, null=True)
    fechainiciogestion = models.DateField()
    fechafingestion = models.DateField(blank=True, null=True)
    descripcionfunciones = models.CharField(max_length=100)
    activarparaqueseveaenfront = models.BooleanField(default=True)
    rutacertificado = models.FileField(upload_to='certificados_laborales/', max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.cargodesempenado} en {self.nombrempresa}"


# --- 3. RECONOCIMIENTOS ---
class Reconocimiento(models.Model):
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, related_name='reconocimientos')
    tiporeconocimiento = models.CharField(max_length=100)
    fechareconocimiento = models.DateField()
    descripcionreconocimiento = models.CharField(max_length=100)
    entidadpatrocinadora = models.CharField(max_length=100, blank=True, null=True)
    nombrecontactoauspicia = models.CharField(max_length=100, blank=True, null=True)
    telefonocontactoauspicia = models.CharField(max_length=60, blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)
    rutacertificado = models.FileField(upload_to='certificados_reconocimientos/', max_length=100, blank=True, null=True)

    def __str__(self):
        return self.descripcionreconocimiento


# --- 4. CURSOS REALIZADOS ---
class CursoRealizado(models.Model):
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, related_name='cursos')
    nombrecurso = models.CharField(max_length=100)
    fechainicio = models.DateField()
    fechafin = models.DateField()
    totalhoras = models.IntegerField()
    descripcioncurso = models.CharField(max_length=100, blank=True, null=True)
    entidadpatrocinadora = models.CharField(max_length=100, blank=True, null=True)
    nombrecontactoauspicia = models.CharField(max_length=100, blank=True, null=True)
    telefonocontactoauspicia = models.CharField(max_length=60, blank=True, null=True)
    emailempresapatrocinadora = models.CharField(max_length=60, blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)
    rutacertificado = models.FileField(upload_to='certificados_cursos/', max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombrecurso


# --- 5. PRODUCTOS ACADÉMICOS ---
class ProductoAcademico(models.Model):
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, related_name='productos_academicos')
    nombrerecurso = models.CharField(max_length=100)
    clasificador = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)

    def __str__(self):
        return self.nombrerecurso


# --- 6. PRODUCTOS LABORALES ---
class ProductoLaboral(models.Model):
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, related_name='productos_laborales')
    nombreproducto = models.CharField(max_length=100)
    fechaproducto = models.DateField()
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)

    def __str__(self):
        return self.nombreproducto


# --- 7. VENTA GARAGE ---
class VentaGarage(models.Model):
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, related_name='ventas_garage')
    nombreproducto = models.CharField(max_length=100)
    estadoproducto = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    valordelbien = models.DecimalField(max_digits=5, decimal_places=2)
    activarparaqueseveaenfront = models.BooleanField(default=True)
    
    foto = models.ImageField(upload_to='fotos_garage/', blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)

    def __str__(self):
        return self.nombreproducto