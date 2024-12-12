from django.urls import path,re_path
from .import views

    
urlpatterns = [
    path('',views.index,name='index'),
    path('promo/crear',views.crear,name='crear'),

]