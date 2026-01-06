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
    """Busca el perfil marcado como activo (1)."""
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
    # Nombre 'experiencias' para coincidir con {% for exp in experiencias %}
    experiencias = ExperienciaLaboral.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    )
    return render(request, 'experiencia.html', {'experiencias': experiencias, 'perfil': perfil})

def cursos(request):
    perfil = get_active_profile()
    # Nombre 'cursos' para coincidir con {% for curso in cursos %}
    cursos_list = CursoRealizado.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    )
    return render(request, 'cursos.html', {'cursos': cursos_list, 'perfil': perfil})

def reconocimientos(request):
    perfil = get_active_profile()
    # Nombre 'reconocimientos' para coincidir con {% for rec in reconocimientos %}
    recs = Reconocimiento.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    ).order_by('-fechareconocimiento')
    return render(request, 'reconocimientos.html', {'reconocimientos': recs, 'perfil': perfil})

def productos_academicos(request):
    perfil = get_active_profile()
    # Cambiado a 'productos_academicos' para que tu HTML lo encuentre
    datos = ProductoAcademico.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    )
    return render(request, 'productos_academicos.html', {'productos_academicos': datos, 'perfil': perfil})

def productos_laborales(request):
    perfil = get_active_profile()
    # Cambiado a 'productos_laborales' para que tu HTML lo encuentre
    datos = ProductoLaboral.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    ).order_by('-fechaproducto')
    return render(request, 'productos_laborales.html', {'productos_laborales': datos, 'perfil': perfil})

def garage(request):
    perfil = get_active_profile()
    # Usamos 'productos_garage' o el nombre que tengas en el {% for ... %} de garage.html
    datos = VentaGarage.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    )
    return render(request, 'garage.html', {'productos_garage': datos, 'perfil': perfil})