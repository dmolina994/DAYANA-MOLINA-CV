import io
import requests
import base64
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from pypdf import PdfWriter 

from Perfil.models import (
    DatosPersonales, ExperienciaLaboral, 
    CursoRealizado, Reconocimiento, 
    ProductoAcademico, ProductoLaboral, VentaGarage
)

def get_active_profile():
    return DatosPersonales.objects.filter(perfilactivo=1).first()

# Función auxiliar para convertir imagen de URL a Base64 (Para que el PDF la vea)
def get_image_base64(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            content_type = response.headers.get('content-type')
            encoded_string = base64.b64encode(response.content).decode('utf-8')
            return f"data:{content_type};base64,{encoded_string}"
    except Exception:
        return None
    return None

def home(request):
    perfil = get_active_profile()
    if not perfil:
        return render(request, 'home.html', {'perfil': None})

    context = {
        'perfil': perfil,
        'resumen_exp': ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)[:3],
        'resumen_cursos': CursoRealizado.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)[:3],
        'resumen_rec': Reconocimiento.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)[:3],
        'resumen_acad': ProductoAcademico.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)[:3],
        'resumen_lab': ProductoLaboral.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)[:3],
        'resumen_garage': VentaGarage.objects.all()[:5],
    }
    return render(request, 'home.html', context)

# Vistas de navegación simples
def experiencia(request): return render(request, 'experiencia.html', {'datos': ExperienciaLaboral.objects.all(), 'perfil': get_active_profile()})
def productos_academicos(request): return render(request, 'productos_academicos.html', {'datos': ProductoAcademico.objects.all(), 'perfil': get_active_profile()})
def productos_laborales(request): return render(request, 'productos_laborales.html', {'datos': ProductoLaboral.objects.all(), 'perfil': get_active_profile()})
def cursos(request): return render(request, 'cursos.html', {'datos': CursoRealizado.objects.all(), 'perfil': get_active_profile()})
def reconocimientos(request): return render(request, 'reconocimientos.html', {'datos': Reconocimiento.objects.all(), 'perfil': get_active_profile()})
def garage(request): return render(request, 'garage.html', {'datos': VentaGarage.objects.all(), 'perfil': get_active_profile()})

def pdf_datos_personales(request):
    perfil = get_object_or_404(DatosPersonales, perfilactivo=1)
    
    # PROCESAR FOTO PARA PDF (Solución al problema de la foto que no sale)
    foto_base64 = None
    if perfil.foto:
        foto_base64 = get_image_base64(perfil.foto.url)

    experiencias = ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    academicos = ProductoAcademico.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    laborales = ProductoLaboral.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    cursos_objs = CursoRealizado.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    reco_objs = Reconocimiento.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)

    template = get_template('cv_pdf_maestro.html')
    html = template.render({
        'perfil': perfil, 
        'foto_pdf': foto_base64, # Usaremos esta variable en el HTML
        'items': experiencias, 
        'productos': academicos,
        'productos_laborales': laborales, 
        'cursos': cursos_objs, 
        'reconocimientos': reco_objs
    })
    
    buffer_cv = io.BytesIO()
    pisa.CreatePDF(io.BytesIO(html.encode("UTF-8")), dest=buffer_cv)

    writer = PdfWriter()
    buffer_cv.seek(0)
    writer.append(buffer_cv)

    def pegar_certificados(queryset):
        for obj in queryset:
            if obj.rutacertificado:
                try:
                    r = requests.get(obj.rutacertificado.url, timeout=10)
                    if r.status_code == 200:
                        writer.append(io.BytesIO(r.content))
                except Exception: continue

    pegar_certificados(cursos_objs)
    pegar_certificados(reco_objs)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Portafolio_{perfil.apellidos}.pdf"'
    writer.write(response)
    writer.close()
    return response