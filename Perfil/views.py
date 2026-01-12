import io
import requests
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from pypdf import PdfWriter

from .models import (
    DatosPersonales, ExperienciaLaboral, CursoRealizado, 
    VentaGarage, Reconocimiento, ProductoAcademico, ProductoLaboral
)

# --- UTILIDADES ---

def get_active_profile():
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
    if perfil is None:
        perfil = DatosPersonales.objects.first()
    return perfil

# --- VISTAS DE NAVEGACIÓN (FRONTEND) ---

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
    datos = ProductoLaboral.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True).order_by('-fechaproducto')
    return render(request, 'productos_laborales.html', {'productos_laborales': datos, 'perfil': perfil})

def productos_academicos(request):
    perfil = get_active_profile()
    datos = ProductoAcademico.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    return render(request, 'productos_academicos.html', {'productos_academicos': datos, 'perfil': perfil})

def garage(request):
    perfil = get_active_profile()
    datos = VentaGarage.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    return render(request, 'ventagarage.html', {'garage_items': datos, 'perfil': perfil})

def cursos(request):
    perfil = get_active_profile()
    datos = CursoRealizado.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    return render(request, 'cursos.html', {'cursos': datos, 'perfil': perfil})

def reconocimientos(request):
    perfil = get_active_profile()
    datos = Reconocimiento.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True).order_by('-fechareconocimiento')
    return render(request, 'reconocimientos.html', {'reconocimientos': datos, 'perfil': perfil})

def experiencia(request):
    perfil = get_active_profile()
    datos = ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    return render(request, 'experiencia.html', {'experiencias': datos, 'perfil': perfil})


# --- VISTA PARA GENERAR EL PDF (ESTILO HOJA DE VIDA CON ANEXOS) ---

def generar_cv_pdf(request):
    perfil = get_active_profile()
    
    # Consultas de todos los datos activos
    experiencias = ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True).order_by('-fechainiciogestion')
    cursos_objs = CursoRealizado.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True).order_by('-fechafin')
    reconocimientos_objs = Reconocimiento.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    productos_acad = ProductoAcademico.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    productos_lab = ProductoLaboral.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)

    # 1. Crear el HTML del CV base
    template = get_template('hoja_de_vida.html')
    context = {
        'perfil': perfil,
        'items': experiencias,      # Usamos 'items' para ser compatible con el HTML de tu amigo
        'cursos': cursos_objs,
        'reconocimientos': reconocimientos_objs,
        'productos': productos_acad,
        'productos_laborales': productos_lab,
    }
    html = template.render(context)
    
    # 2. Generar PDF base en memoria
    buffer_cv_base = io.BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=buffer_cv_base)
    
    if pisa_status.err:
        return HttpResponse('Error al generar el cuerpo del PDF', status=500)
    
    # 3. Unir PDFs (CV + Certificados de Cloudinary)
    writer = PdfWriter()
    buffer_cv_base.seek(0)
    writer.append(buffer_cv_base)

    # Lista de modelos que tienen certificados PDF
    fuentes_certificados = [
        (cursos_objs, 'rutacertificado'),
        (reconocimientos_objs, 'rutacertificado')
    ]

    for queryset, campo_file in fuentes_certificados:
        for obj in queryset:
            archivo = getattr(obj, campo_file)
            # Solo intentamos anexar si es un archivo PDF
            if archivo and archivo.url.lower().endswith('.pdf'):
                try:
                    r = requests.get(archivo.url, timeout=15)
                    if r.status_code == 200:
                        writer.append(io.BytesIO(r.content))
                except Exception as e:
                    print(f"Error al descargar certificado de {obj}: {e}")

    # 4. Responder con el PDF final
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="CV_{perfil.apellidos}.pdf"'
    
    writer.write(response)
    writer.close()
    
    return response