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
    # Buscamos el perfil marcado con 1 en el admin
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
    experiencias = ExperienciaLaboral.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    )
    return render(request, 'experiencia.html', {'experiencias': experiencias, 'perfil': perfil})

def productos_academicos(request):
    perfil = get_active_profile()
    # Cambiado a 'productos_academicos' (o revisa si tu HTML usa 'productos')
    academicos = ProductoAcademico.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    )
    return render(request, 'productos_academicos.html', {'productos_academicos': academicos, 'perfil': perfil})

def productos_laborales(request):
    perfil = get_active_profile()
    # Cambiado a 'productos_laborales' para que coincida con tu {% for producto in productos_laborales %}
    laborales = ProductoLaboral.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    ).order_by('-fechaproducto')
    return render(request, 'productos_laborales.html', {'productos_laborales': laborales, 'perfil': perfil})

def cursos(request):
    perfil = get_active_profile()
    lista_cursos = CursoRealizado.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    )
    return render(request, 'cursos.html', {'cursos': lista_cursos, 'perfil': perfil})

def reconocimientos(request):
    perfil = get_active_profile()
    recs = Reconocimiento.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    ).order_by('-fechareconocimiento')
    return render(request, 'reconocimientos.html', {'reconocimientos': recs, 'perfil': perfil})

def garage(request):
    perfil = get_active_profile()
    # Cambiado a 'garage_items' para que coincida con tu {% for item in garage_items %}
    objetos = VentaGarage.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    )
    # Usamos ventagarage.html que es el que tienes en tus carpetas
    return render(request, 'ventagarage.html', {'garage_items': objetos, 'perfil': perfil})