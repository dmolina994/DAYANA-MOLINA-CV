from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import MinValueValidator, RegexValidator # Se añade RegexValidator

# --- FUNCIONES DE VALIDACIÓN ---

def validar_no_futuro(value):
    """Bloquea cualquier fecha que sea posterior al día de hoy."""
    if value > timezone.now().date():
        raise ValidationError('La fecha no puede ser posterior a la fecha actual.')

# --- 1. DATOS PERSONALES ---
class DatosPersonales(models.Model):
    descripcionperfil = models.CharField(max_length=50)
    perfilactivo = models.IntegerField(default=1)
    apellidos = models.CharField(max_length=60)
    nombres = models.CharField(max_length=60)
    nacionalidad = models.CharField(max_length=20)
    lugarnacimiento = models.CharField(max_length=60, blank=True, null=True)
    fechanacimiento = models.DateField(validators=[validar_no_futuro])
    
    # MODIFICACIÓN AQUÍ: Única y solo números (exactamente 10)
    numerocedula = models.CharField(
        max_length=10, 
        unique=True, 
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='La cédula debe tener 10 dígitos numéricos.',
                code='cedula_invalida'
            )
        ]
    )
    
    SEXO_CHOICES = [('H', 'Hombre'), ('M', 'Mujer')]
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    
    estadocivil = models.CharField(max_length=50, blank=True, null=True)
    licenciaconducir = models.CharField(max_length=6, blank=True, null=True)
    telefonoconvencional = models.CharField(max_length=15, blank=True, null=True)
    telefonofijo = models.CharField(max_length=15, blank=True, null=True)
    direcciontrabajo = models.CharField(max_length=50, blank=True, null=True)
    direcciondomiciliaria = models.CharField(max_length=50, blank=True, null=True)
    sitioweb = models.CharField(max_length=60, blank=True, null=True)
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
    fechainiciogestion = models.DateField(validators=[validar_no_futuro])
    fechafingestion = models.DateField(blank=True, null=True, validators=[validar_no_futuro])
    descripcionfunciones = models.CharField(max_length=100)
    activarparaqueseveaenfront = models.BooleanField(default=True)
    rutacertificado = models.FileField(upload_to='certificados_laborales/', max_length=100, blank=True, null=True)

    def clean(self):
        super().clean()
        if self.fechainiciogestion and self.fechafingestion:
            if self.fechafingestion < self.fechainiciogestion:
                raise ValidationError({
                    'fechafingestion': 'La fecha de fin gestión no puede ser anterior a la fecha de inicio.'
                })

    def __str__(self):
        return f"{self.cargodesempenado} en {self.nombrempresa}"


# --- 3. RECONOCIMIENTOS ---
class Reconocimiento(models.Model):
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, related_name='reconocimientos')
    tiporeconocimiento = models.CharField(max_length=100)
    fechareconocimiento = models.DateField(validators=[validar_no_futuro])
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
    fechainicio = models.DateField(validators=[validar_no_futuro])
    fechafin = models.DateField(validators=[validar_no_futuro])
    # Validación: Horas no pueden ser negativas (mínimo 1 hora)
    totalhoras = models.IntegerField(validators=[MinValueValidator(1)])
    descripcioncurso = models.CharField(max_length=100, blank=True, null=True)
    entidadpatrocinadora = models.CharField(max_length=100, blank=True, null=True)
    nombrecontactoauspicia = models.CharField(max_length=100, blank=True, null=True)
    telefonocontactoauspicia = models.CharField(max_length=60, blank=True, null=True)
    emailempresapatrocinadora = models.CharField(max_length=60, blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)
    rutacertificado = models.FileField(upload_to='certificados_cursos/', max_length=100, blank=True, null=True)

    def clean(self):
        super().clean()
        if self.fechainicio and self.fechafin:
            if self.fechafin < self.fechainicio:
                raise ValidationError({
                    'fechafin': 'La fecha de fin del curso no puede ser anterior a la de inicio.'
                })

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
    fechaproducto = models.DateField(validators=[validar_no_futuro])
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)

    def __str__(self):
        return self.nombreproducto


# --- 7. VENTA GARAGE ---
class VentaGarage(models.Model):
    ESTADO_CHOICES = [
        ('Bueno', 'Bueno'),
        ('Regular', 'Regular'),
    ]

    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, related_name='ventas_garage')
    nombreproducto = models.CharField(max_length=100)
    estadoproducto = models.CharField(
        max_length=40, 
        choices=ESTADO_CHOICES, 
        default='Bueno'
    )
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    # Validación: El valor no puede ser menor a 0.01 (no puede ser gratis o negativo)
    valordelbien = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.01)])
    foto = models.ImageField(upload_to='fotos_garage/', blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)

    def __str__(self):
        return self.nombreproducto