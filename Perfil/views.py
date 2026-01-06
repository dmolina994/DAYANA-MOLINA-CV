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
    # Buscamos el perfil activo según tu configuración del admin
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
    # Usamos 'productos' para que coincida con el bucle del HTML
    productos = ProductoAcademico.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    )
    return render(request, 'productos_academicos.html', {'productos': productos, 'perfil': perfil})

def productos_laborales(request):
    perfil = get_active_profile()
    # Usamos 'productos' para que coincida con el bucle del HTML
    productos = ProductoLaboral.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    ).order_by('-fechaproducto')
    return render(request, 'productos_laborales.html', {'productos': productos, 'perfil': perfil})

def cursos(request):
    perfil = get_active_profile()
    # Enviamos 'cursos' para el bucle en cursos.html
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
    # He visto que tienes garage.html y ventagarage.html
    # Usaremos 'items' como variable estándar para el bucle
    objetos = VentaGarage.objects.filter(
        idperfilconqueestaactivo=perfil,
        activarparaqueseveaenfront=True
    )
    # Cambia 'ventagarage.html' por 'garage.html' si prefieres el otro archivo
    return render(request, 'ventagarage.html', {'items': objetos, 'perfil': perfil})