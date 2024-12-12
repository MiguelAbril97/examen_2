from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages


# Create your views here.

def index(request):
    return render(request, 'index.html') 

def crear (request):
    datosFormulario = None
    if(request.method == 'POST'):
        datosFormulario = request.POST
    formulario = CrearForm(datosFormulario)

    if(request.method == 'POST'):
        promoCreada = crear_promocion(formulario)
        if promoCreada:
            messages.success(request, 'Se ha creado la promoción '+formulario.cleaned_data.get('nombre')+" correctamente")
            redirect('index')
            
    return render(request, 'promo/crear.html',{"formulario":formulario})

def crear_promocion (formulario):
    promo = False
    
    if formulario.is_valid():
        try:
            formulario.save()
            promo = True
        except Exception as error:
            print(error)
    return promo    

def buscar (request):
   
    if(len(request.GET) > 0):
        formulario = Buscar(request.GET)
        
        if formulario.is_valid():            
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
            
            QSpromos = Promocion.objects.select_related('producto').prefetch_related('usuario')
            
            texto = formulario.cleaned_data.get('buscarTexto')
            desde = formulario.cleaned_data.get('buscarFinDesde')
            hasta = formulario.cleaned_data.get('buscarFinHasta')
            descuento = formulario.cleaned_data.get('buscarDescuento')
            usuario = formulario.cleaned_data.get('buscarUsuarios')
            activa = formulario.cleaned_data.get('esActiva')
            
            if(texto !=""):
                QSpromos = Promocion.objects.filter(Q(nombre__contains = texto) | Q(descripcion__contains=texto))
                mensaje_busqueda += "Que el nombre o la descripcion contenga"+texto+"\n"
                
            if(not desde is None):
                QSpromos = Promocion.objects.filter(fecha_fin__gte=desde)
                mensaje_busqueda += "Que la fecha fin sea mayor a"+desde+"\n"
             
            if(not hasta is None):
                QSpromos = Promocion.objects.filter(fecha_fin__lte=hasta)
                mensaje_busqueda += "Que la fecha fin sea menor a"+hasta+"\n"
            
            if(not descuento is None):
                QSpromos = Promocion.objects.filter(descuento__gt = descuento)
                mensaje_busqueda += "Que tengan un descuento mayor a "+descuento+"\n"
            
            if(len(usuario) > 0):
                
                mensaje_busqueda +="Usuario: {usuario[0].nombre}"
                filtroOR = Q(usuario=usuario[0])
                for i in usuario[1:]:
                    mensaje_busqueda += " o {i[0].nombre}"
                    filtroOR |= Q(usuario=i)
                mensaje_busqueda += "\n"
                QSpromos = QSpromos.filter(filtroOR)
            
            if(activa):
                mensaje_busqueda += "Que este activa"
                QSpromos = QSpromos.filter(activa=True)
            else:
                mensaje_busqueda += "Que no este activa"
                QSpromos = QSpromos.filter(activa=False)
            
            promos = QSpromos.all()
            
            return render(request,'promo/lista_busqueda.html',{'promos':promos, 'mensaje':mensaje_busqueda})
        
    else:
        formulario = Buscar(None)    
            
    return render(request, 'promo/buscar.html',{"formulario":formulario})