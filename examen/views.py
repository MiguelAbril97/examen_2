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
            
