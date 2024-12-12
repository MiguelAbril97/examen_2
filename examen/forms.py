from django import forms
from django.forms import ModelForm
from django.db.models import Q
from .models import *
from datetime import date
import datetime

class CrearForm(ModelForm):
    class Meta:
        model = Promocion
      
        fields = ['nombre', 'descripcion', 'producto', 'usuario',
                  'descuento', 'fecha_inicio', 'fecha_fin','activa']
        
        widgets = {
            'descuento':forms.NumberInput(attrs={'min': '0',' max_digits':'10'}),
            "fecha_inicio":forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "fecha_fin":forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            'usuario':forms.CheckboxSelectMultiple()
        }
        
    def clean(self):
        super().clean()
        
        nombre = self.cleaned_data.get('nombre')
        descripcion = self.cleaned_data.get('descripcion')
        producto = self.cleaned_data.get('producto')
        usuarios = self.cleaned_data.get('usuario')
        descuento = self.cleaned_data.get('descuento')
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        fecha_fin = self.cleaned_data.get('fecha_fin')
        activa = self.cleaned_data.get('activa')
        
        promoNombre = Promocion.objects.filter(nombre = nombre).first()
        
        #Recojo todos los usuarios menores para despues comprobar si algun usuario escogido es menor
        menoresEdad = Usuario.objects.filter(edad__lt=18).all()
        
        noPromos = Producto.objects.filter(puede_tener_promociones=False).all()

        if(not promoNombre is None):
            if(not self.instance is None and promoNombre.id == self.instance.id):
                pass
            else:
                self.add_error('nombre','Ya existe una promoción con ese nombre')
        
        #hago doble bucle for para comprobar que todos los usuarios sean mayores. Si coincide algun id 
        # el booleano pasara a true 
        menor = False
        for usuario in usuarios:
            for i in menoresEdad:
                if(usuario.id == i.id):
                    menor = True
        if(menor):
            self.add_error('usuario','Las promociones solo se pueden aplicar a mayores de edad')
            
        sinPromo = False
        for i in noPromos:
            if(i.id == producto.id):
                sinPromo == True
                
        if(sinPromo):
            self.add_error('producto','El producto seleccionado no es válido')
        
        if(len(descripcion) < 100):
            self.add_error('descripcion','Al menos debes indicar 100 caracteres')
            
        if(fecha_fin <= fecha_inicio):
            self.add_error('fecha_inicio','Al debe ser inferior a la fecha de inicio')
        
        if(descuento < 0 or descuento > 10):
            self.add_error('descuento','Debe ser un valor entre 0 y 10')

        fechaHoy = date.today()
        if(fecha_fin < fechaHoy):
            self.add_error('fecha_fin', 'No puede ser inferior a la fecha actual')
        
        return self.cleaned_data
        
class Buscar(forms.Form):
    
    buscarTexto = forms.CharField(required=False)
    buscarFinDesde = forms.DateField(required=False,
                                widget= forms.DateInput(format="%Y-%m-%d", 
                                                          attrs={"type": "date"},
                                                          )
                                ) 
    buscarFinHasta = forms.DateField(required=False,
                                widget= forms.DateInput(format="%Y-%m-%d", 
                                                          attrs={"type": "date"},
                                                          )
                                ) 
    buscarDescuento = forms.IntegerField(required= False,
                                         widget=forms.NumberInput(attrs={'min': '0',' max_digits':'10'})
                                         )
    buscarUsuarios = forms.ModelMultipleChoiceField(queryset=Usuario.objects.filter(edad__gte=18).all(),
                                            required=False,
                                            widget=forms.CheckboxSelectMultiple()
                                            )
    esActiva = forms.BooleanField(required=False)
    
    def clean(self):    
        super().clean()
        
        texto = self.cleaned_data.get('buscarTexto')
        desde = self.cleaned_data.get('buscarFinDesde')
        hasta = self.cleaned_data.get('buscarFinHasta')
        descuento = self.cleaned_data.get('buscarDescuento')
        usuario = self.cleaned_data.get('buscarUsuarios')
        activa = self.cleaned_data.get('esActiva')
        
        if(texto == "" and
           desde is None and
           hasta is None and
           descuento is None and
           len(usuario)==0 and
           activa == False
           ):
            msg = "Debe rellenar al menos un campo"
            self.add_error('buscarTexto',msg)
            self.add_error('buscarFinDesde',msg)
            self.add_error('buscarFinHasta',msg)
            self.add_error('buscarDescuento',msg)
            self.add_error('buscarUsuarios',msg)
            self.add_error('esActiva',msg)