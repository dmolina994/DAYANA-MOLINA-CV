from django.shortcuts import render
from .models import (
    DatosPersonales, ExperienciaLaboral, CursoRealizado, 
    VentaGarage, Reconocimiento, ProductoAcademico, ProductoLaboral
)

def get_active_profile():
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
    if perfil is None:
        # Si no existe uno activo, toma el primero
        perfil = DatosPersonales.objects.first()
    return perfil


def home(request):
    perfil = get_active_profile()
    context = {
        'perfil': perfil,
        'resumen_exp': ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil)[:3],
        'resumen_cursos': CursoRealizado.objects.filter(idperfilconqueestaactivo=perfil)[:3],
        'resumen_garage': VentaGarage.objects.filter(idperfilconqueestaactivo=perfil)[:5],
        'resumen_rec': Reconocimiento.objects.filter(idperfilconqueestaactivo=perfil)[:3],
        'resumen_acad': ProductoAcademico.objects.filter(idperfilconqueestaactivo=perfil)[:3],
        'resumen_lab': ProductoLaboral.objects.filter(idperfilconqueestaactivo=perfil)[:3],
    }
    return render(request, 'home.html', context)

def productos_laborales(request):
    perfil = get_active_profile()
    # Nombre clave: 'productos_laborales'
    datos = ProductoLaboral.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True).order_by('-fechaproducto')
    return render(request, 'productos_laborales.html', {'productos_laborales': datos, 'perfil': perfil})

def productos_academicos(request):
    perfil = get_active_profile()
    # Nombre clave: 'productos_academicos'
    datos = ProductoAcademico.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    return render(request, 'productos_academicos.html', {'productos_academicos': datos, 'perfil': perfil})

def garage(request):
    perfil = get_active_profile()
    # Nombre clave: 'garage_items'
    datos = VentaGarage.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    return render(request, 'ventagarage.html', {'garage_items': datos, 'perfil': perfil})

def cursos(request):
    perfil = get_active_profile()
    # Nombre clave: 'cursos'
    datos = CursoRealizado.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    return render(request, 'cursos.html', {'cursos': datos, 'perfil': perfil})

def reconocimientos(request):
    perfil = get_active_profile()
    # Nombre clave: 'reconocimientos'
    datos = Reconocimiento.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True).order_by('-fechareconocimiento')
    return render(request, 'reconocimientos.html', {'reconocimientos': datos, 'perfil': perfil})

def experiencia(request):
    perfil = get_active_profile()
    # Nombre clave: 'experiencias'
    datos = ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    return render(request, 'experiencia.html', {'experiencias': datos, 'perfil': perfil})