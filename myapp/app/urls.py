from django.urls import path
from . import views

urlpatterns = [
    path('cargarArchivos/',views.cargarArchivos,name='cargarArchivos'),
    path('consultaHashtags/',views.consultaHashtags,name='consultaHashtags'),
    path('consultaMenciones/',views.consultaMenciones,name='consultaMenciones'),
    path('consultaSentimientos/',views.consultaSentimientos,name='consultaSentimientos'),
    path('Ayuda/',views.ayuda,name='Ayuda')
]
