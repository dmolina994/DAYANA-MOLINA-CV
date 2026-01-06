from django.shortcuts import render
from .models import (
    DatosPersonales,
    ExperienciaLaboral,
    CursoRealizado,
    VentaGarage,
    Reconocimiento,
    ProductoAcademico,
    ProductoLaboral
)

def get_active_profile():
    return DatosPersonales.objects.filter(perfilactivo=1).first()

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

def experiencia(request):
    perfil = get_active_profile()
    datos = ExperienciaLaboral.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    )
    return render(request, 'experiencia.html', {'datos': datos, 'perfil': perfil})

def productos_academicos(request):
    perfil = get_active_profile()
    datos = ProductoAcademico.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    )
    return render(request, 'productos_academicos.html', {'datos': datos, 'perfil': perfil})

def productos_laborales(request):
    perfil = get_active_profile()
    datos = ProductoLaboral.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    ).order_by('-fechaproducto')
    return render(request, 'productos_laborales.html', {'datos': datos, 'perfil': perfil})

def cursos(request):
    perfil = get_active_profile()
    datos = CursoRealizado.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    )
    return render(request, 'cursos.html', {'datos': datos, 'perfil': perfil})

def reconocimientos(request):
    perfil = get_active_profile()
    datos = Reconocimiento.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    ).order_by('-fechareconocimiento')
    return render(request, 'reconocimientos.html', {'datos': datos, 'perfil': perfil})

def garage(request):
    perfil = get_active_profile()
    datos = VentaGarage.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    )
    return render(request, 'garage.html', {'datos': datos, 'perfil': perfil})
