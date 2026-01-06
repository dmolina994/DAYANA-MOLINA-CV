from django.contrib import admin
from .models import (
    DatosPersonales,
    ExperienciaLaboral,
    ProductoAcademico,
    ProductoLaboral,
    Reconocimiento,
    CursoRealizado,
    VentaGarage
)

# -------------------------------------------------------------
# REGISTRO DE MODELOS
# -------------------------------------------------------------

# 1. Datos Personales
@admin.register(DatosPersonales)
class DatosPersonalesAdmin(admin.ModelAdmin):
    # Ajustado a los campos reales del SQL:
    # Nota: 'emailpersonal' NO existe en la tabla SQL DatosPersonales, por eso lo quité.
    list_display = ('nombres', 'apellidos', 'numerocedula', 'descripcionperfil', 'perfilactivo')
    search_fields = ('nombres', 'apellidos', 'numerocedula')
    list_filter = ('perfilactivo', 'nacionalidad', 'sexo')

# 2. Experiencia Laboral
@admin.register(ExperienciaLaboral)
class ExperienciaLaboralAdmin(admin.ModelAdmin):
    # Nombres corregidos: cargodesempenado, nombrempresa, fechainiciogestion, fechafingestion
    list_display = ('cargodesempenado', 'nombrempresa', 'fechainiciogestion', 'fechafingestion', 'activarparaqueseveaenfront')
    list_filter = ('activarparaqueseveaenfront', 'nombrempresa')
    # date_hierarchy usa el campo de fecha real
    date_hierarchy = 'fechainiciogestion'
    # Para buscar fácilmente
    search_fields = ('cargodesempenado', 'nombrempresa')

# 3. Productos Académicos
@admin.register(ProductoAcademico)
class ProductoAcademicoAdmin(admin.ModelAdmin):
    # Nombres corregidos: nombrerecurso
    list_display = ('nombrerecurso', 'clasificador', 'activarparaqueseveaenfront')
    list_filter = ('activarparaqueseveaenfront', 'clasificador')
    search_fields = ('nombrerecurso', 'descripcion')

# 4. Productos Laborales
@admin.register(ProductoLaboral)
class ProductoLaboralAdmin(admin.ModelAdmin):
    # Nombres corregidos: nombreproducto, fechaproducto
    list_display = ('nombreproducto', 'fechaproducto', 'activarparaqueseveaenfront')
    list_filter = ('activarparaqueseveaenfront',)
    search_fields = ('nombreproducto', 'descripcion')

# 5. Reconocimientos
@admin.register(Reconocimiento)
class ReconocimientoAdmin(admin.ModelAdmin):
    # Nombres corregidos: descripcionreconocimiento (SQL no tiene nombre_reconocimiento, usa descripcion)
    list_display = ('descripcionreconocimiento', 'tiporeconocimiento', 'fechareconocimiento', 'activarparaqueseveaenfront')
    list_filter = ('activarparaqueseveaenfront', 'tiporeconocimiento')
    date_hierarchy = 'fechareconocimiento'

# 6. Cursos Realizados
@admin.register(CursoRealizado)
class CursoRealizadoAdmin(admin.ModelAdmin):
    # Nombres corregidos: nombrecurso, fechafin (no fecha_termino)
    list_display = ('nombrecurso', 'entidadpatrocinadora', 'fechafin', 'totalhoras', 'activarparaqueseveaenfront')
    list_filter = ('activarparaqueseveaenfront', 'entidadpatrocinadora')
    date_hierarchy = 'fechafin'
    search_fields = ('nombrecurso', 'entidadpatrocinadora')

# 7. Venta Garage
@admin.register(VentaGarage)
class VentaGarageAdmin(admin.ModelAdmin):
    # Nombres corregidos: estadoproducto, valordelbien
    list_display = ('nombreproducto', 'estadoproducto', 'valordelbien', 'activarparaqueseveaenfront')
    list_filter = ('activarparaqueseveaenfront', 'estadoproducto')
    search_fields = ('nombreproducto',)